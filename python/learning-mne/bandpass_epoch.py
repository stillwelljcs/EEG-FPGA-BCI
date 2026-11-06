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

raw.plot(picks = channels, duration = 100, scalings="auto", block=True)
raw_bp = raw.copy().filter(l_freq=8.0, h_freq=30.0, fir_design='firwin')

raw_bp.plot(picks=channels, duration=100, scalings="auto", block=True)

epochs = mne.Epochs(raw_bp, events, event_id, tmin=0.5, tmax=2.5, baseline=None, picks=channels, preload=True)

print("EPOCHS")
print(epochs['T1'])
print(epochs['T1'].get_data().shape)

#ERD

def compute_power(label):
    d = epochs[f"T{label}"].get_data()
    n_trials = d.shape[0]
    n_ch = d.shape[1]
    power = np.zeros((n_trials, n_ch))

    for t in range(n_trials):
        for c in range(n_ch):
            row = d[t,c]
            r_s = (row**2)
            power[t, c] = r_s.sum()/len(row)

    return(power)

p0 = compute_power(0)
p1 = compute_power(1)
p2 = compute_power(2)