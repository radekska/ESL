from pygmyhdl import *
import math


@chunk
def pwm_less_simple(clk_i, pwm_o, threshold, duration):
    length = math.ceil(math.log(duration, 2))
    cnt = Bus(length, name='cnt')

    # Augment the counter with a comparator to adjust the pulse duration.
    @seq_logic(clk_i.posedge)
    def cntr_logic():
        cnt.next = cnt + 1
        # Reset the counter to zero once it reaches one less than the desired duration.
        # So if the duration is 3, the counter will count 0, 1, 2, 0, 1, 2...
        if cnt == duration - 1:
            cnt.next = 0

    @comb_logic
    def output_logic():
        pwm_o.next = cnt < threshold


if __name__ == '__main__':
    initialize()
    clk = Wire(name='clk')
    pwm = Wire(name='pwm')
    pwm_less_simple(clk, pwm, threshold=3, duration=5)
    clk_sim(clk, num_cycles=15)
    show_text_table()
