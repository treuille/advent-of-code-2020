import streamlit as st
from streamlit_ace import st_ace

"""
# Advent of Code 2020 in Streamlit - 01
"""

"""
## Input
"""

# Load the input
problem_input = st_ace()

# Parse it into a an array of integers.
problem_input = [int(line) for line in problem_input.split('\n') if line]
st.write(problem_input)

# Solve the problem
for i in range(len(problem_input)):
    x = problem_input[i]
    for j in range(i+1, len(problem_input)):
        y = problem_input[j]
        for k in range(j+1, len(problem_input)):
            z = problem_input[k]
            if x + y + z == 2020:
                st.write(f"The answer is `{x} * {y} * {z} = {x * y * z}`")
                st.stop()
st.warning("No answer could be found.")
