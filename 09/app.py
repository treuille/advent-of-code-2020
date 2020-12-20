import streamlit as st
from streamlit_ace import st_ace
from typing import List, Tuple

"""
# Advent of Code 2020 in Streamlit - 09
"""

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
preamble_len = st.selectbox("Preamble length", [5, 25])
show_debug_output = st.checkbox("Show debug output")

# Parse the input

# Check the input
@st.cache
def get_invalid_entry(msg: List[int], preamble_len: int) -> int:
    """Searches for an invalid entry as defined in the problem."""
    for line_num in range(preamble_len, len(msg)):
        valid = False
        target = msg[line_num]
        preamble = msg[line_num - preamble_len : line_num]
        for candidate in preamble:
            if (target - candidate) in preamble:
                if show_debug_output:
                    st.write(line_num, ":", candidate, "and",
                        target - candidate, "in", preamble)
                valid = True
                break
        if not valid:
            return target
            break
    raise RuntimeError("Unable to find an invalid entry.")

@st.cache
def find_subsequence(msg: List[int], target: int) -> Tuple[int, int]:
    """Find a pair of indices such that when we sum through these messages
    (inclusively), we achieve the given target."""
    i, j = 0, 1
    while j < len(msg):
        seq_sum = sum(msg[i : j+1])
        if seq_sum == target:
            return i, j
        if seq_sum < target:
            j += 1
        elif i + 1 == j:
            i += 1
            j += 1
        else:
            i += 1
    raise RuntimeError(f"Unable to find a subsequence summing to {target}.")

"""
## Output
"""

msg = [int(line) for line in problem_input.split('\n')]
invalid_entry = get_invalid_entry(msg, preamble_len)
st.warning(f"Message `{invalid_entry}` is invalid.")
i, j = find_subsequence(msg, invalid_entry)
subsequence = msg[i : j+1]
st.write(i, j, sum(subsequence), min(subsequence) + max(subsequence))
