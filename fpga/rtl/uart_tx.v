`timescale 1ns / 1ps

module uart_tx(
    input wire clk,
    input wire tick,
    input wire start,
    input wire [7:0] data,
    output wire tx,
    output reg busy = 0
    );
    
    reg [3:0] index = 4'd0;
    reg pending = 0;
    reg [9:0] shift = {10{1'b1}};
    
    always @(posedge clk) begin
        if (start && !busy) begin
            pending <= 1'b1;
        end
        if (tick) begin
           if (pending && !busy) begin
            index <= 0;
            shift <= {1'b1, data[7:0], 1'b0};
            busy <= 1'b1;
            pending <= 1'b0;
           end
           
           if (!pending && busy) begin
            if (index == 9) begin
                busy <= 0;
            end else begin
                shift <= {1'b1, shift[9:1]};
                index <= index + 1;
           end
           end  
        end
    end
    
    assign tx = shift[0];
    
endmodule
