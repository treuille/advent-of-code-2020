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

"""
## Output
"""

for line_num, line in enumerate(problem_input.split('\n')):
    if show_debug_output:
        st.write(f'`{line_num}`: `"{line}"`')
