import streamlit as st
from streamlit_ace import st_ace

"""
# Advent of Code 2020 in Streamlit - 03
"""

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")
show_simple_debug_output = st.checkbox("Show simple debug output")

"""
## Output
"""

modes = [
    ("Right 1, down 1.", 1, 1),
    ("Right 3, down 1.", 3, 1),
    ("Right 5, down 1.", 5, 1),
    ("Right 7, down 1.", 7, 1),
    ("Right 1, down 2.", 1, 2),
]

product = 1
for mode, right, down in modes:
    x_pos = 0
    trees_hit = 0
    for line_num, line in enumerate(problem_input.split('\n')):
        if down == 2 and line_num % 2 == 1:
            continue
        if line[x_pos % len(line)] == '#':
            trees_hit += 1
        if show_debug_output:
            st.write(f'`{line_num}`: line=`"{line}"`')
            st.write(f'`{line_num}`: x_pos=`x_pos`')

        if show_simple_debug_output:
            line_array = [c for c in line]
            if line[x_pos % len(line)] == '#':
                line_array[x_pos % len(line)] = 'O'
            else:
                line_array[x_pos % len(line)] = 'X'

            st.write(f"`{''.join(line_array)}`")
        x_pos += right
    st.write(f"Hit {trees_hit} trees in mode '{mode}'.")
    product *= trees_hit
st.write(f"Product: `{product}`")
