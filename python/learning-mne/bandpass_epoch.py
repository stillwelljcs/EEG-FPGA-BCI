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
events, event_id = mne.events_from_annotations(raw, event_id={"T0":0, "T1":1, "T2":2})
channels = ["C3", "Cz", "C4"]

raw.plot(picks = channels, duration = 100, scalings="auto", block=True)
raw_bp = raw.copy().filter(l_freq=8.0, h_freq=30.0, fir_design='firwin')

raw_bp.plot(picks=channels, duration=100, scalings="auto", block=True)

epochs = mne.Epochs(raw_bp, events, event_id, tmin=0.5, tmax=2.5, baseline=None, picks=channels, preload=True)


print("EPOCHS T0")
print(epochs['T0'])
print(epochs['T0'].get_data().shape)

print("EPOCHS T1")
print(epochs['T1'])
print(epochs['T1'].get_data().shape)

print("EPOCHS T2")
print(epochs['T2'])
print(epochs['T2'].get_data().shape)

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

print(epochs.ch_names)

def compute_ERD():

    T = []

    for i in range(3):
        C3 = 0
        Cz = 0
        C4 = 0
        p = compute_power(i)
        for j in p:
            C3_c = j[0]
            Cz_c = j[1]
            C4_c = j[2]

            C3 += C3_c
            Cz += Cz_c
            C4 += C4_c

        C3 = C3/p.shape[0]
        Cz = Cz/p.shape[0]
        C4 = C4/p.shape[0]

        T.append([C3, Cz, C4])

    t1_check = True
    t2_check = True

    T1_drops = []
    T2_drops = []

    for k in range(3):
        if T[0][k] > T[1][k]:
            T1_drops.append((T[0][k]-T[1][k])/(T[0][k]))
        else:
            t1_check = False
            print(f"ERD fails at channel 0{k}")
        if T[0][k] > T[2][k]:
            T2_drops.append((T[0][k]-T[2][k])/(T[0][k]))
        else:
            t2_check = False
            print(f"ERD fails at channel 0{k}")

    if t1_check & t2_check:
        print("ERD passes for subject at T1 and T2 on all channels.")

        if T1_drops[2] > T2_drops[2] and T2_drops[0] > T1_drops[0]:
            print ("lateralization passes for subject on C3 and C4.")
        else:
            print ("lateralization failed on one or more channels, check values.")

compute_ERD()