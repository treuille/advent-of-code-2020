import streamlit as st
from streamlit_ace import st_ace
import re
from typing import List, Tuple, Set, Dict, Optional
import functools

"""
# Advent of Code 2020 in Streamlit - *PROBLEM*
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

def fix_instructions(instructions: Instructions) -> None:
    """Fixes the instrutions so that they don't loop infinitely."""

    # Compute the antecedent lines that lead to each line
    antecedents: Antecedents = {}
    flip_antecedents: Antecedents = {}
    for line_num, (inst, arg) in enumerate(instructions):
        if inst == "nop":
            add_antecedent(antecedents, line_num, line_num + 1)
            add_antecedent(flip_antecedents, line_num, line_num + arg)
        elif inst == "acc":
            add_antecedent(antecedents, line_num, line_num + 1)
        elif inst == "jmp":
            add_antecedent(antecedents, line_num, line_num + arg)
            add_antecedent(flip_antecedents, line_num, line_num + 1)
        else:
            raise RuntimeError(f'Unknown instruction: "{inst}"')
        if show_preprocess_output:
            with st.beta_expander(f"Show ouput for line {line_num}"):
                st.write(line_num, inst, arg)
                col1, col2 = st.beta_columns(2)
                col1.write("### Antecedents")
                col1.write({x:repr(y) for x,y in antecedents.items()})
                col2.write("### Flip Antecedents")
                col2.write({x:repr(y) for x,y in flip_antecedents.items()})
                st.write("---")

    # Peform a breadth-first search to find all instructions that terminate
    terminating_lines: Set[int] = set()
    lines_to_process = {len(instructions)}
    while lines_to_process:
        terminating_lines |= lines_to_process
        if show_debug_output:
            st.write("### Terminating lines")
            st.write(terminating_lines)
        if 0 in terminating_lines:
            st.success(
                f"This program terminates on lines `{terminating_lines}`.")
            return
        antecedent_lines = get_all_antecedents(antecedents, lines_to_process)
        if not antecedent_lines:
            # Figure out which instruction to flip. Hopefully only one!
            flip_antecedent_lines = \
                get_all_antecedents(flip_antecedents, lines_to_process)
            st.warning(
                f"No antecedent lines to `{lines_to_process}`.\n\n"
                f"Flip antecedents are `{flip_antecedent_lines}`.\n\n"
                f"Terminating lines are `{terminating_lines}`. "
            )
            assert len(flip_antecedent_lines) == 1, \
                "Too many potential lines to flip here."

            # Actually flip the instruction.
            line_to_flip = list(flip_antecedent_lines)[0]
            inst, arg = instructions[line_to_flip]
            if inst == "nop":
                instructions[line_to_flip] = ("jmp", arg)
            elif inst == "jmp":
                instructions[line_to_flip] = ("nop", arg)
            else:
                raise RuntimeError(f'Unknown instruction: "{inst}"')
            st.success(f"Flipped instruction on line `{line_to_flip}`")
            return
            
        lines_to_process = antecedent_lines
        if show_debug_output:
            st.write("### Lines to process")
            st.write(lines_to_process)
            st.write("---")
        if not antecedent_lines:
            raise RuntimeError("Reached a dead end here")

# Run the ouput
"# Fixing the instructions"
fix_instructions(instructions)

"# Running on fixed instructions"
fix_instructions(instructions)

"# Executing the program"
accumulator = execute(instructions)
f"""
## Output

The final value of the accumulator is `{accumulator}`.
"""

