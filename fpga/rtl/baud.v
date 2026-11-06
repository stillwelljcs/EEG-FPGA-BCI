`timescale 1ns / 1ps

module baud (
    input wire clk,
    output reg tick = 0
    );
    
    reg [9:0] count = 0;
    
    always @(posedge clk) begin
        if (count == 868 - 1) begin
            count <= 0;
            tick <= 1'b1;
        end else begin
            count <= count + 1;
            tick <= 0;
        end
   end
endmodule
