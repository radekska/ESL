from pygmyhdl import *


# defining adder
@chunk
def full_adder_bit(a_i, b_i, c_i, s_o, c_o):
    @comb_logic
    def logic():
        # defining XOR
        s_o.next = a_i ^ b_i ^ c_i
        c_o.next = (a_i & b_i) | (a_i & c_i) | (b_i & c_i)


@chunk
def adder(a_i, b_i, s_o):
    c = Bus(len(a_i) + 1)
    c.i[0] = 0

    for k in range(len(a_i)):
        full_adder_bit(a_i=a_i.o[k], b_i=b_i.o[k], c_i=c.o[k], s_o=s_o.i[k], c_o=c.i[k + 1])




if __name__ == '__main__':
    initialize()  # Once again, initialize for a new simulation.

    # Declare 8-bit buses for the two numbers to be added and the sum.
    a = Bus(8, name='a')
    b = Bus(8, name='b')
    s = Bus(8, name='sum')

    # Instantiate an adder and connect the I/O buses.
    adder(a, b, s)

    # Simulate the adder's output for 20 randomly-selected inputs.
    random_sim(a, b, num_tests=20)

    # Show a table of the adder output for each set of inputs.
    show_text_table()
