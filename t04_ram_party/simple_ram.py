from pygmyhdl import *


# defining block ram instance
@chunk
def simple_ram(clk_i, en_i, wr_i, addr_i, data_i, data_o):
    mem = [Bus(len(data_i)) for _ in range(2 ** len(addr_i))]

    @seq_logic(clk_i.posedge)
    def logic():
        if en_i:
            if wr_i:
                mem[addr_i.val].next = data_i
            else:
                data_o.next = mem[addr_i.val]


def ram_test_bench(clk_i, en_i, wr_i, addr_i, data_i):
    en_i.next = 1
    wr_i.next = 1

    for i in range(10):
        addr_i.next = i
        data_i.next = 3 * i + 1

        clk_i.next = 0
        yield delay(1)
        clk_i.next = 1
        yield delay(1)

    wr_i.next = 0
    for i in range(10):
        addr_i.next = i

        clk_i.next = 0
        yield delay(1)
        clk_i.next = 1
        yield delay(1)


if __name__ == '__main__':
    initialize()

    clk = Wire(name='clk')
    en = Wire(name='en')
    wr = Wire(name='wr')
    addr = Bus(8, name='addr')
    data_in = Bus(8, name='data_i')
    data_out = Bus(8, name='data_o')

    simple_ram(clk_i=clk, en_i=en, wr_i=wr, addr_i=addr, data_i=data_in, data_o=data_out)

    simulate(ram_test_bench(clk_i=clk, en_i=en, wr_i=wr, addr_i=addr, data_i=data_in))

    show_text_table('en clk wr addr data_i data_o')

    # toVerilog(simple_ram, clk_i=Wire(), en_i=Wire(), wr_i=Wire(), addr_i=Bus(8), data_i=Bus(8), data_o=Bus(8))



