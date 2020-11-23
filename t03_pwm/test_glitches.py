from pygmyhdl import *
from t03_pwm.less_simple_pwm import pwm_less_simple


def test_bench(num_cycles, clk_, threshold_):
    clk_.next = 0
    threshold_.next = 3  # Start with threshold of 3.
    yield delay(1)
    for cycle in range(num_cycles):
        clk_.next = 0
        # Raise the threshold to 8 after 15 cycles.
        if cycle >= 14:
            threshold_.next = 8
        yield delay(1)
        clk_.next = 1
        yield delay(1)


if __name__ == '__main__':
    initialize()
    clk = Wire(name='clk')
    pwm = Wire(name='pwm')
    threshold = Bus(4, name='threshold')
    pwm_less_simple(clk, pwm, threshold, 10)

    simulate(test_bench(20, clk, threshold))
    show_text_table()