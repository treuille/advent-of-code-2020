import streamlit as st
from streamlit_ace import st_ace

"""
# Advent of Code 2020 in Streamlit - 05
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

# BFFFBBFRRR: row 70, column 7, seat ID 567.
# FFFBBBFRRR: row 14, column 7, seat ID 119.
# BBFFBBFRLL: row 102, column 4, seat ID 820.

max_seat = -1
taken_seats = []
for line_num, line in enumerate(problem_input.split('\n')):
    row_str = line[:7].replace('B', '1').replace('F', '0')
    row = int(row_str, 2)
    col_str = line[7:10].replace('R', '1').replace('L', '0')
    col = int(col_str, 2)
    seat = row * 8 + col
    taken_seats.append(seat)
    if show_debug_output:
        st.write(f'`{line_num}`: line=`"{line}"`')
        st.write(col_str, col)
        st.write(row_str, row)
        st.write("seat:", seat)
    if seat > max_seat:
        max_seat = seat
st.write("Highest seat:", max_seat)

# Try to figure out which seat I have
taken_seats.sort()
st.write('taken_seats', taken_seats)
for i in range(1, len(taken_seats)):
    if taken_seats[i] - taken_seats[i-1] > 1:
        st.write(i - 1, i, taken_seats[i-1], taken_seats[i])

