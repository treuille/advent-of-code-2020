import streamlit as st
from streamlit_ace import st_ace
from typing import Dict, List

"""
# Advent of Code 2020 in Streamlit - 10
"""

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")

# Get the adapters in a nice sorted order
adapters = [int(line) for line in problem_input.split('\n')]
st.write(adapters)
adapters.sort()
adapters = [0] + adapters + [adapters[-1] + 3]
st.write(adapters)

def count_chains(adapters: List[int]) -> int:
    """Count the number of chains that get from source to sink."""
    num_adapters = len(adapters)
    if num_adapters < 2:
        return 0
    elif num_adapters == 2:
        if adapters[1] - adapters[0] <= 3:
            return 1
        else:
            return 0

    # The general case is 3 or more adapters. First, partition into 3.
    midpoint = len(adapters) // 2
    adapters_1 = adapters[:midpoint]
    adapters_2 = [ adapters[midpoint] ]
    adapters_3 = adapters[midpoint + 1:]

    # Count all chains that contain the midpoint.
    num_chains = (count_chains(adapters_1 + adapters_2) *
        count_chains(adapters_2 + adapters_3))

    # Count all chains that do not contain the midpoint.
    if adapters_3[0] - adapters_1[-1] <= 3:
        num_chains += count_chains(adapters_1 + adapters_3)

    # Done
    return num_chains


"## Output"

st.write(count_chains(adapters))
