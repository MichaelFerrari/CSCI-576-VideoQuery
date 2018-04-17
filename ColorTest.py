from PIL import Image
import numpy as np
from scipy.stats.stats import pearsonr


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
    return comb


def pearson_correlation_coefficients(comb1, comb2):
    return np.corrcoef(comb1.flatten(), comb2.flatten())[0, 1]


if __name__ == "__main__":
    file_path1 = "/Users/skywish/Downloads/Class/576/query/first/first001.rgb"
    file_path2 = "/Users/skywish/Downloads/Class/576/query/first/first002.rgb"
    result = pearson_correlation_coefficients(read_img_color(file_path1), read_img_color(file_path2))
    print(result)
    # read_img_color(file_path1)
