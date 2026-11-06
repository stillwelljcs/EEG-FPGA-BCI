ERD Choices:

* each cue lasts for 4 seconds, but the useful data is really in between 0.5 seconds (pt has time to read cue change and begin reaction) and 2.5 seconds (get early neural response data since attention tends to drift afterwards.)

* Linear classifier: score = w_1 * x_1 + w_2 * x_2 + b
    * x-vals are features of a trial
    * w vals are weights, b is an offset and both are learned inside of training
    * decisions = score > 0 -> "right", score < 0 -> "left"
    * x_1 = mu power at C_3
    * x_2 = mu power at C_4

* We bandpass this data at 8-30 Hz because we want to select for the range where mu and beta peaks can occur. After bandpassing, we then cut this data into epochs to generate a list of voltages measured during a specific cue so we can have them organized and labeled for the classifier. We will average these values because if we fed the classifier the voltage readings (321 readings) the phase would be at a random point each time and it would require a lot more data and a different classifier architecture to see that pattern. If we tried to take the average of these values just as is we would end up with ~0 since voltage spends ~ the same time above and below and 0 axis, so we will use RMS.

* One average per epoch, per channel, so we get 3 data points per trial.