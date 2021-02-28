import numpy as np 
# import scipy.io.wavfile as wav
import wavio as wav
from scipy import signal as sig
import scipy
# import stft
import matplotlib.pyplot as plt 
from scipy.fftpack import fftshift
import music_utils as mu
import os

#flow args
doTests = True

# directory args
current_dir = os.getcwd()
print('in directory ' + current_dir)
path = '\\data\\'
file = '055-AngelsInAmplifiers-ImAlright.wav'
print('makeing spectrogram for file: ' + file)

# import file
# see https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.io.wavfile.read.html
# returns sampling frequency and a numpy array

# new_file = mu.remove_metadata(current_dir, path, file)
# print('\n\nreceived new file' + new_file)

audio = wav.read(current_dir + path + file)

sound = np.array(audio.data)
sound = sound.transpose()

f, t, spec = sig.spectrogram(sound[0][:], audio.rate)

# GAIN
spec = spec * 1

#min max that boi
spec_min = 0
spec_max = 20000
cmap = 'winter'

# plot
plt.pcolormesh(t, f, spec, vmin=spec_min, vmax=spec_max, cmap=cmap)
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
