"""
	Delegates animation tasks to threads
	Keeps track of animation queue
	Main program for running all of this
"""
import vlc

def main():
	# TODO add cmd flags
	# --ds --data-structure = ["graph", "array"]
	# --inf -- infinite
	# --ql --queue-length [num]

	# temp behavior, run bfs
	# how to process manim scene in python?	
	player = vlc.MediaPlayer()
	media = vlc.Media("file.mkv")
	player.set_media(media)
	player.play()

	# get fullscreen status ? true or false thing?
	fs = player.get_fullscreen()

	# TODO animation queue
	anim_queue = []

	return

if __name__ == "__main__":
	main()
