from predictOnIncomingStream import predictfromStream
from model import BasicClassifier
while(True):
    choice = int(input("press 1 for: prediction on incoming stream \npress 9 for: exit\n:"))

    if choice == 1: 
        print("predict on incoming stream starting")
        predictfromStream()
    

    if choice == 9: 
        print("Exiting")
        break
