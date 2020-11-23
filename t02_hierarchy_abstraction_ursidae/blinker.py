from pygmyhdl import *
from t02_hierarchy_abstraction_ursidae.counter import counter


@chunk
def blinker(clk_i, led_o, length):
    cnt = Bus(length, name='cnt')
    counter(clk_i, cnt)

    @comb_logic
    def output_logic():
        led_o.next = cnt[length - 1]


if __name__ == '__main__':
    initialize()  # Initialize for simulation.
    clk = Wire(name='clk')  # Declare the clock input.
    led = Wire(name='led')  # Declare the LED output.
    blinker(clk, led, 3)  # Instantiate a three-bit blinker and attach I/O signals.
    clk_sim(clk, num_cycles=16)  # Apply 16 clock pulses.
    show_text_table()

    toVerilog(blinker, clk_i=clk, led_o=led, length=22)
