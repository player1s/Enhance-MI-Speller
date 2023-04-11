# Imports
from pylsl import StreamInlet, resolve_stream
import time
import numpy as np
import torch
from model import NeuralNetworkClassificationModel
from utilityFunctions import getData, getInference

def predictfromStream():

    # Load model
    input_dim  = 16
    output_dim = 3
    model = NeuralNetworkClassificationModel(input_dim,output_dim)
    model.load_state_dict(torch.load("Saved models/890342.pth"))

    # first resolve an EEG stream on the lab network
    print("looking for an EEG stream...")
    streams = resolve_stream('type', 'EEG')

    # create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    t_endOuter = time.time() + 5
    starterTime = time.time()

    while time.time() < t_endOuter:
        samples = getData(inlet)
        predictions = getInference(samples, model)

    finisherTime = time.time()
    print("total time taken", finisherTime - starterTime)