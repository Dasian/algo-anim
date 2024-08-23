"""
    Delegates animation rendering to multiple processes
    Keeps track of animation queue
    Main program for running all of this
"""
from manim import *
from graphs.scenes import *
import subprocess as sp
import multiprocessing as mp
import time
import argparse
import platform
import json
from graphs.generator import *

graph_algos = ['BFS', 'DFS']
start_time = time.time()
playback_queue = mp.Queue()
# Note: you can't have a playlist using xdg-open

# driver
def main():
    # sets watch video command, default config file,
    # and media generation path based on os
    os_init()

    # get commandline arguments
    cmd_args = cmdline_args()
    num_animations = cmd_args.num_animations
    algo = cmd_args.algo
    is_random = cmd_args.random
    is_infinite = cmd_args.inf

    # doesn't do anything rn
    max_runtime = cmd_args.runtime    # in seconds

    # helper to generate animation arguments for pool workers
    def create_anim_job(anim_num=0):
        # create a list of animations to render
        worker_algo = graph_algos[random.randint(0, len(graph_algos)-1)] if is_random else algo
        worker_args = (anim_num,worker_algo,conf_template,cmd_args.size)
        return worker_args

    # create a list of animations to render
    anim_list = []
    for i in range(num_animations):
        anim_list.append(create_anim_job(i))

    # give workers rendering job
    # automatically assigns new job when finished
    pool = mp.Pool()
    for anim_job in anim_list:
        results = pool.apply_async(render_worker, args=anim_job, callback=worker_callback)
        time.sleep(1)   # don't delete, manim race condition

    # playback until limit reached/indefinitely
    num_complete = 0 if not is_infinite else len(anim_list)
    while num_complete < num_animations or is_infinite:

        # play rendered scene
        open_cmd = playback_queue.get()
        sp.Popen(open_cmd)  
        filename = open_cmd[1]
        result = sp.check_output(
            f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{filename}"',
            shell=True).decode()
        fields = json.loads(result)['streams'][0]
        duration = fields['duration']

        # assign new animation if infinite
        if is_infinite:
            anim_job = create_anim_job(num_complete)
            pool.apply_async(render_worker, args=anim_job, callback=worker_callback)

        # wait until scene is finished playing
        num_complete += 1
        time.sleep(float(duration))

    # TODO graceful shutdown for infinite animations

    print('shutting down...')
    pool.close()
    pool.join()

def render_worker(num, algo,  conf, ds_size):
    """Render a scene and add it to playback queue"""
    print('render worker starting')

    # name rendered algo
    fname = algo.upper() + str(num) + ext
    conf["output_file"] = fname
    conf["partial_movie_dir"] = "{video_dir}/partial_movie_files/" + algo.upper() + str(num)

    # render algo
    scene = None
    with tempconfig(conf):
        if algo.upper() in graph_algos:
            scene = GraphScene(n=ds_size, algo=algo.upper())
        else:
            raise("'" + algo + "'" + " is not a supported algorithm")

        scene.render()

    # return command to view render
    open_cmd = [os_open]
    open_cmd.append(scene_path + fname)
    return open_cmd

def worker_callback(res):
    """when a worker completes an animation, add to queue"""
    # res is the cmd to view render (list of shell args)
    playback_queue.put(res)
    return


def cmdline_args():
    """Set cmdline args and return parsed args object"""

    # --runtime = 10, 50, 100, ... (in seconds)
    parser = argparse.ArgumentParser(description='Generate an algorithm animation with manim')
    # implies a data structure
    # ["BFS, "DFS", "sort", "insertion-sort"]
    parser.add_argument('-a', '--algo', type=str, 
                        choices=['BFS', 'DFS', 'bfs', 'dfs'], default='BFS',
                        help='Algorithm to display')
    # maybe just make one size arg for arrs, graphs, and others?
    parser.add_argument('--size', type=int, 
                        default=5,
                        help='Size of the generated data structure')
    parser.add_argument('--inf', '--infinite', type=bool, 
                        default=False, action=argparse.BooleanOptionalAction,
                        help='Generate animations indefinitely')
    # currently just changes the number of workers
    # since workers only make one animation
    parser.add_argument('--num-animations', type=int, 
                        default=3,
                        help='Number of animations to generate')
    # a set data structure should restrict this?
    parser.add_argument('-r', '--random', type=bool, 
                        default=False, action=argparse.BooleanOptionalAction,
                        help='Generate a random animation')
    # TODO
    parser.add_argument('-ds', '--data-structure', type=str, 
                        default='graph', choices=['graph'],
                        help='Data structure to generate animations on')
    # TODO make this,, better
    parser.add_argument('-rt', '--runtime', type=int, 
                        default=60,
                        help='Maximum runtime of the program in seconds')
    return parser.parse_args()

def os_init():
    """Sets playback command, media directory, and sets default config"""
    # os specific init
    global os_open
    curr_os = platform.system()
    media_dir = ''
    os_open = []
    if curr_os == 'Linux':
        os_open = 'xdg-open'
        media_dir = '/tmp/algo-anim'
    elif curr_os == 'Windows':
        os_open = 'cygstart'
    elif curr_os == 'Darwin':
        os_open = 'open'

    global scene_path
    global ext
    # TODO remove quality folder + add user input
    quality = '480p15/' # /1080p60
    ext = ".mp4"
    scene_path = media_dir + '/videos/'
    scene_path += quality

    # aspect_ratio, quality, media_dir, movie_file_extension
    # output_file, scene_names, window_position, window_size
    # write_to_movie, force_window
    global conf_template
    conf_template = {
        "quality": "low_quality",
        "disable_caching": True,
        "output_file": 'tmp',   # will be replaced with the filename
        "media_dir": media_dir, # changes based on os
        "verbosity": "WARNING",
        "partial_movie_dir": "{video_dir}/partial_movie_files/"
    }

def uptime():
    """Returns the number of seconds the program has been running"""
    return time.time() - start_time

if __name__ == "__main__":
    main()
