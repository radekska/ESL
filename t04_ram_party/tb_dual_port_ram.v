module tb_dual_port_ram;

reg clk_i;
reg wr_i;
reg [7:0] wr_addr_i;
reg [7:0] rd_addr_i;
reg [7:0] data_i;
wire [7:0] data_o;

initial begin
    $from_myhdl(
        clk_i,
        wr_i,
        wr_addr_i,
        rd_addr_i,
        data_i
    );
    $to_myhdl(
        data_o
    );
end

dual_port_ram dut(
    clk_i,
    wr_i,
    wr_addr_i,
    rd_addr_i,
    data_i,
    data_o
);

endmodule
