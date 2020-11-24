from pygmyhdl import *


@chunk
def counter(clk_i, cnt_o):
    # Here's the counter state variable.
    cnt = Bus(len(cnt_o))

    # The next state logic is just an adder that adds 1 to the current cnt state variable.
    @seq_logic(clk_i.posedge)
    def next_state_logic():
        cnt.next = cnt + 1

    # The output logic just sends the current cnt state variable to the output.
    @comb_logic
    def output_logic():
        cnt_o.next = cnt


if __name__ == '__main__':
    initialize()
    clk = Wire(name='clk')
    cnt = Bus(3, name='cnt')
    counter(clk_i=clk, cnt_o=cnt)
    clk_sim(clk, num_cycles=10)

    show_text_table()