from PIL import Image
import numpy as np
import os
import glob
import time
from scipy.stats import pearsonr
from scipy.spatial.distance import cosine, euclidean, cityblock


def read_img_color(file):
    width = 352
    height = 288
    with open(file, "rb") as imageFile:
        f = imageFile.read()
        array = bytearray(f)

    # im2 = Image.new("RGB", (352, 288))
    ind = 0
    comb = np.zeros((4, 4, 4))

    for y in range(0, height):
        for x in range(0, width):
            (r, g, b) = (array[ind], array[ind + height * width], array[ind + height * width * 2])
            ind += 1
            comb[int(r / 64), int(g / 64), int(b / 64)] += 1
            # im2.putpixel((x, y), (r, g, b))
    # im2.save("1.png")
    # im2.show()
    # print(comb.flatten())
    return comb.flatten()


def read_file_img2(file_path, outfile_npy):
    data_list = {}
    for filename in glob.glob(os.path.join(file_path, '*.rgb')):
        data_list[os.path.basename(filename)] = read_img_color(filename)
    np.save(outfile_npy, data_list)


def read_file_img(folder_path, folder_name, way):
    data_list = []
    # db 601, query 151
    loop_time = 601 if way == 1 else 151
    for _ in range(1, loop_time):
        filename = folder_path + "/" + folder_name + "/" + folder_name + '{0:03}'.format(_) + ".rgb"
        data_list.append(read_img_color(filename))
    np.save(folder_name + ".npy", data_list)


def read_query_file_and_compare(folder_path, folder_name, npy_file):
    data_list = []
    for _ in range(1, 151):
        filename = folder_path + "/" + folder_name + "/" + folder_name + '{0:03}'.format(_) + ".rgb"
        data_list.append(read_img_color(filename))
    db_list = np.load(npy_file)
    result = []
    for i in range(0, 451):
        temp = 0
        for j in range(0, 15):
            temp += calculate_similarity(2, data_list[10 * j], db_list[i + 10 * j])
        result.append(temp)
    print(result)


def compare(query_npy, db_npy):
    result = []
    for i in range(0, 451):
        temp = 0
        for j in range(0, 150):
            temp += calculate_similarity(1, query_npy[j], db_npy[i + j])
        result.append(temp / 150)
    print(result)


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


def test_read_file_img():
    start_time = time.time()

    end_time = time.time()
    print("it costs", end_time - start_time, "seconds")


def test_read_specific_npy_item():
    test_whole_path = "/Users/skywish/Downloads/Class/576/databse_videos/flowers/flowers001.rgb"
    test_base_path = "flowers001.rgb"
    print(read_specific_npy_item("flowers.npy", test_base_path))
    print("========")
    print(read_img_color(test_whole_path))


def test_get_result(index):
    n = np.load("traffic.npy")
    print(n[index])


if __name__ == "__main__":
    test_db_file_path = "/Users/skywish/Downloads/Class/576/databse_videos"
    test_db_file_name = "traffic"
    test_query_file_path = "/Users/skywish/Downloads/Class/576/query"
    test_query_file_name = "second"
    npy_file_name = "traffic.npy"
    traffic_npy = np.load("traffic.npy")
    second_npy = np.load("second.npy")

    t = time.time()
    # print(pearsonr(second_npy[0], traffic_npy[0])[0])
    compare(second_npy, traffic_npy)
    print("It costs", time.time() - t, "seconds")

    # t = time.time()
    # print(re.findall('\d+', "first001.rgb")[0])
    # test_get_result()
    # test_read_specific_npy_item()
    # test_read_file_img()
    # f1 = "/Users/skywish/Downloads/Class/576/databse_videos/test"
    # read_file_img(f1, "flowers.npy")
    # result = pearson_correlation_coefficients(read_img_color(file_path1), read_img_color(file_path2))
    # print(result)
    # # read_img_color(file_path1)
