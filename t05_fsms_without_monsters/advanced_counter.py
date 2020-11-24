from pygmyhdl import *


@chunk
def counter_en_rst(clk_i, en_i, rst_i, cnt_o):
    cnt = Bus(len(cnt_o))

    # The next state logic now includes a reset input to clear the counter
    # to zero, and an enable input that only allows counting when it is true.
    @seq_logic(clk_i.posedge)
    def next_state_logic():
        if rst_i:
            cnt.next = 0
        elif en_i:
            cnt.next = cnt + 1
        else:
            pass

    @comb_logic
    def output_logic():
        cnt_o.next = cnt


def cntr_tb(clk, en, rst):
    '''Test bench for the counter with a reset and enable inputs.'''

    # Enable the counter for a few cycles.
    rst.next = 0
    en.next = 1
    for _ in range(4):
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)

    # Disable the counter for a few cycles.
    en.next = 0
    for _ in range(2):
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)

    # Re-enable the counter for a few cycles.
    en.next = 1
    for _ in range(2):
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)

    # Reset the counter.
    rst.next = 1
    clk.next = 0
    yield delay(1)
    clk.next = 1
    yield delay(1)

    # Start counting again.
    rst.next = 0
    for _ in range(4):
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)


if __name__ == '__main__':
    initialize()
    clk = Wire(name='clk')
    rst = Wire(1, name='rst')
    en = Wire(1, name='en')
    cnt = Bus(3, name='cnt')
    counter_en_rst(clk_i=clk, rst_i=rst, en_i=en, cnt_o=cnt)

    simulate(cntr_tb(clk, en, rst))
    show_text_table()
