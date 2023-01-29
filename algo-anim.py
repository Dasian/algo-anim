"""
	Delegates animation rendering to multiple processes
	Keeps track of animation queue
	Main program for running all of this
"""
from graphs.scenes import *
import platform
import subprocess as sp
from manim import *
import multiprocessing as mp
import time

def main():
	# TODO add cmd flags
	# --ds --data-structure = ["graph", "array"]
	# --inf --infinite
	# --nw --num_workers [num]
	# --a --algo = ["BFS, "DFS", "sort", "insertion-sort"]
	init()

	# TODO user controlled input
	global is_infinite
	global start_time
	num_workers = 2
	algo = "BFS"
	is_infinite = False
	start_time = time.time()
	max_runtime = 60 	# in seconds

	# Note: you can't have a playlist using xdg-open
	playback_queue = mp.Queue()

	# multiprocessing shenanigans >:)
	# start playback_worker, it will wait until something is added to the playback queue
	pb_proc = mp.Process(target=playback_worker, args=(playback_queue,), daemon=True)
	pb_proc.start()

	# start n render_workers
	procs = []
	for i in range(num_workers):
		p = mp.Process(target=render_worker, args=(i,algo,playback_queue,conf_template), daemon=True)
		# callback when proc finishes to start new render_worker?
		p.start()
		time.sleep(1)	# don't remove this, there's a race condition in manim when creating mobjects
		procs.append(p)
	
	# let threads run until time limit
#	while is_infinite or uptime() < max_runtime:
#		if not is_infinite:
#			time.sleep(max_runtime - uptime())

	# join render workers for graceful shutdown?
	print('joining procs: ')
	for i in range(len(procs)):
		p = procs[i]
		p.join()
		print('proc ' + str(i) + ' finished')
	

def init():
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
	quality = '480p15/'	# /1080p60
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
		"output_file": 'tmp',	# will be replaced with the filename
		"media_dir": media_dir,	# changes based on os
		"verbosity": "WARNING",
		"partial_movie_dir": "{video_dir}/partial_movie_files/"
	}

def render_worker(num, algo, playback_queue, conf):
	"""Render a scene and add it to playback queue"""

	fname = algo.upper() + str(num) + ext
	conf["output_file"] = fname
	conf["partial_movie_dir"] = "{video_dir}/partial_movie_files/" + algo.upper() + str(num)

	# TODO use a dict to make scene object
	scene = None
	with tempconfig(conf):
		if algo.upper() == "BFS":
			scene = BFS()
		else:
			raise("'" + algo + "'" + " is not a supported algorithm")

		scene.render()

	open_cmd = [os_open]
	open_cmd.append(scene_path + fname)
	playback_queue.put(open_cmd)	

def playback_worker(playback_queue):
	"""Play videos in the playback queue"""
	# TODO find a way to play next vid w/o starting a new proc
	print('playback starting')

	open_cmd = playback_queue.get()
	while open_cmd != None: 
		print('playback open_cmd ', open_cmd)
		sp.Popen(open_cmd)
		# TODO wait until playback is finished
		open_cmd = playback_queue.get()

	# queue is empty here with no more render workers
	print('playback ending')

def uptime():
	"""Returns the number of seconds the program has been running"""
	return time.time() - start_time

if __name__ == "__main__":
	main()
