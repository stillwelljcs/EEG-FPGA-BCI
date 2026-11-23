* mu range: frequencies filtered in the 8 - 12Hz range
* beta_range: frequencies filtered in the 13 - 30Hz range
* epoching: cutting trials around a cue time, for this chose (0.5-2.5s)
    * Shape: (trials, channels, time)

* extracting features: collapsing time into a single number
    * power = avg(signal^2) over time -> log
    * shape: (trials, channels)

* stacking bands together:
    * gives us a feature matrix A
    * shape: (45 trails, 6 features)
    * columns: C3_mu, Cz_mu, C4_mu, C3_beta, Cz_beta, C4_beta

* Labels -> y
    shape: (45,), each entry of T1 or T2

* Classifier (LDA):
    * Cross-validation -> accuracy (comparing to 64% threshold)


* Test 1:
    * Subject: S1
    * Features: 6(log mu + beta)
    * Window: 0.5s - 2.5s
    * CV: 5-fold * 1
    * Accuracy (mean +- std): 64.4 +- 13.0%
    * Notes: This is right at the chance threshold, high fold variance

    * what this means: a fold is a chunk of the data. The model studies all the other folds and leaves one fold for testing, then repeats this process for each fold. We chose 5 as the amount of folds because it provides a nice middle ground for noisiness in the data balanced with training set size, where a smaller set size can impact model accuracy out of 45 pieces of data . If we thought of each trial as a flashcard, the data the classifier "sees" to try to make its guess from is log power values from the 3 channels (C3, Cz, C4) bandpass filtered into mu and beta, so this means each "card" has 6 data points on it and the "back of the card" has the actual answer on it (T1 (left) or T2 (right)) 

        * We say that a p value < 0.05 (5%) is the cutoff for random chance of getting the ideal result, in other words if the p value is below this we can say that our model is not just getting lucky when it gets the desired results. A score of 29/45 on this data set indicates this so we say that 64.4% accuracy is the cutoff for random chance. The results of the CV gave us a score average of 64.44...5 % right at the threshold line for chance. This is not ideal for classifying data and I need to fix something.


* Test 2:
    * Subject: S1
    * Features: 6(log mu + beta)
    * Window: 0.5s - 2.5s
    * CV: 5-fold * 20
    * Accuracy (mean +- std): 70.7 +- 15.0%
    * Notes: Clearly above chance