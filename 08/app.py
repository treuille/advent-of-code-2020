import streamlit as st
from streamlit_ace import st_ace
import re
from typing import List, Tuple, Set

"""
# Advent of Code 2020 in Streamlit - *PROBLEM*
"""

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")

# Parse the input
INSRUCTION = re.compile(r"(?P<inst>acc|jmp|nop) (?P<sign>\-|\+)(?P<arg>\d+)")
instructions : List[Tuple[str, int]] = []
for line_num, line in enumerate(problem_input.split("\n")):
    match = INSRUCTION.match(line)
    assert match, f'Parse error: "{line}"'
    arg = int(match.group('arg'))
    if match.group('sign') == '-':
        arg *= -1
    instructions.append((match.group('inst'), arg))
    if show_debug_output:
        st.write(f'`{line_num}`: line=`"{line}"`')
        st.write(f'`{line_num}`: instruction=`"{instructions[-1]}"`')
        st.write("---")

# Execute the program
if show_debug_output:
    st.write("## Executing")
executed : Set[int] = set()
line_num = 0
accumulator = 0
while line_num not in executed:
    executed.add(line_num)
    inst, arg = instructions[line_num]
    if show_debug_output:
        st.write(line_num, inst, arg, accumulator)
        st.write("---")
    if inst == "nop":
        line_num += 1
    elif inst == "acc":
        accumulator += arg
        line_num += 1
    elif inst == "jmp":
        line_num += arg

f"""
## Output

The final value of the accumulator is `{accumulator}`.
"""

