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

    case "2":
        channel = input("Enter channel (C3, Cz, C4): ").strip()
        spec = raw.compute_psd(picks=channel, fmax=50, n_fft=320)
        psd, freqs = spec.get_data(return_freqs=True)

        alpha_range = (freqs >= 6) & (freqs <= 14)
        peak = freqs[alpha_range][psd[0,alpha_range].argmax()]
        print(f"{channel}: alpha peak at {peak:.1f} Hz")

        spec.plot(amplitude=False)
        plt.show(block=True)

    case _:
        print("Invalid option.")