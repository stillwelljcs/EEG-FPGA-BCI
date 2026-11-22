import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, cross_val_score
from bandpass_epoch import *

raw_bp_mu = raw.copy().filter(l_freq=8.0, h_freq=12.99, fir_design='firwin')
raw_bp_beta = raw.copy().filter(l_freq=13.0, h_freq=30.0, fir_design='firwin')

epochs_mu = mne.Epochs(raw_bp_mu, events, event_id, tmin=0.5, tmax=2.5, baseline=None, picks=channels, preload=True)
epochs_beta = mne.Epochs(raw_bp_beta, events, event_id, tmin=0.5, tmax=2.5, baseline=None, picks=channels, preload=True)

mu_features = epochs_mu['T1','T2']
beta_features = epochs_beta['T1','T2']

mu_p_t1 = compute_power(1, mu_features)
mu_p_t2 = compute_power(2, mu_features)

beta_p_t1 = compute_power(1, beta_features)
beta_p_t2 = compute_power(2, beta_features)

log_10_mu_t1 = np.log10(mu_p_t1)
log_10_mu_t2 = np.log10(mu_p_t2)

log_10_beta_t1 = np.log10(beta_p_t1)
log_10_beta_t2 = np.log10(beta_p_t2)

# x and y for linear discriminant analysis:

mu = np.vstack([log_10_mu_t1, log_10_mu_t2])
beta = np.vstack([log_10_beta_t1, log_10_beta_t2])
X = np.hstack([mu, beta])
y = np.array([0]*23 + [1]*22)

lda = LinearDiscriminantAnalysis()
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
scores = cross_val_score(lda, X, y, cv=cv)

print(f"Scores raw: {scores}")
print(f"Scores average: {scores.mean()}")
print(f"Scores standard deviation: {scores.std()}")