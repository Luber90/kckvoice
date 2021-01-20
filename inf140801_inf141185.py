import sys
import scipy.io.wavfile
from scipy.signal import kaiser, decimate
import matplotlib.pyplot as plt
from numpy import *
import time
import warnings

warnings.simplefilter("ignore")

def data(name):
    samp, signal = scipy.io.wavfile.read('trainall/'+name)
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

    fig, ax = plt.subplots()
    hpik = copy(signalK1)
    for i in range(2, 6):
        d = decimate(signalK1, int(i))
        hpik[:len(d)] *= d
    if(freqsK[where(hpik==max(hpik))[0][0]] > 175):
        print(name+' K', 'K'==name[-5], freqsK[where(hpik==max(hpik))[0][0]])
        return 'K'==name[-5]
    else:
        print(name+' M', 'M'==name[-5], freqsK[where(hpik==max(hpik))[0][0]])
        return 'M'==name[-5]
    
    

if __name__ == "__main__":
    #program('037_K.wav')
    ile = 0
    for i in range(1,92):
        try:
            if i < 10:
                t0 = time.time()
                if program('00{}_K.wav'.format(i)):
                    print("czas: ", time.time()-t0)
                    ile += 1     
            else:
                t0 = time.time()
                if program('0{}_K.wav'.format(i)):
                    print("czas: ", time.time()-t0)
                    ile += 1   
        except:
            if i < 10:
                t0 = time.time()
                if program('00{}_M.wav'.format(i)):
                    print("czas: ", time.time()-t0)
                    ile += 1   
            else:
                t0 = time.time()
                if program('0{}_M.wav'.format(i)):
                    print("czas: ", time.time()-t0)
                    ile += 1
    print(ile/91)
    
        
