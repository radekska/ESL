from pygmyhdl import *

# initialize the module
initialize()


# defining core blinking function
@chunk
def blinker(clk_i, led_o, length):
    cnt = Bus(length, name='cnt')

    @seq_logic(clk_i.posedge)
    def counter_logic():
        cnt.next = cnt + 1

    @comb_logic
    def output_logic():
        led_o.next = cnt[length - 1]


# defining signals
clk = Wire(name='clk')
led = Wire(name='led')

blinker(clk_i=clk, led_o=led, length=3)

# simulation
clk_sim(clk, num_cycles=16)  # Pulse the clock input 16 times.
show_text_table()

# converting script to verilog and vhdl
toVerilog(blinker, clk_i=clk, led_o=led, length=22)
toVHDL(blinker, clk_i=clk, led_o=led, length=22)


