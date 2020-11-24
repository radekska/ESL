module tb_optimized_simple_ram;

reg clk_i;
reg wr_i;
reg [7:0] addr_i;
reg [7:0] data_i;
wire [7:0] data_o;

initial begin
    $from_myhdl(
        clk_i,
        wr_i,
        addr_i,
        data_i
    );
    $to_myhdl(
        data_o
    );
end

optimized_simple_ram dut(
    clk_i,
    wr_i,
    addr_i,
    data_i,
    data_o
);

endmodule
