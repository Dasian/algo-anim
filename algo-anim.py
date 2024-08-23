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
from graphs.generator import *

graph_algos = ['BFS', 'DFS']

# driver
def main():
    # sets watch video command, default config file,
    # and media generation path
    init()

    # get commandline arguments
    cmd_args = cmdline_args()
    global start_time
    num_workers = cmd_args.num_animations
    algo = cmd_args.algo
    is_infinite = cmd_args.inf
    start_time = time.time()
    max_runtime = cmd_args.runtime    # in seconds
    is_random = cmd_args.random

    # Note: you can't have a playlist using xdg-open
    playback_queue = mp.Queue()

    # multiprocessing shenanigans >:)
    # start playback_worker, it will wait until something is added to the playback queue
    pb_proc = mp.Process(target=playback_worker, args=(playback_queue,), daemon=True)
    pb_proc.start()

    # start n render_workers
    procs = []
    for i in range(num_workers):
        # render_worker() args
        worker_algo = graph_algos[random.randint(0, len(graph_algos))] if is_random else algo
        args = (i,worker_algo,playback_queue,conf_template,cmd_args.size)
        p = mp.Process(target=render_worker, args=args, daemon=True)
        # create a callback when proc finishes to start new render_worker?
        p.start()
        time.sleep(1)   # don't remove this, there's a race condition in manim when creating mobjects
        procs.append(p)
    
    # let threads run until time limit
    while is_infinite or uptime() < max_runtime:
        if not is_infinite:
            time.sleep(max_runtime - uptime())

    # join render workers for graceful shutdown?
    print('joining procs: ')
    for i in range(len(procs)):
        p = procs[i]
        p.join()
        print('proc ' + str(i) + ' finished')
    pb_proc.terminate() 

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
                        default=False,
                        help='Generate animations indefinitely')
    # currently just changes the number of workers
    # since workers only make one animation
    parser.add_argument('--num-animations', type=int, 
                        default=4,
                        help='Number of animations to generate')
    # doesn't do anything yet
    # a set data structure should restrict this?
    parser.add_argument('-r', '--random', type=bool, 
                        default=False,
                        help='Generate a random animation')
    parser.add_argument('-ds', '--data-structure', type=str, 
                        default='graph', choices=['graph'],
                        help='Data structure to generate animations on')
    parser.add_argument('-rt', '--runtime', type=int, 
                        default=60,
                        help='Maximum runtime of the program in seconds')
    return parser.parse_args()

def init():
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

def render_worker(num, algo, playback_queue, conf, ds_size):
    """Render a scene and add it to playback queue"""

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

    # add playback command to queue
    open_cmd = [os_open]
    open_cmd.append(scene_path + fname)
    playback_queue.put(open_cmd)    

def playback_worker(playback_queue):
    """Play videos in the playback queue"""
    # TODO find a way to play next vid w/o starting a new proc
    import json

    while True:
        open_cmd = playback_queue.get()
        print('playback open_cmd ', open_cmd)
        sp.Popen(open_cmd)  # play rendered scene
        filename = open_cmd[1]
        result = sp.check_output(
            f'ffprobe -v quiet -show_streams -select_streams v:0 -of json "{filename}"',
            shell=True).decode()
        fields = json.loads(result)['streams'][0]
        duration = fields['duration']
        time.sleep(float(duration)) # wait until scene is finished playing

def uptime():
    """Returns the number of seconds the program has been running"""
    return time.time() - start_time

if __name__ == "__main__":
    main()
