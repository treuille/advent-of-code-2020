import streamlit as st
from streamlit_ace import st_ace

"""
# Advent of Code 2020 in Streamlit - 13
"""

@st.cache
def get_primes():
    """Returns a set of prime numbers."""
    with open("13/primes.txt") as input:
        return {int(x) for x in input.readlines()}

"""## Input"""

# Load the input
problem_input = st_ace(height=150)

"""## Computation"""

# Parse the input
line1, line2 = problem_input.split('\n')
start_time = int(line1)
bus_input = [(departure_offset, int(bus_number))
        for (departure_offset, bus_number) in
        enumerate(line2.split(',')) if bus_number != 'x']
bus_numbers = {bus_number for (_, bus_number) in bus_input}
assert set(bus_numbers) < get_primes(), "Must have only prime bus numbers."

# The loop precondition is for iteration i is that all buses 0..i satisify thier
# respective modular departure time constraints modulo the product of bus
# numbers 0..i. The 0th iteration (base case) is trivially satified by:
t, modulus = bus_input[0]

# Iterate over the buses, incrementing the timestep until we find the first that
# matches all our modular arithmetic constraints.
for departure_offset, bus_number in bus_input[1:]:
    # We want to update t and modulus as follows:
    # 
    # t -> t_prime = t + x * modulus
    # modulus -> modulus_prime = modulus * bus_number
    # 
    # Such that:
    # 
    # t_prime = departure_offset (mod bus_number)
    # t + x * modulus = departure_offset (mod bus_number)
    # x = modulus^-1 * (departure_offset - t) (mod bus_number)
    neg_departure_offset_minus_t = -departure_offset - t
    neg_departure_offset_minus_t += 2 * bus_number
    neg_departure_offset_minus_t %= bus_number
    assert 0 <= neg_departure_offset_minus_t < bus_number, \
            "departure_offset_minus_t should be simplified mod bus_number"
    assert bus_number > 2, "Bus number too small"
    mod_inv = (modulus ** (bus_number - 2)) % bus_number
    x = (mod_inv * neg_departure_offset_minus_t) % bus_number
    t += x * modulus
    modulus *= bus_number

    # Show our work
    st.write('departure_offset', departure_offset)
    st.write('bus_number', bus_number)
    st.write('modulus', modulus)
    st.write('mod_inv', mod_inv)
    st.write('product', (modulus * mod_inv))
    st.write('product mod', (modulus * mod_inv) % bus_number)
    st.write('x', x)
    st.write('t', t)
    st.write('modulus', modulus)
    st.write('**Result:**', t % bus_number)
    st.write("---")

"""## Output"""

st.write("The answer is:", t)
