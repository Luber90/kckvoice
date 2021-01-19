import sys
import scipy.io.wavfile
from scipy.signal import kaiser, decimate
import matplotlib.pyplot as plt
from numpy import *

def data(name):
    samp, signal = scipy.io.wavfile.read('trainall/'+name)
    if(len(signal.shape)==2):
        signal = [i[0] for i in signal]
    time = range(0, len(signal))
    time = [i/samp for i in time]
    return [time, signal, samp]

def secToIndex(freq, t):
    return int(freq*t)

def program(name):
    t, s, w = data(name)
    time = len(s)/w
    lMargin = secToIndex(w, 0.5)
    rMargin = secToIndex(w, 2.0)
    
    signal = s[lMargin:rMargin]
    signalK = s[lMargin:rMargin]*kaiser(len(signal), 100)

    signal1 = abs(fft.fft(signal))     
    #signal1 = [i/len(signal1)*w for i in signal1]
    #signal1[0]=signal1[0]/2
    
    signalK1 = abs(fft.fft(signalK))     
    #signalK1 = [i/len(signalK1)*w for i in signalK1]
    #signalK1[0]=signalK1[0]/2
    
    #freqs = range(len(signal1))
    #freqs = [i/len(signal1)*w for i in freqs]
    freqsK = range(len(signalK1))
    freqsK = [i/len(signalK1)*w for i in freqsK]
    #ax.plot(freqsK, signalK1)
    #plt.show()
    hpik = copy(signalK1)
    for i in range(2, 6):
        d = decimate(signalK1, int(i))
        hpik[:len(d)] *= d
    if(freqsK[where(hpik==max(hpik))[0][0]] > 175):
        print(name+' K', 'K'==name[-5], freqsK[where(hpik==max(hpik))[0][0]], time)
        return 'K'==name[-5]
    else:
        print(name+' M', 'M'==name[-5], freqsK[where(hpik==max(hpik))[0][0]], time)
        return 'M'==name[-5]
    
    

if __name__ == "__main__":
    program('003_K.wav')
    ile = 0
    for i in range(1,92):
        try:
            if i < 10:
                if program('00{}_K.wav'.format(i)):
                    ile += 1     
            else:
                if program('0{}_K.wav'.format(i)):
                    ile += 1   
        except:
            if i < 10:
                if program('00{}_M.wav'.format(i)):
                    ile += 1   
            else:
                if program('0{}_M.wav'.format(i)):
                    ile += 1
    print(ile/91)
    
        
