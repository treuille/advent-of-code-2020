import streamlit as st
from streamlit_ace import st_ace
import re

"""
# Advent of Code 2020 in Streamlit - 02
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

valid_input_lines = 0
line_expression = re.compile(
        r"(?P<pos_1>\d+)\-(?P<pos_2>\d+) (?P<char>[a-z]): (?P<pw>[a-z]+)$")
for line_num, line in enumerate(problem_input.split("\n")):
    match = line_expression.match(line)
    if not match:
        st.warning(f'Line `{line_num}`: Parse error `"{line}"`')
        continue
    pos_1 = int(match.group("pos_1"))
    pos_2 = int(match.group("pos_2"))
    char = match.group("char")
    pw = match.group("pw")
    if show_debug_output:
        st.write(f'Line `{line_num}`: `"{line}"`')
        st.write(pos_1, pos_2, char, pw)
        st.write(f"Testing `'{pw[pos_1 - 1]}'` and `'{pw[pos_2 - 1]}'`")
    char_matches = 0
    if pw[pos_1 - 1] == char:
        char_matches += 1
    if pw[pos_2 - 1] == char:
        char_matches += 1
    if char_matches == 1:
        valid_input_lines += 1
        if show_debug_output:
            st.success(f"Line `{line_num}` valid (`{valid_input_lines}`).")
    elif show_debug_output:
        st.error(f"There were `{char_matches}` matches")
        st.error(f"Line `{line_num}` invalid (`{valid_input_lines}`).")
st.write(f"In total `{valid_input_lines}` lines are valid.")
