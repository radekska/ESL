from pygmyhdl import *
from t03_pwm.simple_pwm import pwm_simple


@chunk
def ramp(clk_i, ramp_o):
    """
    Inputs:
        clk_i: Clock input.
    Outputs:
        ramp_o: Multi-bit amplitude of ramp.
    """

    # Delta is the increment (+1) or decrement (-1) for the counter.
    delta = Bus(len(ramp_o))

    @seq_logic(clk_i.posedge)
    def logic():
        # Add delta to the current ramp value to get the next ramp value.
        ramp_o.next = ramp_o + delta

        # When the ramp reaches the bottom, set delta to +1 to start back up the ramp.
        if ramp_o == 1:
            delta.next = 1

        # When the ramp reaches the top, set delta to -1 to start back down the ramp.
        elif ramp_o == ramp_o.max - 2:
            delta.next = -1

        # After configuring the FPGA, the delta register is set to zero.
        # Set it to +1 and set the ramp value to +1 to get things going.
        elif delta == 0:
            delta.next = 1
            ramp_o.next = 1


@chunk
def wax_wane(clk_i, led_o, length):
    rampout = Bus(length, name='ramp')  # Create the triangle ramp counter register.
    ramp(clk_i, rampout)  # Generate the ramp.
    pwm_simple(clk_i, led_o, rampout.o[length:length - 4])  # Use the upper 4 ramp bits to drive the PWM threshold


if __name__ == '__main__':
    initialize()
    clk = Wire(name='clk')
    led = Wire(name='led')
    wax_wane(clk, led, 6)  # Set ramp counter to 6 bits: 0, 1, 2, ..., 61, 62, 63, 62, 61, ..., 2, 1, 0, ...

    clk_sim(clk, num_cycles=180)
    show_text_table()
    toVerilog(wax_wane, clk, led, 23)
