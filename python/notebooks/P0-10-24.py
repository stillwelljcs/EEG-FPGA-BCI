import mne
from mne.datasets import eegbci

# Subject 1:
files = eegbci.load_data(1, runs=[4, 8, 12]) # Subj 1, L/R fist movement data
raw = mne.concatenate_raws([mne.io.read_raw_edf(f, preload=True) for f in files]) #compiles multiple different recordings into one
eegbci.standardize(raw)  # use standard channel names
raw.set_montage("colin27_1005")
raw.plot(picks=["C3", "Cz", "C4"], duration=100, scalings="auto", block=True)

#Subject 2:
#files = eegbci.load_data(2, runs=[4, 8, 12])
#raw = mne.concatenate_raws([mne.io.read_raw_edf(f, preload=True) for f in files])