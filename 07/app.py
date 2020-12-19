import streamlit as st
from streamlit_ace import st_ace
from typing import Dict, Set, Match, cast, List, Tuple
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

# Parse the input

BAG_RE = re.compile(r"(?P<num_bags>\d+)\ (?P<bag_type>[a-z]+ [a-z]+) bags?\.?$")
Bags = Dict[str, int]

contains : Dict[str, Bags] = {}
for line_num, line in enumerate(problem_input.split('\n')):
    container_bag_type, containees_str = line.split(" bags contain ")
    containees : List[Tuple[str, int]] = []
    if containees_str != "no other bags.":
        for containee in containees_str.split(", "):
            match = BAG_RE.match(containee)
            assert match, f'Regular expression parse error: "{containee}".'
            containees.append((match.group("bag_type"),
                int(match.group("num_bags"))))
    assert container_bag_type not in contains, f'Repeat bag type on {line_num}.'
    contains[container_bag_type] = dict(containees)
    if show_debug_output:
        st.write(f'`{line_num}`: line=`"{line}"`')
        st.write(f'`{line_num}`: container_bag_type=`"{container_bag_type}"`')
        st.write(f'`{line_num}`: containees=`{containees}`')
        st.write(contains)
        st.write('---')

# Write the output

"""
## Output
"""

def sum_bags(bags_1 : Bags, bags_2 : Bags) -> Bags:
    """Sum the bags in two multisets of bags."""
    bags_sum = bags_1.copy()
    for bag_type, num_bags_2 in bags_2.items():
        num_bags_1 = bags_sum.get(bag_type, 0)
        bags_sum[bag_type] = num_bags_1 + num_bags_2
    return bags_sum

def mult_bags(coef : int, bags : Bags) -> Bags:
    """Multiply the number of bags in a multiset of bags."""
    return {bag_type:(coef * num_bags) for bag_type, num_bags in bags.items()}

bags_per_level = [{'shiny gold': 1}]
while True:
    bags_last_level = bags_per_level[-1]
    if not bags_last_level:
        break
    bags_next_level : Bags = {}
    for bag_type, num_bags in bags_last_level.items():
        bags_next_level = sum_bags(bags_next_level,
                mult_bags(num_bags, contains[bag_type]))
    bags_per_level.append(bags_next_level)
    if show_debug_output:
        st.write(bags_per_level)
all_bags = functools.reduce(sum_bags, bags_per_level[1:])
total_num_bags = functools.reduce(int.__add__, all_bags.values())        
"In total there are", total_num_bags, "bags across:", all_bags

