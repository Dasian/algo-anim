"""
	List of custom config values
"""
from manim.utils.color import manim_colors
from enum import Enum

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
	GraphState.DEFAULT: manim_colors.LIGHT_GRAY,
	GraphState.QUEUED: manim_colors.BLUE_D,
	GraphState.PROCESS: manim_colors.PURPLE_D,
	GraphState.VISITED: manim_colors.YELLOW_B,
	GraphState.CHECK: manim_colors.MAROON_B,
	GraphState.FOUND: manim_colors.GREEN_D,
	GraphState.START: manim_colors.PURE_GREEN,
	GraphState.END: manim_colors.PURE_RED
}
