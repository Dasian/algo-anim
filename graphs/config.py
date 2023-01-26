"""
	List of custom config values
"""
from manim.utils.color import Colors

# states for nodes/edges of a graph
class GraphState(Enum):
	DEFAULT = 0
	QUEUED = 1
	PROCESS = 2
	VISITED = 3
	CHECK = 4
	FOUND = 5
	START = 6
	END = 7

state_colors = {
	GraphState.DEFAULT: Colors.light_gray.value,
	GraphState.QUEUED: Colors.blue_d.value ,
	GraphState.PROCESS: Colors.purple_d.value ,
	GraphState.VISITED: Colors.yellow_b.value ,
	GraphState.CHECK: Colors.maroon_b.value ,
	GraphState.FOUND: Colors.green_d.value ,
	GraphState.START: Colors.pure_green.value ,
	GraphState.END: Colors.pure_red.value
}