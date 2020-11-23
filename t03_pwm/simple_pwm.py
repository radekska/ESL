from pygmyhdl import *


@chunk
def pwm_simple(clk_i, pwm_o, threshold):
    '''
    Inputs:
        clk_i: PWM changes state on the rising edge of this clock input.
        threshold: Bit-length determines counter width and value determines when output goes low.
    Outputs:
        pwm_o: PWM output starts and stays high until counter > threshold and then output goes low.
    '''
    cnt = Bus(len(threshold), name='cnt')  # Create a counter with the same number of bits as the threshold.

    # Here's the sequential logic for incrementing the counter. We've seen this before!
    @seq_logic(clk_i.posedge)
    def cntr_logic():
        cnt.next = cnt + 1

    # Combinational logic that drives the PWM output high when the counter is less than the threshold.
    @comb_logic
    def output_logic():
        pwm_o.next = cnt < threshold  # cnt<threshold evaluates to either True (1) or False (0).


if __name__ == '__main__':
    initialize()

    # Create signals and attach them to the PWM.
    clk = Wire(name='clk')
    pwm = Wire(name='pwm')
    threshold = Bus(3, init_val=3)  # Use a 3-bit threshold with a value of 3.
    pwm_simple(clk, pwm, threshold)

    # Pulse the clock and look at the PWM output.
    clk_sim(clk, num_cycles=24)
    show_text_table()