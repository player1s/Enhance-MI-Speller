import time
import torch
import numpy as np

# get data func
def getData(inlet):
    #pull once to initialize np arr
    sample, timestamp = inlet.pull_sample()
    items = np.asarray(sample)
    items = np.reshape(items, (-1, 16))
    t_end = time.time() + 0.5

    while time.time() < t_end:
        # get a new sample 
        sample, timestamp = inlet.pull_sample()
        sampleInArr = np.asarray(sample)
        sampleInArr = np.reshape(sampleInArr, (-1, 16))
        items = np.append(items, sampleInArr, axis=0)
    return items

# get inference func (longest time it took on pracc data was 0.003 sec. that means i can have shorter data collection 
# )
def getInference(samples, model):
    tensor = torch.tensor(samples)
    predictions = []
    final = []
    with torch.no_grad():
        predictions = model(tensor)

    predictions = predictions.numpy()

    for i in range(len(predictions)):
            final.append(np.argmax(predictions[i]))
    final = np.array(final)    
    print("the most occuring predicted class in the samples:", np.argmax(np.bincount(final)), "with percentage:", np.bincount(final)[np.argmax(np.bincount(final))] / len(final), "out of:", len(final))
    mostOccuringClass = np.argmax(np.bincount(final))

    return final, mostOccuringClass