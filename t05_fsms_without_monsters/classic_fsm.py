from pygmyhdl import *


@chunk
def classic_fsm(clk_i, inputs_i, outputs_o):
    '''
    Inputs:
        clk_i: Main clock input.
        inputs_i: Two-bit input vector directs state transitions.
        outputs_o: Four-bit output vector.
    '''

    # Declare a state variable with four states. In addition to the current
    # state of the FSM, the state variable also stores a complete list of its
    # possible values to use for comparing what state the FSM is in and for
    # assigning a new state.
    fsm_state = State('A', 'B', 'C', 'D', name='state')

    # This counter is used to apply a reset to the FSM for the first few clocks upon startup.
    reset_cnt = Bus(2)

    @seq_logic(clk_i.posedge)
    def next_state_logic():
        if reset_cnt < reset_cnt.max - 1:
            # The reset counter starts at zero upon startup. The FSM stays in this reset
            # state until the counter increments to its maximum value. Then it never returns here.
            reset_cnt.next = reset_cnt + 1
            fsm_state.next = fsm_state.s.A  # Set initial state for FSM after reset.
        elif fsm_state == fsm_state.s.A:  # Compare current state to state A.
            # If the FSM is in state A, then go forward to state B if inputs_i[0] is active,
            # otherwise go backward to state D if inputs_i[1] is active.
            # Stay in this state if neither input is active.
            if inputs_i[0]:
                fsm_state.next = fsm_state.s.B  # Update state to state B.
            elif inputs_i[1]:
                fsm_state.next = fsm_state.s.D  # Update state to state D.
        elif fsm_state == fsm_state.s.B:
            # State B operates similarly to state A.
            if inputs_i[0]:
                fsm_state.next = fsm_state.s.C
            elif inputs_i[1]:
                fsm_state.next = fsm_state.s.A
        elif fsm_state == fsm_state.s.C:
            # State C operates similarly to states A and B.
            if inputs_i[0]:
                fsm_state.next = fsm_state.s.D
            elif inputs_i[1]:
                fsm_state.next = fsm_state.s.B
        elif fsm_state == fsm_state.s.D:
            # State D yada, yada...
            if inputs_i[0]:
                fsm_state.next = fsm_state.s.A
            elif inputs_i[1]:
                fsm_state.next = fsm_state.s.C
        else:
            # If the FSM is in some unknown state, send it back to the starting state.
            fsm_state.next = fsm_state.s.A

    @comb_logic
    def output_logic():
        # Turn on one of the outputs depending upon which state the FSM is in.
        if fsm_state == fsm_state.s.A:
            outputs_o.next = 0b0001
        elif fsm_state == fsm_state.s.B:
            outputs_o.next = 0b0010
        elif fsm_state == fsm_state.s.C:
            outputs_o.next = 0b0100
        elif fsm_state == fsm_state.s.D:
            outputs_o.next = 0b1000
        else:
            # Turn on all the outputs if the FSM is in some unknown state (shouldn't happen).
            outputs_o.next = 0b1111


def fsm_tb(clk, inputs):
    nop = 0b00  # no operation - both inputs are inactive
    fwd = 0b01  # Input combination for moving forward.
    bck = 0b10  # Input combination for moving backward.

    # Input sequence of 3 forwards and 3 backwards transitions.
    # The four initial NOPs are for the FSM's initial reset period.
    ins = [nop, nop, nop, nop, fwd, fwd, fwd, bck, bck, bck]

    # Apply each input combination from the list and then pulse the clock.
    for inputs.next in ins:
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)


if __name__ == '__main__':
    initialize()

    inputs = Bus(2, name='inputs')
    outputs = Bus(4, name='outputs')
    clk = Wire(name='clk')
    classic_fsm(clk, inputs, outputs)

    simulate(fsm_tb(clk, inputs))
    show_text_table()