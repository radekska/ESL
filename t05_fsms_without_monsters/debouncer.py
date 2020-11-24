from pygmyhdl import *
from math import ceil, log2


@chunk
def debouncer(clk_i, button_i, button_o, debounce_time):
    """
    Inputs:
        clk_i: Main clock input.
        button_i: Raw button input.
        button_o: Debounced button output.
        debounce_time: Number of clock cycles the button value has to be stable.
    """

    # These are the state variables of the FSM.
    debounce_cnt = Bus(int(ceil(log2(debounce_time + 1))), name='dbcnt')  # Counter big enough to store debounce time.
    prev_button = Wire(name='prev_button')  # Stores the button value from the previous clock cycle.

    @seq_logic(clk_i.posedge)
    def next_state_logic():
        if button_i == prev_button:
            # If the current and previous button values are the same, decrement the counter
            # until it reaches zero and then stop.
            if debounce_cnt != 0:
                debounce_cnt.next = debounce_cnt - 1
        else:
            # If the current and previous button values aren't the same, then the button must
            # still be bouncing so reset the counter to the debounce interval and try again.
            debounce_cnt.next = debounce_time

        # Store the current button value for comparison during the next clock cycle.
        prev_button.next = button_i

    @seq_logic(clk_i.posedge)
    def output_logic():
        if debounce_cnt == 0:
            # Output the stable button value whenever the counter is zero.
            # Don't use the actual button input value because that could change at any time.
            button_o.next = prev_button


def debounce_tb(button_i, clk):
    """Test bench for the counter with a reset and enable inputs."""

    # Initialize the button and leave it stable for the debounce time.
    button_i.next = 1
    for _ in range(4):
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)

    # Blip the button for less than the debounce time and show the debounced output does not change.
    button_i.next = 0
    for _ in range(2):
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)
    button_i.next = 1
    for _ in range(2):
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)

    # Press the button for more than the debounce time and show the debounced output changes.
    button_i.next = 0
    for _ in range(5):
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)


if __name__ == '__main__':
    initialize()  # Initialize for simulation here because we'll be watching the internal debounce counter.

    clk = Wire(name='clk')
    button_i = Wire(name='button_i')
    button_o = Wire(name='button_o')
    debouncer(clk, button_i, button_o, 3)

    simulate(debounce_tb(button_i, clk))
    show_text_table()