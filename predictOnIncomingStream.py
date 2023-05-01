# Imports
from pylsl import StreamInlet, resolve_stream
import time
import numpy as np
import torch
from utilityFunctions import getData, getInference
from preprocessing import handleOutliers, filterAndStandardize, applyPCA
from model import BasicClassifier

def predictfromStream():

    # Load model
    model = BasicClassifier(3,3)
    modelState = torch.load("Saved models/895083.pth")['model_state']
    print("type", modelState['input_layer.weight'].dtype)
    model.load_state_dict(modelState)
    #model = full['model_architecture']
    #todo: need to figure out smooth model loading. Got incompatible keys. got to review if the model class here match loads
    #model = model.load_state_dict(full['model_state'])
    model.eval()

    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    t_endOuter = time.time() + 5
    starterTime = time.time()

    while time.time() < t_endOuter:
        starterTimeInner = time.time()
        # obtain data
        samples = getData(inlet)
        # preprocess data
        # outliers
        samplesOutlier, changedAmount = handleOutliers(samples)
        if changedAmount == 0:
            assert(np.array_equal(samples, samplesOutlier))
        else:
            try:
                assert(not np.array_equal(samples, samplesOutlier))
            except AssertionError: 
                print("Issue: the returned array after outlier removal seems to be the same as the one supplied, though outliers were handled.")
                print(np.array_equal(samples, samplesOutlier))
                #print("in unprocessed but not processed: ", np.setdiff1d(samples, samplesOutlier))
                #print("in processed but not unprocessed: ", np.setdiff1d(samplesOutlier, samples))

        outlierTime = time.time()

        # filter and standardize
        samples = filterAndStandardize(samples)
        filterTime = time.time()
        # pca
        samples = applyPCA(3, samples)
        pcaTime = time.time()

        print("outlier ", outlierTime - starterTimeInner, "filter", filterTime - outlierTime, "pca", pcaTime - filterTime)
        # make predictions
        predictions, mostOccuringClass = getInference(samples, model)

    finisherTime = time.time()
    print("total time taken", finisherTime - starterTime)
    print("shape of samples: ", samples.shape)