import matplotlib.pyplot as plt
import numpy as np
import wave
import sys
import time

from scipy import signal
from scipy.io import wavfile
from scipy.spatial import distance

# Run the program
def main():
    wavePath = '../query/Q3/Q3.wav'
    videos = ['musicvideo', 'traffic', 'flowers', 'interview', 'movie', 'sports', 'StarCraft']

    sampleRate, samples = wavfile.read(wavePath)
    monoSamples = stereoToMono(samples)
    spectogram = signal.spectrogram(monoSamples, fs = sampleRate)[2]

    audioData = np.load('data/audioData.npy')

    audioValues = {}
    for video in videos:
        monoSamples2 = audioData.item().get(video)

        length = len(samples);
        maxValue = 0.0
        # 31 and 10

        videoSimilarity = []
        for count in range(151):
            start = int(count * length / 50)
            testSamples = monoSamples2[start : start + length]
            testSpectogram = signal.spectrogram(testSamples, fs = sampleRate)[2]
            difference = 0.0
            if (len(testSamples) < length):
                newMonoSamples = monoSamples[0 : len(testSamples)]
                newSpectogram = signal.spectrogram(newMonoSamples, fs = sampleRate)[2]
                difference = findDifference(newSpectogram, testSpectogram)
            else:
                difference = findDifference(spectogram, testSpectogram)
            videoSimilarity.append(difference)
            if (difference > maxValue):
                maxValue = difference
        audioValues[video] = (videoSimilarity, maxValue)

    return audioValues

# Convert two-channel samples into one-channel samples
def stereoToMono(input):
    output = []
    for i in range(len(input)):
        d = input[i][0] / 2 + input[i][1] / 2
        output.append(d)
    return np.array(output, dtype='Int16')

# Find the difference between two spectograms
def findDifference(spectogramOrigin, spectogramNew):
    difference = 0.0
    size = len(spectogramOrigin)
    for i in range(size):
        dif = distance.cosine(spectogramNew[i], spectogramOrigin[i])
        difference += dif
    return 1 - difference / size

# Read all audio files and save mono samples into a .npy file
def preProcess():
    paths = ['databse_videos/musicvideo/musicvideo.wav', 'databse_videos/traffic/traffic.wav', 'databse_videos/flowers/flowers.wav', 'databse_videos/interview/interview.wav', 'databse_videos/movie/movie.wav', 'databse_videos/sports/sports.wav', 'databse_videos/starcraft/StarCraft.wav']
    audioData = {}
    for path in paths:
        passsampleRate, samples = wavfile.read(path)
        monoSamples = stereoToMono(samples)
        audioData[path.split('/')[2].split('.')[0]] = monoSamples
    np.save('audioData.npy', audioData)

if __name__ == "__main__":
    main()
