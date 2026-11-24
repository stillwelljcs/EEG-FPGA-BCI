import matplotlib.pyplot as plt
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold, cross_val_score
from sklearn.model_selection import permutation_test_score
from bandpass_epoch import load_subject, bandpass, make_epochs, compute_power, CHANNELS

raw, events, event_id = load_subject(1)
epochs_mu = make_epochs(bandpass(raw, 8.0, 12.0), events, event_id)
epochs_beta = make_epochs(bandpass(raw, 13.0, 30.0), events, event_id)

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
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=20, random_state=0)
scores = cross_val_score(lda, X, y, cv=cv)

score, perm_scores, pvalue = permutation_test_score(
    lda, X, y, cv=cv, n_permutations=1000, random_state=0
)

print(f"Scores raw: {scores}")
print(f"Scores average: {scores.mean()}")
print(f"Scores standard deviation: {scores.std()}")

print(f"Permutation Test Score: {score}")
print(f"Permutation Test P-Value: {pvalue}")
print(f"Permutation Test Average: {perm_scores.mean()}")