import streamlit as st
from streamlit_ace import st_ace
import functools

"""
# Advent of Code 2020 in Streamlit - 06
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

yes_sum = 0
for group_num, group in enumerate(problem_input.split('\n\n')):
    responses = [set(response) for response in group.split('\n')]
    yesses = functools.reduce(set.intersection, responses)
    if show_debug_output:
        st.write(responses)
        st.write(yesses)
        st.write(len(yesses))
        st.write('---')
    yes_sum += len(yesses)
st.write("sum:", yes_sum)
