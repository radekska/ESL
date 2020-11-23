from pygmyhdl import *
from random import randint


# defining D flip-flop
@chunk
def dff(clk_i, d_i, q_o):
    @seq_logic(clk_i.posedge)
    def logic():
        q_o.next = d_i


# defining a register
@chunk
def register(clk_i, d_i, q_o):
    for k in range(len(d_i)):
        dff(clk_i, d_i.o[k], q_o.i[k])


def test_bench(clk_i, d_i):
    for i in range(10):
        d_i.next = randint(0, 256)
        clk_i.next = 0
        yield delay(1)
        clk_i.next = 1
        yield delay(1)


if __name__ == '__main__':
    initialize()
    # create clock signal and 8-bit register input and output buses.
    clk = Wire(name='clk')
    data_in = Bus(8, name='data_in')
    data_out = Bus(8, name='data_out')

    register(clk_i=clk, d_i=data_in, q_o=data_out)

    simulate(test_bench(clk, data_in))
    show_text_table()

