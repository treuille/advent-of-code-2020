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
        r"(?P<low>\d+)\-(?P<hi>\d+) (?P<char>[a-z]): (?P<pw>[a-z]+)$")
for line_num, line in enumerate(problem_input.split("\n")):
    match = line_expression.match(line)
    if not match:
        st.warning(f'Line `{line_num}`: Parse error `"{line}"`')
        continue
    low = int(match.group("low"))
    hi = int(match.group("hi"))
    char = match.group("char")
    pw = match.group("pw")
    char_count = len([c for c in pw if c == char])
    if show_debug_output:
        st.write(f'Line `{line_num}`: `"{line}"`')
        st.write(low, hi, char, pw)
    if low <= char_count <= hi:
        valid_input_lines += 1
        if show_debug_output:
            st.success(f"Line `{line_num}` valid (`{valid_input_lines}`).")
    elif show_debug_output:
        st.error(f"Line `{line_num}` invalid (`{valid_input_lines}`).")
st.write(f"In total `{valid_input_lines}` lines are valid.")
