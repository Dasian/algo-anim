"""
	List of custom config values
"""

import Colors

# Process node
# when done processing,
# the node is visited
# The process state
# should be the current
# working position
class GraphState(Enum):
	DEFAULT = 0
	QUEUED = 1
	PROCESS = 2
	VISIT = 3
	FOUND = 4
	START = 5
	END = 6

# try to figure out what
# states you need and
# what color to set them
# (make changing color
# easy for the user)
