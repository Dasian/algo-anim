"""
	Delegates animation tasks to threads
	Keeps track of animation queue
	Main program for running all of this
"""
from graphs.scenes import *
import platform
import subprocess as sp
from manim import *
import threading

def main():
	# TODO add cmd flags
	# --ds --data-structure = ["graph", "array"]
	# --inf -- infinite
	# --ql --queue-length [num]
	# --a --algo = ["BFS, "DFS", "sort", "insertion-sort"]

	# os specific init
	curr_os = platform.system()
	media_dir = ''
	open_cmd = []

	if curr_os == 'Linux':
		open_cmd.append('xdg-open')
		media_dir = '/tmp/algo-anim'
	elif curr_os == 'Windows':
		open_cmd.append('cygstart')
	elif curr_os == 'Darwin':
		open_cmd.append('open')

	scene_path = media_dir + 'videos/'
	quality = '480p15/'	# /1080p60

	# play
	scene_path += quality
	open_cmd.append(scene_path + scene_name + '.mp4')
	sp.Popen(open_cmd)

	# TODO implement manim render settings
	# aspect_ratio, quality, media_dir, movie_file_extension
	# output_file, scene_names, window_position, window_size
	# write_to_movie, force_window
	tmp_config = {
		"quality": "low_quality",
		"disable_caching": True,
		"output_file": 'tmp',	# will be replaced with the filename
		"media_dir": media_dir	# changes based on os
	}

	# TODO threads + signal render completion
	anim_queue = []
	for i in range(3):
		scene_name = 'bfs' + str(i)
		tmp_config["output_file"] = scene_name
		with tempconfig(tmp_config):
			threading.Thread(target=thread_render, args=(i,), daemon=True)

			# when scene is finished rendering, add it to play queue
			play(scene_name)


def thread_render(num):
	scene = BFS()
	scene.render()
	fname = 'bfs' + str(i)
	return fname

if __name__ == "__main__":
	main()
