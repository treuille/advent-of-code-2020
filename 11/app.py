import streamlit as st
from streamlit_ace import st_ace
from typing import Tuple, Set, cast, Optional

"""
# Advent of Code 2020 in Streamlit - 11
"""

# Types
Seat = Tuple[int, int]
Seats = Set[Seat]

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")

def parse_input(problem_input: str) -> Seats:
    """Read the list of seats from the input string."""
    seats: Seats = set()
    for y, line in enumerate(problem_input.split('\n')):
        seats |= {(x, y) for x, c in enumerate(line) if c == 'L'}
    return seats

def print_seats(occupied: Seats, seats: Seats) -> None:
    """Prints out the seats nicely."""
    xs, ys = cast(Tuple[Set[int], Set[int]], map(set, zip(*seats)))
    seat_map = ""
    for y in range(min(ys), max(ys) + 1):
        for x in range(min(xs), max(xs) + 1):
            if (x, y) in occupied:
                seat_map += "#"
            elif (x, y) in seats:
                seat_map += "L"
            else:
                seat_map += "."
        seat_map += "\n"
    st.text(seat_map[:-1])

def get_adjacent_seats(seat: Seat) -> Seats:
    """Returns the set of eight adjacent seats."""
    sx, sy = seat
    return {(sx + x, sy + y)
            for x in range(-1, 2)
            for y in range(-1, 2)
            if (x != 0 or y != 0)}

def cycle(occupied: Seats, seats: Seats) -> Optional[Seats]:
    """Rune one iteration of the simulation."""
    newly_occupied: Seats = set()
    for seat in seats:
        adjacent_seats = get_adjacent_seats(seat)
        num_neighbors = len(adjacent_seats.intersection(occupied))

        # If a seat is empty (L) and there are no occupied seats adjacent to it,
        # the seat becomes occupied.
        if seat not in occupied:
            if num_neighbors == 0:
                newly_occupied.add(seat)

        # If a seat is occupied (#) and four or more seats adjacent to it are
        # also occupied, the seat becomes empty.
        elif num_neighbors < 4:
            newly_occupied.add(seat)

    if occupied != newly_occupied:
        return newly_occupied

"""
## Output
"""
seats = parse_input(problem_input)        
occupied: Optional[Seats] = set()
num_occupied = 0
while occupied != None:
    if show_debug_output:
        print_seats(cast(Seats, occupied), seats)
    num_occupied = len(occupied)
    occupied = cycle(cast(Seats, occupied), seats)
f"There are `{num_occupied}` occupied seats."
