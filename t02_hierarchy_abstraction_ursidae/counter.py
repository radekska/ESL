from pygmyhdl import *
from .register import register
from .adder import adder


# defining counter from adder and register
@chunk
def counter(clk_i, cnt_o):
    length = len(cnt_o)

    one = Bus(length, init_val=1)
    next_cnt = Bus(length)

    adder(one, cnt_o, next_cnt)

    register(clk_i, next_cnt, cnt_o)
