import numpy as np
from scipy import signal

from sklearn import preprocessing
from sklearn.decomposition import PCA


def handleOutliers(data):
    counter = 0
    dataT = data.T
    for i in range(dataT.shape[1]):
          col = dataT[:, i]
          # First quartile (Q1)
          Q1 = np.percentile(col, 25, method = 'midpoint')

          # Third quartile (Q3)
          Q3 = np.percentile(col, 75, method = 'midpoint')
          
          upper = Q3 + 1.5 * (abs(Q3) + abs(Q1))
          lower = Q1 - 1.5 * (abs(Q3) + abs(Q1))

          index = 0

          # replace outlying values with smallest or largest cap 
          for i in col:
              if i > upper:
                    col[index] = upper
                    counter += 1
              if i < lower:
                    col[index] = lower
                    counter += 1
              index += 1
    print("changed this much stuff: ", counter)
    returnData = dataT.T
    return returnData, counter

def notchFilter(data, type):
  samp_freq = 125  # Sample frequency (Hz)
  notch_freq = type  # Frequency to be removed from signal (Hz)
  quality_factor = 20.0  # Quality factor

  # Design a notch filter using signal.iirnotch
  b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
  notch50 = signal.filtfilt(b_notch, a_notch, data, axis=0)

  assert(not np.array_equal(data, notch50))
  print("TODO: notch filter applied, for proper checks do a spectrogram")
  return notch50

def filterAndStandardize(data): 
  data = notchFilter(data, 50.0)
  data = notchFilter(data, 25.0)
  sos = signal.cheby2(12, 20, [1, 50], 'band', fs=125, output='sos')
  filtered = signal.sosfilt(sos, data, axis = 0)
  assert(not np.array_equal(data, filtered))

  #Standardize
  standardized = preprocessing.scale(filtered)
  assert(not np.array_equal(standardized, filtered))

  return standardized


def applyPCA(componentNum, spatial_patterns):
  # Apply pca
  # Create a PCA object with the desired number of components
  pca = PCA(n_components=componentNum)

  # Fit the PCA model to the EEG data
  pca.fit(spatial_patterns)

  # Transform the EEG data to the new principal component space
  eeg_data_pca = pca.transform(spatial_patterns)

  # Get the explained variance ratio of each component
  explained_variance_ratio = pca.explained_variance_ratio_

  print(explained_variance_ratio)
  print(sum(explained_variance_ratio))
  return eeg_data_pca
