import streamlit as st
from streamlit_ace import st_ace
import re
from typing import List, Tuple, Set, Dict, Optional
import functools

"""
# Advent of Code 2020 in Streamlit - 08
"""

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_parse_ouput = st.checkbox("Show parse output")
show_preprocess_output = st.checkbox("Show preprocess output")
show_debug_output = st.checkbox("Show debug output")

# Types
Instruction = Tuple[str, int]
Instructions = List[Instruction]
Antecedents = Dict[int, Set[int]]

# Parse the input
INST_RE = re.compile(r"(?P<inst>acc|jmp|nop) (?P<sign>\-|\+)(?P<arg>\d+)")
instructions: Instructions = []
for line_num, line in enumerate(problem_input.split("\n")):
    match = INST_RE.match(line)
    assert match, f'Parse error: "{line}"'
    arg = int(match.group('arg'))
    if match.group('sign') == '-':
        arg *= -1
    instructions.append((match.group('inst'), arg))
    if show_parse_ouput:
        st.write(f'`{line_num}`: line=`"{line}"`')
        st.write(f'`{line_num}`: instruction=`"{instructions[-1]}"`')
        st.write("---")

def execute(instructions: Instructions) -> int:
    """Execute the program and return the accumulator."""
    if show_debug_output:
        st.write("## Executing")
    executed: Set[int] = set()
    line_num = 0
    accumulator = 0
    while line_num not in executed:
        if show_debug_output:
            st.write("Line number:", line_num)
        if line_num == len(instructions):
            return accumulator
        executed.add(line_num)
        inst, arg = instructions[line_num]
        if show_debug_output:
            st.write(inst, arg, accumulator)
            st.write("---")
        if inst == "nop":
            line_num += 1
        elif inst == "acc":
            accumulator += arg
            line_num += 1
        elif inst == "jmp":
            line_num += arg
        else:
            raise RuntimeError(f'Unkown instruction: "{inst}"')
    return accumulator

def add_antecedent(antecedents: Antecedents, line: int, next_line: int):
    """Adds an antecedent line to the antecedents lookup table."""
    antecedent_lines = antecedents.setdefault(next_line, set())
    antecedent_lines.add(line)

def get_all_antecedents(antecedents: Antecedents, lines: Set[int]):
    """Returns all lines antecedent to this set of lines."""
    antecedent_lines: Set[int] = set()
    for line in lines:
        antecedent_lines |= antecedents.get(line, set())
    return antecedent_lines

def get_antecedents(instructions: Instructions) -> Antecedents:
    """Get a graph of all the antecedents to each line"""

    # Compute the antecedent lines that lead to each line
    antecedents: Antecedents = {}
    for line_num, (inst, arg) in enumerate(instructions):
        if inst == "nop":
            add_antecedent(antecedents, line_num, line_num + 1)
        elif inst == "acc":
            add_antecedent(antecedents, line_num, line_num + 1)
        elif inst == "jmp":
            add_antecedent(antecedents, line_num, line_num + arg)
        else:
            raise RuntimeError(f'Unknown instruction: "{inst}"')
        if show_preprocess_output:
            with st.beta_expander(f"Show ouput for line {line_num}"):
                st.write(line_num, inst, arg)
                col1, col2 = st.beta_columns(2)
                col1.write("### Antecedents")
                col1.write({x:repr(y) for x,y in antecedents.items()})
                st.write("---")
    return antecedents

def get_terminating_lines(antecedents: Antecedents) -> Set[int]:
    """Returns a set of all lines which will eventually terminate without
    flipping instructions."""

    # Peform a breadth-first search to find all instructions that terminate
    terminating_lines: Set[int] = set()
    highest_line = max(max(lines) for lines in antecedents.values())
    lines_to_process = { highest_line + 1 }
    while lines_to_process:
        terminating_lines |= lines_to_process
        lines_to_process = get_all_antecedents(antecedents, lines_to_process)
        if show_debug_output:
            st.write("### Terminating lines")
            st.write(terminating_lines)
            st.write("### Lines to process")
            st.write(lines_to_process)
            st.write("---")
    return terminating_lines

def fix_instructions(instructions: Instructions, terminating_lines: Set[int]) \
        -> None:
    """Flips a single instruction so that the instructions terminate."""
    # Start executing from the beginning, seeing where we can flip an
    # an instruction.
    line_num = 0
    executed: Set[int] = set()
    while line_num not in executed:
        if line_num == len(instructions):
            raise RuntimeError("Program terminated while fixing instructions.")
        executed.add(line_num)
        inst, arg = instructions[line_num]
        if show_debug_output:
            st.write(line_num, inst, arg)
            st.write(line_num + 1, (line_num + 1) in terminating_lines)
            st.write(line_num + arg, (line_num + arg) in terminating_lines)
            st.write("---")

        if inst == "nop":
            if line_num + arg in terminating_lines:
                instructions[line_num] = "jmp", arg
                st.warning(
                    f"Changed line `{line_num}` to "
                    f"`{instructions[line_num]}`")
                return
            line_num += 1
        elif inst == "acc":
            line_num += 1
        elif inst == "jmp":
            if line_num + 1 in terminating_lines:
                instructions[line_num] = "nop", arg
                st.warning(
                    f"Changed line `{line_num}` to "
                    f"`{instructions[line_num]}`")
                return
            line_num += arg
        else:
            raise RuntimeError(f'Unkown instruction: "{inst}"')
    raise RuntimeError("Program looped while fixing instructions.")
 

# Run the ouput
"## Fixing instructions"
antecedents = get_antecedents(instructions)
terminating_lines = get_terminating_lines(antecedents)
fix_instructions(instructions, terminating_lines)

"""
## Output
"""

accumulator = execute(instructions)

f"""
The final value of the accumulator is `{accumulator}`.
"""

