import mne
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from mne.datasets import eegbci


subj = input("Enter subject number: ")
files = eegbci.load_data(int(subj), runs=[4, 8, 12]) # load subject x L/R fist movement data
raw = mne.concatenate_raws([mne.io.read_raw_edf(f, preload=True) for f in files]) #compiles multiple different recordings into one
eegbci.standardize(raw)  # use standard channel names
raw.set_montage("colin27_1005")
events, event_id = mne.events_from_annotations(raw, event_id={"T1":1, "T2":2})
channels = ["C3", "Cz", "C4"]

menu = input("Plot raw recordings(1) or PSD(2): ").strip()
match menu:
    case "1":
        raw.plot(picks=channels, duration=100, scalings="auto", block=True)
        print(raw.annotations.count())

    case "2":
        channel = input("Enter channel (C3, Cz, C4): ").strip()
        spec = raw.compute_psd(picks=channel, fmax=50, n_fft=320)
        psd, freqs = spec.get_data(return_freqs=True)
        psd = psd[0]

        # alpha peak and 1/f slope
        f_range = (freqs >= 2) & (freqs <= 40)
        mu_range = (freqs >= 7) & (freqs <= 14)

        fit = f_range & ~mu_range

        x = np.log10(freqs[fit])
        y = np.log10(psd[fit])

        slope, intercept = np.polyfit(x, y, 1)

        background = intercept + slope * np.log10(freqs[mu_range])
        
        excess = np.log10(psd[mu_range]) - background

        i = excess.argmax()
        peak_freq = freqs[mu_range][i]
        peak_height = excess[i]

        if peak_height > 0.1:
            print(f"{channel}: peak at {peak_freq:.1f} Hz, {10**peak_height:.1f}x above 1/f background")
        else:
            print(f"{channel}: no clear peak in 7–14 Hz")

        #finding and plotting 1/f curve

        beta = -slope

        print(f"1/f exponent: {beta:.2f}")


        plt.loglog(freqs[1:], psd[1:])
        plt.loglog(freqs[fit], 10**(intercept + slope * x), "--")
        plt.show(block=True)

        spec.plot(amplitude=False)
        plt.show(block=True)

    case _:
        print("Invalid option.")