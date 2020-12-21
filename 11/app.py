import streamlit as st
from streamlit_ace import st_ace
from typing import Tuple, Set, cast, Optional, NamedTuple

"""
# Advent of Code 2020 in Streamlit - 11
"""

# Types
Seat = Tuple[int, int]
Seats = Set[Seat]
class Dims(NamedTuple):
    """Represents the width and height extent of the state space."""
    width: int
    height: int

"""
## Input
"""

# Load the input
problem_input = st_ace(height=150)
show_debug_output = st.checkbox("Show debug output")

def parse_input(problem_input: str) -> Tuple[Seats, Dims]:
    """Read the list of seats from the input string."""
    # Parse out the set of seats
    lines = problem_input.split('\n')
    seats: Seats = set()
    for y, line in enumerate(lines):
        assert line.strip(), "Cannot have an empty line."
        seats |= {(x, y) for x, c in enumerate(line) if c == 'L'}
    
    # Figure out the dimensions
    dims = Dims(width = len(lines[0]), height = len(lines))

    # All done
    return (seats, dims)

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

def get_adjacent_seats(seat: Seat, seats: Seats, dims: Dims) -> Seats:
    """Returns the set of adjacent seats according to the part 2 algorithm."""
    adjacent_seats: Seats = set()
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue
            x, y = seat
            while True:
                x += dx
                if x < 0 or x >= dims.width:
                    break
                y += dy
                if y < 0 or y >= dims.height:
                    break
                if (x, y) in seats:
                    adjacent_seats.add((x, y))
                    break
    return adjacent_seats

def cycle(occupied: Seats, seats: Seats, dims: Dims) -> Optional[Seats]:
    """Rune one iteration of the simulation."""
    newly_occupied: Seats = set()
    for seat in seats:
        adjacent_seats = get_adjacent_seats(seat, seats, dims)
        num_neighbors = len(adjacent_seats.intersection(occupied))

        # If a seat is empty (L) and there are no occupied seats adjacent to it,
        # the seat becomes occupied.
        if seat not in occupied:
            if num_neighbors == 0:
                newly_occupied.add(seat)

        # If a seat is occupied (#) and four or more seats adjacent to it are
        # also occupied, the seat becomes empty.
        elif num_neighbors < 5:
            newly_occupied.add(seat)

    if occupied != newly_occupied:
        return newly_occupied
    else:
        return None

def test_adjacency(seats: Seats, dims: Dims) -> None:
    """Provide a little UI to let the user test the new adjacent seat
    algorithm."""
    with st.beta_expander("Test Adjacency"):
        c1, c2 = st.beta_columns(2)
        x = c1.number_input("x", 0, dims.width - 1, 0) 
        y = c2.number_input("y", 0, dims.height - 1, 0) 
        adjacent_seats = get_adjacent_seats((x, y), seats, dims)
        print_seats(adjacent_seats, seats)


st.write("## Output")
seats, dims = parse_input(problem_input)        

test_adjacency(seats, dims)

if st.button("Run simulation"):
    occupied: Optional[Seats] = set()
    num_occupied = 0
    while occupied != None:
        if show_debug_output:
            print_seats(cast(Seats, occupied), seats)
        num_occupied = len(cast(Seats, occupied))
        occupied = cycle(cast(Seats, occupied), seats, dims)
    f"There are `{num_occupied}` occupied seats."
