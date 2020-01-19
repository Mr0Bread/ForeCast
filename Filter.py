from pykalman import KalmanFilter
import numpy as np

kf = KalmanFilter(initial_state_mean=0, n_dim_obs=1)

measurements = [[1], [0], [0]]

print(kf.em(measurements).smooth([[2], [2], [2]])[0])


