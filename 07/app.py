import streamlit as st
from streamlit_ace import st_ace
from typing import Dict, Set, Match, cast
import re
import functools

"""
# Advent of Code 2020 in Streamlit - 07
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

BAG_RE = re.compile(r"\d+\ (?P<bag_type>[a-z]+ [a-z]+) bags?\.?$")

contained_by : Dict[str, Set[str]] = {}
for line_num, line in enumerate(problem_input.split('\n')):
    container, containees = line.split(" bags contain ")
    if containees == "no other bags.":
        containees = []
    else:
        containees = [cast(Match[str], BAG_RE.match(s)).group("bag_type")
            for s in containees.split(", ")]
    for containee in containees:
        containers = contained_by.setdefault(containee, set())
        containers.add(container)
    if show_debug_output:
        st.write(f'`{line_num}`: line=`"{line}"`')
        st.write(f'`{line_num}`: container=`"{container}"`')
        st.write(f'`{line_num}`: containees=`{containees}`')
        st.write(repr(contained_by))
        st.write('---')

# Perform a breadth-first search to figure out which bag eventually contain
# a shiny gold bag
eventual_containers = contained_by["shiny gold"]
# st.help(set.union)
while True:
    if show_debug_output:
        st.write(eventual_containers)
    new_eventual_containers = eventual_containers.copy()
    for bag in eventual_containers:
        new_eventual_containers |= contained_by.get(bag, set())
    if show_debug_output:
        st.write(new_eventual_containers)
        st.write('---')
    if len(eventual_containers) == len(new_eventual_containers):
        break
    eventual_containers = new_eventual_containers
st.write(f"There are `{len(eventual_containers)}` eventual containers.")
st.write(list(eventual_containers))
