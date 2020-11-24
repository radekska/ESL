from pygmyhdl import *


@chunk
def classic_fsm_v2(clk_i, inputs_i, outputs_o):
    fsm_state = State('A', 'B', 'C', 'D', name='state')
    reset_cnt = Bus(2)

    # Variables for storing the input values during the previous clock
    # and holding the changes between the current and previous input values.
    prev_inputs = Bus(len(inputs_i), name='prev_inputs')
    input_chgs = Bus(len(inputs_i), name='input_chgs')

    # This logic compares the current input values with the negation of the previous values.
    # The output is active only if an input goes from 0 to 1.
    @comb_logic
    def detect_chg():
        input_chgs.next = inputs_i & ~prev_inputs

    # This is the same FSM state transition logic as before, except it looks at the
    # input_chgs signals instead of the input_i signals.
    @seq_logic(clk_i.posedge)
    def next_state_logic():
        if reset_cnt < reset_cnt.max - 1:
            reset_cnt.next = reset_cnt + 1
            fsm_state.next = fsm_state.s.A
        elif fsm_state == fsm_state.s.A:
            if input_chgs[0]:
                fsm_state.next = fsm_state.s.B
            elif input_chgs[1]:
                fsm_state.next = fsm_state.s.D
        elif fsm_state == fsm_state.s.B:
            if input_chgs[0]:
                fsm_state.next = fsm_state.s.C
            elif input_chgs[1]:
                fsm_state.next = fsm_state.s.A
        elif fsm_state == fsm_state.s.C:
            if input_chgs[0]:
                fsm_state.next = fsm_state.s.D
            elif input_chgs[1]:
                fsm_state.next = fsm_state.s.B
        elif fsm_state == fsm_state.s.D:
            if input_chgs[0]:
                fsm_state.next = fsm_state.s.A
            elif input_chgs[1]:
                fsm_state.next = fsm_state.s.C
        else:
            fsm_state.next = fsm_state.s.A

        prev_inputs.next = inputs_i  # Record the current input values.

    @comb_logic
    def output_logic():
        if fsm_state == fsm_state.s.A:
            outputs_o.next = 0b0001
        elif fsm_state == fsm_state.s.B:
            outputs_o.next = 0b0010
        elif fsm_state == fsm_state.s.C:
            outputs_o.next = 0b0100
        elif fsm_state == fsm_state.s.D:
            outputs_o.next = 0b1000
        else:
            outputs_o.next = 0b1111


def fsm_tb(clk, inputs):
    nop = 0b00
    fwd = 0b01
    bck = 0b10

    ins = [nop, nop, nop, nop, fwd, fwd, fwd, bck, bck, bck]
    for inputs.next in ins:
        clk.next = 0
        yield delay(1)
        clk.next = 1
        yield delay(1)

    # Interspersed active and inactive inputs.
    ins = [fwd, nop, fwd, nop, fwd, nop, bck, nop, bck, nop, bck, nop]
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
    classic_fsm_v2(clk, inputs, outputs)

    simulate(fsm_tb(clk, inputs))
    show_text_table('clk inputs prev_inputs input_chgs state outputs')

    toVerilog(classic_fsm_v2, clk_i=Wire(), inputs_i=Bus(2), outputs_o=Bus(4))
