import streamlit as st
from streamlit_ace import st_ace
import typing

"""
# Advent of Code 2020 in Streamlit - 04
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
REQUIRED_FIELDS = {
    "byr", # (Birth Year)
    "iyr", # (Issue Year)
    "eyr", # (Expiration Year)
    "hgt", # (Height)
    "hcl", # (Hair Color)
    "ecl", # (Eye Color)
    "pid", # (Passport ID)
}

OPTIONAL_FIELDS = {
    "cid", # (Country ID)
}

ALL_FIELDS = REQUIRED_FIELDS.union(OPTIONAL_FIELDS)

# st.write(REQUIRED_FIELDS)
# st.write(OPTIONAL_FIELDS)
# st.write(ALL_FIELDS)

valid_passports = 0
for passport in problem_input.split('\n\n'):
    passport = passport.replace("\n", " ")
    params = dict(typing.cast(typing.Tuple[str, str], param.split(':'))
        for param in passport.split(' '))
    fields = set(params.keys())
    if show_debug_output:
        st.write(f'`"{passport}"`')
        st.json(params)
        st.write(fields)
    assert fields <= ALL_FIELDS, f"Unexpected field: {fields}"
    if REQUIRED_FIELDS <= fields:
        valid_passports += 1
st.write(f"There are {valid_passports} valid passports.")
