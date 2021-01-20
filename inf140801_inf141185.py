import sys
import scipy.io.wavfile
from scipy.signal import kaiser, decimate
import matplotlib.pyplot as plt
from numpy import *
import time
import warnings

warnings.simplefilter("ignore")

def data(name):
    samp, signal = scipy.io.wavfile.read(name)
    if(len(signal.shape)==2):
        signal = [i[0] for i in signal]
    time = range(0, len(signal))
    time = [i/samp for i in time]
    return [time, signal, samp]

def secToIndex(freq, t):
    return int(freq*t)

def cutt(t, s, duration, w):
    x = duration/15
    results = []
    s = (s-average(s))/std(s)
    for i in range(15):
        lIndex = secToIndex(w, i*x)
        rIndex = secToIndex(w, i*x+x)
        if(std(s[lIndex:rIndex])>0.75):
            results.extend(s[lIndex:rIndex])
    return results  
    
def program(name):
    t, s, w = data(name)
    time = len(s)/w
    signal = cutt(t, s, time, w)
    signalK = signal*kaiser(len(signal), 100)

    
    signalK1 = abs(fft.fft(signalK))
    
    
    freqsK = range(len(signalK1))
    freqsK = [i/len(signalK1)*w for i in freqsK]
    signalK1[:where(array(freqsK)>70)[0][0]] = 0

    hpik = copy(signalK1)
    for i in range(2, 6):
        d = decimate(signalK1, int(i))
        hpik[:len(d)] *= d
    if(freqsK[where(hpik==max(hpik))[0][0]] > 175):
        print('K')
    else:
        print('M')
    
    

if __name__ == "__main__":
    a = time.time()
    program(sys.argv[1])
    print(time.time()-a)

    
    
        
