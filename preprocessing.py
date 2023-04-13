import numpy as np
from scipy import signal

from sklearn import preprocessing
from sklearn.decomposition import PCA


def handleOutliers(data):
    for col in data.columns:
          # First quartile (Q1)
          Q1 = np.percentile(data[col], 25, method = 'midpoint')

          # Third quartile (Q3)
          Q3 = np.percentile(data[col], 75, method = 'midpoint')
          
          upper = Q3 + 1.5 * (abs(Q3) + abs(Q1))
          lower = Q1 - 1.5 * (abs(Q3) + abs(Q1))

          counter = 0
          index = 0

          # replace outlying values with smallest or largest cap 
          for i in data[col]:
              if i > upper:
                    data[col][index] = upper
                    counter += 1
              if i < lower:
                    data[col][index] = lower
                    counter += 1
              index += 1
          print("changed this much stuff: ", counter)

def notchFilter(data, type):
  notch50 = []
  samp_freq = 125  # Sample frequency (Hz)
  notch_freq = type  # Frequency to be removed from signal (Hz)
  quality_factor = 20.0  # Quality factor

  # Design a notch filter using signal.iirnotch
  b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, samp_freq)
  freq, h = signal.freqz(b_notch, a_notch, fs=samp_freq)

  
  notch50.append(signal.filtfilt(b_notch, a_notch, data, axis=0))
  return notch50

def filterAndStandardize(data): 
  data = notchFilter(data, 50.0)
  data = notchFilter(data, 25.0)

  Filtered1_50 = []
  sos = signal.cheby2(12, 20, [1, 50], 'band', fs=125, output='sos')
  Filtered1_50.append(signal.sosfilt(sos, data, axis = 0))

  #Standardize
  standardizedNumList = []
  for data in Filtered1_50: 
      standardizedNumList.append(preprocessing.scale(data))

  return standardizedNumList


def applyPCA(componentNum, spatial_patterns):
  # Apply pca
  # Create a PCA object with the desired number of components
  pca = PCA(n_components=componentNum)

  # Fit the PCA model to the EEG data
  pca.fit(spatial_patterns)

  # Transform the EEG data to the new principal component space
  eeg_data_pca = pca.transform(spatial_patterns)

  # The transformed data is now in a new space with 3 components
  print(eeg_data_pca.shape)

  # Get the explained variance ratio of each component
  explained_variance_ratio = pca.explained_variance_ratio_

  print(explained_variance_ratio)
  print(sum(explained_variance_ratio))
  return eeg_data_pca
