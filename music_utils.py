import ffmpy
import os
# import ffmeg
import scipy.io.wavfile as wav
from pydub import AudioSegment
import zipfile
import wavio as wav
import numpy as np
from scipy import signal as sig

def save_stft_as_cst(fname, f, t, spec):
    output_array = spec #np.concatenate(f, t, spec)

    np.savetxt(fname + '.cst', output_array)

## performs the stft for a given file input path
## returns f, t, and spec
def wav_to_stft(path):
    print('makeing spectrogram for file: ' + path)

    audio = wav.read(path)

    sound = np.array(audio.data)
    sound = sound.transpose()

    f, t, spec = sig.spectrogram(sound[0][:], audio.rate)
    return f, t, spec

## pulls the vox file out from a directory filled 
## with stems and puts it into the output directory
def pull_vox(stem_dir, output_dir, song_name):
    print("getting vox for song: "+ song_name)
    files = os.listdir(stem_dir)

    addedToVox = False

    output = AudioSegment

    for file in files:
        # all the different types it might be labeled as 
        isvox = "vox" in file
        isvox = isvox or "VOX" in file 
        isvox = isvox or "Vox" in file 
        isvox = isvox or "vocal" in file
        isvox = isvox or "VOCAL" in file 
        isvox = isvox or "Vocal" in file
        isvox = isvox or "vocals" in file 
        isvox = isvox or "Vocals" in file 
        isvox = isvox or "VOCALS" in file 

        isvox = isvox and file.endswith(".wav")

        # add to vox output
        if (isvox and not addedToVox):
            output = AudioSegment.from_file(stem_dir + '\\' + file, format='wav')
            addedToVox = True
            print("adding vox: " + file)
        elif (isvox):
            curr = AudioSegment.from_file(stem_dir + '\\' + file, format='wav')
            output.overlay(curr, position=0)
            print("adding vox: " + file)
    
    if (addedToVox):
        print("Exporting" + song_name)
        output.export(output_dir + '\\' + song_name + '-vox.wav', format='wav')

## will unzip all folders in the path passed in
## then output the results into the passed in
## output_dir/zipname
def unzip_dir(working_dir, output_dir):
    zipped_list = os.listdir(working_dir)
    for file in zipped_list:
        if file.endswith(".zip"):
            print("uncrompressing: " + file)
            with zipfile.ZipFile(working_dir + file, 'r') as zip_ref:
                zip_ref.extractall(output_dir + file[:-4])
        else:
            print("ignoring file: " + file)
    
    print("unzip_dir complete")

## will take a directory path where all the stems
## are and take in a directory to output the new file
## as a wav file
def combine_stems(input_dir, output_dir):
    dir = os.listdir(input_dir)

    output = AudioSegment

    notSet = False

    for file in dir:
        if(not file.startswith('.') and (file.endswith(".wav") or file.endswith(".mp3"))):
            if (not notSet):
                output = AudioSegment.from_file(input_dir + '\\' + file)
                notSet = True
            else :
                curr = AudioSegment.from_file(input_dir + '\\' + file, format="wav")
                output = output.overlay(curr, position=0)
        
            print("adding file: " + file)
        else:
            print("excluding file: "+ file)
    output.export(output_dir, format="wav")


## takes in the path and file of a .wav file
## creates a new .wav file called 
## file-no-meta.wav in the the path passed in
def remove_metadata(working_dir, path, file):
    my_fp = working_dir + path + file
    new_file = file[: len(file) - 4] + '-no-meta.wav'
    my_new_fp =  working_dir + path + new_file
    print('creating new file: ' + path + new_file)
    print('from file: ' + path + file)

    # have to creat output file ahead of time

    cmd = working_dir + '\\ffmpeg\\bin\\ffmpeg.exe -i ' + my_fp + ' -map 0 -map_metadata -1 -c copy -y ' + my_new_fp
    print('\n\nRUNNING:\n' + cmd + '\n\n')
    os.system(cmd)
    # broke as fuck
    # create ffmpeg command
    # ff = ffmpy.FFmpeg(
    #     executable='ffmpeg/bin/ffmpeg.exe',
    #     inputs={path + file : None},
    #     outputs={path + new_file : ['-map', '0', '-​map_metadata', '-c:v', 'copy', '-c:a', 'copy']}
    # )
    # # call comand
    # ff.cmd
    # ff.run()
    return new_file

# takes in stereo signal
# def make_mono(audio):
#     ffmpeg.input()
