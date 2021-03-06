// File: simple_ram.v
// Generated by MyHDL 0.11
// Date: Tue Nov 24 11:39:27 2020


`timescale 1ns/10ps

module simple_ram (
    clk_i,
    en_i,
    wr_i,
    addr_i,
    data_i,
    data_o
);


input clk_i;
input en_i;
input wr_i;
input [7:0] addr_i;
input [7:0] data_i;
output [7:0] data_o;
reg [7:0] data_o;

reg [7:0] mem [0:256-1];



always @(posedge clk_i) begin: SIMPLE_RAM_LOC_INSTS_CHUNK_INSTS_K
    if (en_i) begin
        if (wr_i) begin
            mem[addr_i] <= data_i;
        end
        else begin
            data_o <= mem[addr_i];
        end
    end
end

endmodule
