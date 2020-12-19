import streamlit as st
from streamlit_ace import st_ace
import typing
import re

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

# List of fields
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

# Field regular expressions
FOUR_DIGITS = re.compile(r"\d{4}$")
HEIGHT_FORMAT = re.compile(r"(?P<height>\d+)(?P<units>cm|in)$")

# Check all passports
valid_passports = 0
for passport in problem_input.split('\n\n'):
    # Parse out all the fields from the passport 
    passport = passport.replace("\n", " ")
    params = dict(typing.cast(typing.Tuple[str, str], param.split(':'))
        for param in passport.split(' '))
    fields = set(params.keys())
    if show_debug_output:
        st.write(f'`"{passport}"`')
        st.json(params)
        st.write(fields)
    assert fields <= ALL_FIELDS, f"Unexpected field: {fields}"

    # Check whether the passport is valid
    valid = True
    if not REQUIRED_FIELDS <= fields:
        valid = False
    else:
        for field, value in params.items():
            assert valid == True, f"{field} {value}"
            # st.write(f'Checking field "{field}" valid={valid}')
            if field == "byr":
                # (Birth Year) - four digits; at least 1920 and at most 2002.
                if not FOUR_DIGITS.match(value):
                    valid = False
                else:
                    byr = int(value)
                    if not (1920 <= byr <= 2002):
                        valid = False
            elif field == "iyr":
                # (Issue Year) - four digits; at least 2010 and at most 2020.
                if not FOUR_DIGITS.match(value):
                    valid = False
                else:
                    iyr = int(value)
                    if not (2010 <= iyr <= 2020):
                        valid = False
            elif field == "eyr":
                # (Expiration Year) - four digits; at least 2020 and at most 2030.
                if not FOUR_DIGITS.match(value):
                    valid = False
                else:
                    eyr = int(value)
                    if not (2020 <= eyr <= 2030):
                        valid = False
            elif field == "hgt":
                # (Height) - a number followed by either cm or in:
                # cm, the number must be at least 150 and at most 193.
                # in, the number must be at least 59 and at most 76.
                match = HEIGHT_FORMAT.match(value)
                if not match:
                    valid = False
                else:
                    height = int(match.group("height"))
                    units = match.group("units")
                    if units == 'cm' and not (150 <= height <= 193):
                        valid = False
                    if units == 'in' and not (59 <= height <= 76):
                        valid = False
            # elif field == "hcl":
            # elif field == "hcl":
            #     # (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
            #     raise NotImplementedError
            #     continue
            # elif field == "ecl":
            #     # (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
            #     raise NotImplementedError
            #     continue
            # elif field == "pid":
            #     # (Passport ID) - a nine-digit number, including leading zeroes.
            #     raise NotImplementedError
            #     continue
            # elif field == "cid":
            #     # (Country ID) - ignored, missing or not.
            #     raise NotImplementedError
            #     continue
            if field == 'hgt' and show_debug_output:
                if valid:
                    st.success(f'Field `{field}` is valid: `"{value}"`')
                else:
                    st.error(f'Field `{field}` is invalid: `"{value}"`')
                    raise RuntimeError
            if not valid:
                break
    if valid:
        valid_passports += 1
st.write(f"There are `{valid_passports}` valid passports!")
