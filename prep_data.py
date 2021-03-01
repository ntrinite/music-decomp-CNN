import music_utils as mu
import os
import numpy as np
curr_dir = os.getcwd()

# directories being used
compressed_dir = curr_dir + '\\data\\compressed_data\\'
stem_dir = curr_dir + '\\data\\stems\\'
song_dir = curr_dir + '\\data\\songs\\'
vox_dir = curr_dir + '\\data\\vox\\'

song_cst_dir = curr_dir + '\\data\\song_cst\\'
vox_cst_dir = curr_dir + '\\data\\vox_cst\\'

# mu.unzip_dir(compressed_dir, stem_dir)

it = 1

# loop through songs dir
for possible_stems in os.listdir(stem_dir):

    print("on " + str(it) + " of " + str(len(stem_dir)+1))
    it = it + 1

    stems = os.listdir(stem_dir + possible_stems)

    working_dir = stem_dir + possible_stems
    print(working_dir)
    # they might be in another directory, so 
    # loop until you find an audio file

    hasWav = False

    while(not hasWav):# or (not stems[0].endswith('.txt')) or (not stems[0].endswith('.mp3'))):
        # check if there are any wav files there
        for file in stems:
            if (file.endswith(".wav") or file.endswith(".mp3")):
                print("found song files")
                hasWav = True
                break     
        else:
            print("digging into: " +working_dir + '\\' + stems[0])
            working_dir = working_dir + '\\' + stems[0]
            stems = os.listdir(working_dir)
    
    song_name = '\\' + working_dir[working_dir.rindex('\\'):]
    # combine the files into a single wav
    # print(song_dir)

    # create songs folder if needed
    if (os.path.isfile(song_dir + song_name )):
        print("making directory: " + song_dir + song_name)
        os.mkdir(song_dir + song_name)

    mu.combine_stems(working_dir, song_dir +  song_name + ".wav")

    # pull out vox
    mu.pull_vox(working_dir, vox_dir, song_name)

# loop through songs file to create stfts:
songs = os.listdir(song_dir)
for song in songs:
    filename = song_cst_dir + song[:song.index('.')]
    f, t, spec = mu.wav_to_stft(song_dir+song)
    mu.save_stft_as_cst(filename, f,t , spec)

# loop through vox files and create stft:
songs = os.listdir(vox_dir)
for song in songs:
    filename = vox_cst_dir + song[:song.index('.')]
    f, t, spec = mu.wav_to_stft(vox_dir+song)
    mu.save_stft_as_cst(filename, f, t, spec)
