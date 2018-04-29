from PIL import Image
import numpy as np
import os
import io
import glob
import time
import cv2
import json
import math
import wave
import sys
import time

from scipy import signal
from scipy.io import wavfile
from scipy.stats import pearsonr
from scipy.spatial.distance import cosine, euclidean, cityblock


def read_img_color(file):
    width = 352
    height = 288
    with open(file, "rb") as imageFile:
        f = imageFile.read()
        array = bytearray(f)

    img = Image.new("RGB", (352, 288))
    ind = 0
    comb = np.zeros((4, 4, 4))

    for y in range(height):
        for x in range(width):
            (r, g, b) = (array[ind], array[ind + height * width], array[ind + height * width * 2])
            ind += 1
            comb[int(r / 64), int(g / 64), int(b / 64)] += 1
            img.putpixel((x, y), (r, g, b))
    return img, comb.flatten()


def read_img_motion(folder_path, folder_name):
    old_path = folder_path + '/' + folder_name + '/' + folder_name + '001.rgb'
    query_array = np.zeros(149)
    img, _ = read_img_color(old_path)
    img = np.asarray(img)
    old_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for index in range(2, 151):
        new_path = folder_path + '/' + folder_name + '/' + folder_name + '{0:03}'.format(index) + '.rgb'
        img, _ = read_img_color(new_path)
        img = np.asarray(img)
        new_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(old_image, new_image)
        old_image = new_image
        query_array[index - 2] = np.mean(diff)
    result = ""
    for i in range(148):
        result += str(query_array[i]) + ","
    result += str(query_array[148])
    print(result)
    return result


def read_img_color_and_motion(folder_path, folder_name, way):
    """

    :param folder_path:
    :param folder_name:
    :param way: 1 is for database data, else for query data
    :return:
    """
    # db 601, query 151
    loop_time = 601 if way == 1 else 151
    # color feature list
    data_list = []
    # motion list
    query_array = np.zeros(loop_time - 2)

    # handle first img
    img, comb = read_img_color(folder_path + "/" + folder_name + "/" + folder_name + "001.rgb")
    data_list.append(comb)
    img = np.asarray(img)
    old_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # handle rest
    for index in range(2, loop_time):
        filename = folder_path + "/" + folder_name + "/" + folder_name + '{0:03}'.format(index) + ".rgb"
        img, comb = read_img_color(filename)
        data_list.append(comb)
        img = np.asarray(img)
        new_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(old_image, new_image)
        old_image = new_image
        query_array[index - 2] = np.mean(diff)
    # result = ""
    # for i in range(0, 148):
    #     result += str(query_array[i]) + ","
    # result += str(query_array[148])
    return data_list, query_array
    # np.save(folder_name + ".npy", data_list)


def compare_color(query_list):
    databases = ["flowers", "interview", "movie", "musicvideo", "sports", "starcraft", "traffic"]
    color_result = {}
    for db in databases:
        db_npy = np.load('data/%s.npy' % db)
        result = []
        for i in range(451):
            temp = 0
            for j in range(150):
                temp += calculate_similarity(2, query_list[j], db_npy[i + j])
            result.append(temp / 150)
        color_result[db] = (max(result), result)
    print(color_result)
    return color_result


def compare_motion(query_array):
    database = ["flowers", "interview", "movie", "musicvideo", "sports", "starcraft", "traffic"]
    db_array = np.zeros((7, 599))
    frame_array = np.zeros((7, 451))
    motion_result = {}
    for index in range(len(database)):
        file_path = '/Users/skywish/Projects/Python/CSCI-576-VideoQuery/data/' + database[index] + 'motion.txt'
        with open(file_path, "r") as f:
            array = f.read().split(",")
            results = list(map(float, array))
            db_array[index] = np.asarray(results)
    for i in range(7):
        for j in range(451):
            # frame_array[i][j] = np.sum(np.absolute(np.subtract(db_array[i][j:j + 149], query_array)))
            frame_array[i][j] = diff_to_coefficient(
                np.sum(np.absolute(np.subtract(db_array[i][j:j + 149], query_array))))
        motion_result[database[i]] = (np.amax(frame_array[i]), frame_array[i].tolist())
        # motion_result[database[i]] = (frame_array[i], np.amax(frame_array[i]))
    print(motion_result)
    return motion_result


def diff_to_coefficient(sample):
    if sample > 10:
        return 0.95 / math.log10(sample)
    return 1 - 0.005 * sample


def compare_audio(wave_path):
    database = ['musicvideo', 'traffic', 'flowers', 'interview', 'movie', 'sports', 'starcraft']

    sample_rate, samples = wavfile.read(wave_path)
    mono_samples = stereo_to_mono(samples)
    spectogram = signal.spectrogram(mono_samples, fs=sample_rate)[2]

    audio_data = np.load('data/audioData.npy')

    audio_values = {}
    for video in database:
        mono_samples2 = audio_data.item().get(video)

        length = len(samples)
        max_value = 0.0
        # 31 and 10

        video_similarity = []
        for count in range(151):
            start = int(count * length / 50)
            test_samples = mono_samples2[start: start + length]
            test_spectogram = signal.spectrogram(test_samples, fs=sample_rate)[2]
            difference = 0.0
            if len(test_samples) < length:
                new_mono_samples = mono_samples[0: len(test_samples)]
                new_spectogram = signal.spectrogram(new_mono_samples, fs=sample_rate)[2]
                difference = find_difference(new_spectogram, test_spectogram)
            else:
                difference = find_difference(spectogram, test_spectogram)
            video_similarity.append(difference)
            if difference > max_value:
                max_value = difference
        audio_values[video] = (max_value, video_similarity)
    print(audio_values)
    return audio_values


# Convert two-channel samples into one-channel samples
def stereo_to_mono(sample_input):
    output = []
    for i in range(len(sample_input)):
        d = sample_input[i][0] / 2 + sample_input[i][1] / 2
        output.append(d)
    return np.array(output, dtype='Int16')


# Find the difference between two spectograms
def find_difference(spectogram_origin, spectogram_new):
    difference = 0.0
    size = len(spectogram_origin)
    for i in range(size):
        dif = cosine(spectogram_new[i], spectogram_origin[i])
        difference += dif
    return 1 - difference / size


# Read all audio files and save mono samples into a .npy file
def pre_process():
    videos = ['musicvideo', 'traffic', 'flowers', 'interview', 'movie', 'sports', 'starcraft']
    paths = []
    for _ in videos:
        paths.append('/Users/skywish/Downloads/Class/576/databse_videos/%s/%s.wav' % (_, _))
    audio_data = {}
    for _ in range(len(videos)):
        pass_sample_rate, samples = wavfile.read(paths[_])
        mono_samples = stereo_to_mono(samples)
        audio_data[videos[_]] = mono_samples
    np.save('audioData.npy', audio_data)


def read_specific_npy_item(npy_path, file_basename):
    n1 = np.load(npy_path)
    return n1.item().get(file_basename)


def calculate_similarity(way, comb1, comb2):
    # https://docs.scipy.org/doc/scipy/reference/spatial.distance.html
    # pearson_correlation_coefficients2
    if way == 1:
        return pearsonr(comb1, comb2)[0]
        # return np.corrcoef(comb1, comb2)[0, 1]
    # cosine_similarity
    elif way == 2:
        return 1 - cosine(comb1, comb2)
    # Euclidean distance
    elif way == 3:
        return euclidean(comb1, comb2)
    # City Block (Manhattan) distance.
    elif way == 4:
        return cityblock(comb1, comb2)


def test_read_query_data(folder_path, folder_name):
    query_data_list = []
    for _ in range(1, 3):
        filename = folder_path + "/" + folder_name + "/" + folder_name + '{0:03}'.format(_) + ".rgb"
        query_data_list.append(read_img_color(filename))
    print(query_data_list[0])


def test_read_specific_npy_item():
    test_whole_path = "/Users/skywish/Downloads/Class/576/databse_videos/flowers/flowers001.rgb"
    test_base_path = "flowers001.rgb"
    print(read_specific_npy_item("flowers.npy", test_base_path))
    print("========")
    print(read_img_color(test_whole_path))


def test_get_result(index):
    n = np.load("traffic.npy")
    print(n[index])


def data_to_json(data):
    # Write JSON file
    with open('data/data.json', 'w', encoding='utf8') as outfile:
        str_ = json.dumps(data,
                          indent=4, sort_keys=True,
                          separators=(',', ': '), ensure_ascii=False)
        outfile.write(str_)


def test():
    test_db_file_path = "/Users/skywish/Downloads/Class/576/databse_videos"
    test_db_file_name = "traffic"
    test_query_file_path = "/Users/skywish/Downloads/Class/576/query"
    test_query_file_name = "second"
    npy_file_name = "traffic.npy"
    wave_path = '/Users/skywish/Downloads/Class/576/query/first/first.wav'
    query = ["first", "second"]
    n1 = np.load('data/flowers.npy')
    n2 = np.load('data/first.npy')
    result = dict()
    data = dict()
    # get motion
    t = time.time()
    with open("data/queryfirst.txt", "r") as f:
        array = f.read().split(",")
        results = list(map(float, array))
        query = np.asarray(results)
    motion = compare_motion(query)
    # get color
    color = compare_color(n2)
    # get audio
    audio = compare_audio(wave_path)
    print("It costs %f seconds to process." % (time.time() - t))
    motion_coefficients = 0.55
    color_coefficients = 0.35
    audio_coefficients = 0.1
    database = ['musicvideo', 'traffic', 'flowers', 'interview', 'movie', 'sports', 'starcraft']
    t = time.time()
    for db in database:
        (motion_best, motion_array) = motion[db]
        (color_best, color_array) = color[db]
        (audio_best, audio_array) = audio[db]
        item = dict()
        array = []
        item['motion'] = round(motion_best, 2)
        item['color'] = round(color_best, 2)
        item['audio'] = round(audio_best, 2)
        for i in range(451):
            frame_value = motion_coefficients * motion_array[i] + color_coefficients * color_array[i] + \
                          audio_coefficients * audio_array[int(i / 3)]
            array.append(round(frame_value, 2))
        item['array'] = array
        item['matchPerc'] = max(array)
        data[db] = item
    result['data'] = data
    data_to_json(result)
    print("It costs %f seconds to process." % (time.time() - t))


def main():
    test_query_file_path = "/Users/skywish/Downloads/Class/576/query"
    test_query_file_name = "second"
    wave_path = '/Users/skywish/Downloads/Class/576/query/first/first.wav'
    di = dict()
    motion_coefficients = 0.5
    color_coefficients = 0.3
    audio_coefficients = 0.2
    t = time.time()
    data_list, query_array = read_img_color_and_motion(test_query_file_path, test_query_file_name, 2)
    print("It costs", time.time() - t, "seconds to pre process color and motion")
    t = time.time()
    di['motion'] = compare_motion(query_array)
    print("It costs", time.time() - t, "seconds to analyze motion")
    t = time.time()
    di['color'] = compare_color(data_list)
    print("It costs", time.time() - t, "seconds to analyze color")
    t = time.time()
    di['audio'] = compare_audio(wave_path)
    print("It costs", time.time() - t, "seconds to analyze audio")
    t = time.time()
    data_to_json(di)
    print("It costs", time.time() - t, "seconds to save to json file")


if __name__ == "__main__":
    test()
