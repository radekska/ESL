from pygmyhdl import *
from t03_pwm.test_glitches import test_bench


@chunk
def pwm_glitchless(clk_i, pwm_o, threshold, interval):
    import math
    length = math.ceil(math.log(interval, 2))
    cnt = Bus(length)

    threshold_r = Bus(length, name='threshold_r')  # Create a register to hold the threshold value.

    @seq_logic(clk_i.posedge)
    def cntr_logic():
        cnt.next = cnt + 1
        if cnt == interval - 1:
            cnt.next = 0
            threshold_r.next = threshold  # The threshold only changes at the end of a pulse.

    @comb_logic
    def output_logic():
        pwm_o.next = cnt < threshold_r


if __name__ == '__main__':
    initialize()
    clk = Wire(name='clk')
    pwm = Wire(name='pwm')
    threshold = Bus(4, name='threshold')
    pwm_glitchless(clk, pwm, threshold, 10)

    simulate(test_bench(22, clk, threshold))
    show_text_table()
