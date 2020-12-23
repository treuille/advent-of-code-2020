import streamlit as st
from streamlit_ace import st_ace
import math

"""
# Advent of Code 2020 in Streamlit - 12
"""

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")

"""
## Output
"""

# The starting location
x, y = 0, 0

# The waypoint's relative location
wx, wy = 10, 1

for line_num, line in enumerate(problem_input.split('\n')):
    if show_debug_output:
        st.write(f'`{line_num}`: line=`"{line}"`')
        st.write(f'`{line_num}`: pos=`"{(x, y)}"`')
        st.write(f'`{line_num}`: dir=`"{(wx, wy)}"`')
        st.write("---")

    # Action N means to move north by the given value.
    # Action S means to move south by the given value.
    # Action E means to move east by the given value.
    # Action W means to move west by the given value.
    if line[0] == 'N':
        wy += int(line[1:])
    elif line[0] == 'S':
        wy -= int(line[1:])
    elif line[0] == 'E':
        wx += int(line[1:])
    elif line[0] == 'W':
        wx -= int(line[1:])

    # Action L means to turn left the given number of degrees.
    # Action R means to turn right the given number of degrees.
    elif line in ('L90', 'R270'):
        wx, wy = -wy, wx
    elif line in ('R90', 'L270'):
        wx, wy = wy, -wx
    elif line in ('R180', 'L180'):
        wx, wy = -wx, -wy
    
    # Action F means to move forward by the given value in the direction the
    # ship is currently facing.
    elif line[0] == 'F':
        x += wx * int(line[1:])
        y += wy * int(line[1:])

    else:
        raise RuntimeError(f'Cannot parse: "{line}"')

# Print the final state
f"""
pos=`"{(x, y)}"`
dir=`"{(wx, wy)}"`
dist=`"{int(math.fabs(x) + math.fabs(y))}"`
"""
