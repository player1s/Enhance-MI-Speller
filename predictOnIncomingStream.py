# Imports
from pylsl import StreamInlet, resolve_stream
import time
import numpy as np
import torch
from model import DynamicClassifier
from utilityFunctions import getData, getInference
from preprocessing import handleOutliers, filterAndStandardize, applyPCA

def predictfromStream():

    # Load model
    input_dim  = 3
    output_dim = 3
    model = DynamicClassifier(input_dim,output_dim)
    model = torch.load("Saved models/145836.pth")
    #model.load_state_dict(item)

    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    t_endOuter = time.time() + 5
    starterTime = time.time()

    while time.time() < t_endOuter:
        # obtain data
        samples = getData(inlet)
        print(len(samples))
        
        print(len(samples[0]))
        # preprocess data
        # outliers
        samples = handleOutliers(samples)
        outlierTime = time.time()
        # filter and standardize
        samples = filterAndStandardize(samples)
        filterTime = time.time()
        # pca
        samples = applyPCA(samples)
        pcaTime = time.time()

        print("outlier ", outlierTime - starterTime, "filter", filterTime - starterTime, "pca", pcaTime - starterTime)
        # make predictions
        predictions = getInference(samples, model)

    finisherTime = time.time()
    print("total time taken", finisherTime - starterTime)
    print("shape of samples: ", samples.shape)