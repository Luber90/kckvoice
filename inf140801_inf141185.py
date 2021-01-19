import sys
import scipy.io.wavfile
from scipy import *
import matplotlib.pyplot as plt

def data(name):
    samp, signal = scipy.io.wavfile.read('trainall/'+name)
    if(len(signal[0])==2):
        signal = [i[0] for i in signal]
    time = range(0, len(signal))
    time = [i/samp for i in time]
    return [time, signal]

def secToIndex(freq, t):
    return int(freq*t)


if __name__ == "__main__":
    t, s = data('001_K.wav')
    plt.plot(t, s)
    plt.show()
    print(signal[100])
    print(sys.argv[1])
