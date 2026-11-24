import mne
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
from mne.datasets import eegbci

CHANNELS = ["C3", "Cz", "C4"]
EVENT_ID = {"T0": 0, "T1": 1, "T2": 2}

def load_subject(subj, runs=(4, 8, 12)):
    """Load and concatenate a subject's L/R fist imagery runs."""
    files = eegbci.load_data(int(subj), runs=list(runs))
    raw = mne.concatenate_raws([mne.io.read_raw_edf(f, preload=True) for f in files])
    eegbci.standardize(raw)  # use standard channel names
    raw.set_montage("colin27_1005")
    events, event_id = mne.events_from_annotations(raw, event_id=EVENT_ID)
    return raw, events, event_id


def bandpass(raw, l_freq, h_freq):
    """Return a bandpass-filtered copy of raw."""
    return raw.copy().filter(l_freq=l_freq, h_freq=h_freq, fir_design="firwin")


def make_epochs(raw, events, event_id, channels=CHANNELS, tmin=0.5, tmax=2.5):
    """Cut raw into epochs around each cue."""
    return mne.Epochs(raw, events, event_id, tmin=tmin, tmax=tmax,
                      baseline=None, picks=channels, preload=True)

def compute_power(label, epochs_set):
    d = epochs_set[f"T{label}"].get_data()
    n_trials = d.shape[0]
    n_ch = d.shape[1]
    power = np.zeros((n_trials, n_ch))

    for t in range(n_trials):
        for c in range(n_ch):
            row = d[t,c]
            r_s = (row**2)
            power[t, c] = r_s.sum()/len(row)

    return(power)

def compute_ERD(epochs):

    T = []

    for i in range(3):
        C3 = 0
        Cz = 0
        C4 = 0
        p = compute_power(i, epochs)
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

if __name__ == "__main__":
    subj = input("Enter subject number: ")
    raw, events, event_id = load_subject(subj)
    raw_bp = bandpass(raw, 8.0, 30.0)
    epochs = make_epochs(raw_bp, events, event_id)
    compute_ERD(epochs)