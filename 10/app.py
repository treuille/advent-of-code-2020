import streamlit as st
from streamlit_ace import st_ace
from typing import Dict

"""
# Advent of Code 2020 in Streamlit - 10
"""

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")

adapters = [int(line) for line in problem_input.split('\n')]
st.write(adapters)
adapters.sort()
adapters = [0] + adapters + [adapters[-1] + 3]
st.write(adapters)

difference_counts: Dict[int, int] = {}
for j in range(1, len(adapters)):
    i = j - 1
    difference = adapters[j] - adapters[i]
    n_diff = difference_counts.get(difference, 0)
    difference_counts[difference] = n_diff + 1

"## Output"

st.write(difference_counts)
st.write(difference_counts[1] * difference_counts[3])
