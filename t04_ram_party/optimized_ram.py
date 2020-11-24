from pygmyhdl import *


# removed en_i signal
@chunk
def optimized_simple_ram(clk_i, wr_i, addr_i, data_i, data_o):
    mem = [Bus(len(data_i)) for _ in range(2 ** len(addr_i))]

    @seq_logic(clk_i.posedge)
    def logic():
        if wr_i:
            mem[addr_i.val].next = data_i
        else:
            data_o.next = mem[addr_i.val]


if __name__ == '__main__':
    toVerilog(optimized_simple_ram, clk_i=Wire(), wr_i=Wire(), addr_i=Bus(8), data_i=Bus(8), data_o=Bus(8))
