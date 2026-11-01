`timescale 1ns/1ps
// Simulation check: measure pulse width and period at three positions.
module tb_servo;
    reg clk = 0, rst = 1;
    reg [7:0] pos = 0;
    wire pwm;
    always #5 clk = ~clk;   // 100 MHz

    servo_pwm dut (.clk(clk), .rst(rst), .position(pos), .pwm(pwm));

    time t_rise, t_fall, t_prev_rise;
    task measure(input [7:0] p);
        begin
            pos = p;
            // let two full periods pass so the new width is latched
            repeat (2) @(posedge pwm);
            @(posedge pwm) t_prev_rise = $time;
            @(negedge pwm) t_fall = $time;
            @(posedge pwm) t_rise = $time;
            $display("pos=%3d  pulse=%0.3f ms  period=%0.3f ms",
                     p, (t_fall - t_prev_rise)/1e6, (t_rise - t_prev_rise)/1e6);
        end
    endtask

    initial begin
        #100 rst = 0;
        measure(0);
        measure(128);
        measure(255);
        $finish;
    end
endmodule
