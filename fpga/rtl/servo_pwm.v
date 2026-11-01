// Hobby servo PWM driver for Basys 3 (100 MHz clock)
// Position is set by sw[7:0]: 0 = one end, 255 = other end.
//
// Standard hobby servo signal:
//   period = 20 ms (50 Hz)
//   pulse  = 1.0 ms (0 deg) ... 2.0 ms (180 deg), 1.5 ms = center
// Some servos (e.g. SG90) accept ~0.5-2.5 ms for full travel; widen
// PULSE_MIN/PULSE_MAX carefully if yours doesn't reach the ends.

module servo_pwm #(
    parameter integer CLK_HZ    = 100_000_000,
    parameter integer PERIOD    = CLK_HZ / 50,     // 20 ms  -> 2,000,000 counts
    parameter integer PULSE_MIN = CLK_HZ / 1000,   // 1.0 ms -> 100,000 counts
    parameter integer PULSE_MAX = CLK_HZ / 500     // 2.0 ms -> 200,000 counts
)(
    input  wire       clk,
    input  wire       rst,        // active-high, synchronous
    input  wire [7:0] position,   // 0..255
    output reg        pwm
);
    localparam integer SPAN = PULSE_MAX - PULSE_MIN;  // 100,000 counts

    reg [21:0] counter = 0;       // 2^22 > 2,000,000
    reg [21:0] pulse_len = PULSE_MIN;

    // pulse = PULSE_MIN + position * SPAN / 255
    // Latched once per period so the pulse never changes mid-cycle.
    wire [31:0] scaled = (position * SPAN) / 255;

    always @(posedge clk) begin
        if (rst) begin
            counter   <= 0;
            pulse_len <= PULSE_MIN;
            pwm       <= 1'b0;
        end else begin
            if (counter == PERIOD - 1) begin
                counter   <= 0;
                pulse_len <= PULSE_MIN + scaled[21:0];
            end else begin
                counter <= counter + 1;
            end
            pwm <= (counter < pulse_len);
        end
    end
endmodule

// Top level: switches -> servo on Pmod JA1, LEDs mirror switches.
module top (
    input  wire        clk,
    input  wire        btnC,      // reset
    input  wire [7:0]  sw,
    output wire [7:0]  led,
    output wire        servo      // Pmod JA pin 1
);
    // Two-flop synchronizer for the asynchronous switch inputs
    reg [7:0] sw_s1 = 0, sw_s2 = 0;
    always @(posedge clk) begin
        sw_s1 <= sw;
        sw_s2 <= sw_s1;
    end

    servo_pwm u_servo (
        .clk      (clk),
        .rst      (btnC),
        .position (sw_s2),
        .pwm      (servo)
    );

    assign led = sw_s2;
endmodule
