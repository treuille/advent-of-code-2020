import streamlit as st
from streamlit_ace import st_ace
from typing import Tuple, Set, cast

"""
# Advent of Code 2020 in Streamlit - 09
"""

# Types
Point = Tuple[int, int, int, int]
Points = Set[Point]

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")

def get_initial_state(problem_input: str) -> Points:
    """Parses the program input and returns the intial state of the program."""
    state: Points = set()
    for y, line in enumerate(problem_input.split('\n')):
        for x, char in enumerate(line):
            if char == "#":
                state.add((x, y, 0, 0))
    return state

def pretty_print_points(points: Points) -> None:
    """Writes the points out to the console as a series of dataframe."""
    # Sort the points by z values
    xs, ys, zs, ws = cast(Tuple[Set[int], Set[int], Set[int], Set[int]],
            map(set, zip(*points)))
    for w in range(min(ws), max(ws) + 1):
        for z in range(min(zs), max(zs) + 1):
            st.write(f"**z = `{z}` w = `{w}`**")
            z_slice = "" 
            for y in range(min(ys), max(ys) + 1):
                line = ''.join(['.', '#'][int((x, y, z) in points)]
                        for x in range(min(xs), max(xs) + 1))
                z_slice += line + '\n'
            st.text(z_slice)

def get_neighbors(point: Point) -> Points:
    """Returns the 26 adjacent points in 3D."""
    px, py, pz, pw = point
    return set((x, y, z, w)
            for x in range(px - 1, px + 2)
            for y in range(py - 1, py + 2)
            for z in range(pz - 1, pz + 2)
            for w in range(pw - 1, pw + 2)
            if (x != px or y != py or z != pz or w != pw))

def get_all_neighbors(points: Points) -> Points:
    """Like get_neighbors() but unions over a set of points."""
    all_neighbors: Points = set()
    for point in points:
        all_neighbors |= get_neighbors(point)
    return all_neighbors


def cycle(state: Points) -> Points:
    """Implements the simulation one timestep into the future."""
    new_state: Points = set()
    for point in get_all_neighbors(state):
        active_neigbors = len(get_neighbors(point).intersection(state))
        if point in state:
            # If a cube is active and exactly 2 or 3 of its neighbors are also
            # active, the cube remains active. Otherwise, the cube becomes
            # inactive.
            if active_neigbors in (2, 3):
                new_state.add(point)
        else:
            # If a cube is inactive but exactly 3 of its neighbors are active,
            # the cube becomes active. Otherwise, the cube remains inactive.
            if active_neigbors == 3:
                new_state.add(point)
    return new_state

def run_simulation(state: Points, n_iters: int) -> Points:
    for iteration in range(n_iters):
        state = cycle(state)
        if show_debug_output:
            with st.beta_expander(f"After `{iteration + 1}` cycles"):
                pretty_print_points(state)
                st.write(f"There are `{len(state)}` cubes.")
    return state

state = get_initial_state(problem_input)
state = run_simulation(state, 6)

"""
## Output
"""

st.write(f"There are `{len(state)}` cubes.")

