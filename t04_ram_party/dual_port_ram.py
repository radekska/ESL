from pygmyhdl import *


@chunk
def dual_port_ram(clk_i, wr_i, wr_addr_i, rd_addr_i, data_i, data_o):
    mem = [Bus(len(data_i)) for _ in range(2 ** len(wr_addr_i))]

    @seq_logic(clk_i.posedge)
    def logic():
        if wr_i:
            mem[wr_addr_i.val].next = data_i
        data_o.next = mem[rd_addr_i.val]


def ram_test_bench(clk_i, wr_i, wr_addr_i, rd_addr_i, data_i):
    for i in range(10):
        wr_addr_i.next = i
        data_i.next = 3 * i + 1
        wr_i.next = 1

        rd_addr_i.next = i - 3

        clk_i.next = 0
        yield delay(1)
        clk_i.next = 1
        yield delay(1)


if __name__ == '__main__':
    initialize()

    clk = Wire(name='clk')
    wr = Wire(name='wr')
    wr_addr = Bus(8, name='wr_addr')
    rd_addr = Bus(8, name='rd_addr')
    data_in = Bus(8, name='data_i')
    data_out = Bus(8, name='data_o')

    dual_port_ram(clk, wr, wr_addr, rd_addr, data_in, data_out)

    simulate(ram_test_bench(clk, wr, wr_addr, rd_addr, data_in))

    show_text_table('clk wr wr_addr data_i rd_addr data_o')
    toVerilog(dual_port_ram, clk_i=Wire(), wr_i=Wire(), wr_addr_i=Bus(8), rd_addr_i=Bus(8), data_i=Bus(8),
              data_o=Bus(8))
