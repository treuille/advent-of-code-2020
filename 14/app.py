import streamlit as st
from streamlit_ace import st_ace
from typing import Dict
import re

"""
# Advent of Code 2020 in Streamlit - 14
"""

# Types
Memory = Dict[int, int]

# Utility functions
def sep_by_10s(s):
    """Insert a period every ten characters, starting from the back."""
    # return s
    t = ""
    for i, c in enumerate(reversed(s)):
        t += c
        if i % 10 == 9:
            t += '.'
    return ''.join(reversed(t))
        
def write_binary(x, metadata):
    """Writes out a number in binary and adds some medatadata"""
    # Only write if debug output is turned on
    if not show_debug_output:
        return

    # Convert the number to a binary representation
    if type(x) == int:
        bin_repr = bin(x)[2:]
        bin_repr = '0' * (36 - len(bin_repr)) + bin_repr
    elif type(x) == str:
        bin_repr = x
    assert len(bin_repr) == 36, "String length must be 36."

    # Add a little counter below for reference
    counter = ''.join(reversed([str(x % 10) for x in range(36)]))

    # All done!
    st.text(f"{sep_by_10s(bin_repr)} {metadata}\n{sep_by_10s(counter)}")

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")

"""
## Output
"""

memory: Memory = {}
assigmnet_expr = re.compile(r"mem\[(?P<loc>\d+)\] = (?P<val>\d+)$")
for line_num, line in enumerate(problem_input.split('\n')):
    # If in debug mode, show the line.
    if show_debug_output:
        st.write(f'`{line_num}`: line=`"{line}"`')

    # Parse a mask update line 
    if line.startswith("mask"):
        mask = line[7:]
        write_binary(mask, f"(new mask) line={line_num}")
        continue

    # Parse a memory assignment line
    match = assigmnet_expr.match(line)
    assert match, f'Unable to parse line {line_num}: "{line}"'
    loc = int(match.group("loc"))
    val = int(match.group("val"))

    write_binary(loc, f"loc={loc} line={line_num}")

    # Update the value with the mask
    locs = [0]
    for bit, constraint in enumerate(reversed(mask)):
        if constraint == "0":
            locs = [new_loc | (loc & (1 << bit)) for new_loc in locs]
        elif constraint == "1":
            locs = [new_loc | (1 << bit) for new_loc in locs]
        elif constraint == "X":
            locs_2 = [new_loc | (1 << bit) for new_loc in locs]
            locs.extend(locs_2)
        else:
            raise RuntimeError(f"Unknown constraint '{constraint}'")
    for loc in locs:
        memory[loc] = val
        write_binary(loc, f"<- {val} (loc={loc})")

if show_debug_output:
    st.write('The memory:', memory)
st.write("The answer:", sum(memory.values()))
