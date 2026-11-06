* Why is finding the alpha peak even relevant?

  * the channel mu peak is the mu rhythm (motor cortex) peak here, which is not the posterior alpha usually referenced in most google searches. 
  * mu power drops during motor imagery, this is how my classifier will detect "movement" in the eeg data.
  * used to customize filtering per-subject
  * the 1/f curve is considered aperiodic because it lacks any kind of repeating rhythm or distinct peak frequency and goes down at a semi predictable rate
  * mu is periodic becuase it is a rhythm that is roughly a sin wave, which during the recording tested, happened to hover around 13 cycles per second in the time domain. The amplitude of this wave is the voltage reading in micro volts


* PSD is a spectrum which is a result of all the constituent spectrums power at each frequency summed together since power is always > 0, this is an average over the entire reading. to make this more intuitive to a human reader would add a third axis (Z) to serve as time then would see a 3d map of the P against f at each moment (Spectrogram).

* 1/f slope calculation: 
    * I identified and made variables for the general range of the frequencies and the range where alpha(mu) peak tends to be found and then created a bitmask for general range that excludes the mu peak range. 
    * We apply log_10 to each side of the power-frequency relationship data to make the relationship linear and since it is still relatively scattered due to noise (didnt take beta range out on this one) we run a least squares regression on the data to find a line of best fit for the curve.

* Having issue with finding alpha peak above 1/f noise on graphs where the slope is constantly moving downward so numpy just takes the lower bound of the search range to be the peak which is not accurate.

    * In order to fix this we need to fit the 1/f line in log space and substract it away from the log spectrum, this will make the alpha peak appear as a local maximum above zero.
      * For this we apply a bit mask over the entire graph (excluding zero) and remove the general alpha peak region (7-14Hz) so that peak region doesnt erroneously pull that line upward.


* Results of my run

  * ran for subject 1, on the C3 channel
  * aperiodic exponent = 1.64
  * peak: ~13Hz
  * 23 T1 annotations, 22 T2 annotations (51.11% : 48.89%) ratio, balanced for my classifer.