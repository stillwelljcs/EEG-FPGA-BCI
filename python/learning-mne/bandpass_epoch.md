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

* Implementing ERD:
    * We must include T0, so we can compare how T1 and T2 change relative to T0 (idle/rest state) otherwise we are really just confirming that T1 and T2 do in fact differ from each other, which is basically what the linear classifier is doing. The purpose of computing ERD in the first place is that it tells us that the signal that is power dropping over the opposite hemisphere when the subject imagines moving their hand exists and that if this does not occur we may need to pick another subject. 

    * basically just checking if A.) there is a response at all and B.) if the response is "lateralized" meaning that it presents on opposite sides for both left and right hand movements. 

    * this gives us three possible outcomes: 
        *No drop in activity vs T0 (Rest state) this allows for the possiblity of a specific subjects brain measurements that just happen to not express not much of a difference in T0 vs T1 or T2, or that our linear classifier is broken in some way, either way this is unneeded ambiguity in our problem solving process.

        * The subject does respond to the imagery but T1 (left) vs T2 (right) does not show much of a difference. so the L/R classifer will end up at about "chance" (~50%) for either L vs. R

        * We will see distinct a signal for T1 (imagined movement for T1 and a neuroscience-predicted drop at channel C4) as opposed to T2 (imagined movement for T2 and a neuroscience-predicted drop at channel C3) and this will allow the linear classifier to function optimally. If say, channel C4 dropped at an imagined right hand movement, this would indicate a problem with labeling or the channel itself, same thing with problem 1 where it gives us a much clearer path to solving the problem faster.

* Lateralization:
    * For this section I chose to implement cross-class comparison to see if lateralization held.
    * This means that instead of rigoriously checking for each type of imagery (left fist vs right fist) which channel responds more and then using this information to see if lateralization holds, I chose to check by the channel. 
    * Checking at C4 if left fist imagery causes a bigger drop than right fist and so on. This is to test if each channel discriminates between the classes of imagery. 
    *This also happens to be the quicker method to implement and also coincidentally be the data I need for my linear classifier which is great because I need to push this and move on.