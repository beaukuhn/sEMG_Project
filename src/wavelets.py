from pywt import wavedec, threshold
import matplotlib.pyplot as plt

wavelet = 'db2'  # also try coiflet5
level = 4  # decimation level
fs = 1000 # sampling rate

# 1) Get signal data
# 2)
universal_thresh = np.sqrt()

thresh =
threshed_sig = threshold(signal, , 'soft')
output = wavedec(signal, wavelet, level=level)
# output is [cA_n, cD_n, cD_n-1,...,cD2, cD1]
# >>> cD1
# array([-0.70710678, -0.70710678, -0.70710678, -0.70710678])
