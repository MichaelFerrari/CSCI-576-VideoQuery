from PIL import Image
import numpy as np
import cv2
import sys
from io import BytesIO

def read_img_color(file):
    width = 352
    height = 288
    with open(file, "rb") as imageFile:
        f = imageFile.read()
        array = bytearray(f)
    im2 = Image.new("RGB", (352, 288))
    ind = 0
    number = 101376
    for y in range(0, height):
        for x in range(0, width):
            (r, g, b) = (array[ind], array[ind + number], array[ind + 2 * number])
            im2.putpixel((x, y), (r, g, b))
            ind += 1
    return im2
def funtion(filenam)
query_array = np.zeros((149))
old_path = 'new queries/From Searching Content/Q5/Q5_001.rgb'
img = read_img_color(old_path)
img.show()
img = np.asarray(img)
old_Image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
index = 2
while True:
    newPath = "new queries/From Searching Content/Q5/Q5_" + (str("%03d" % (index,))) + ".rgb"
    img = read_img_color(newPath)
    img = np.asarray(img)
    new_Image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(old_Image, new_Image)
    old_Image = new_Image
    query_array[index - 2] = np.mean(diff)
    index = index + 1
    if index > 150:
        break
result = ""
for i in range(0, 149):
    if(i != 148):
        result += str(query_array[i]) + ","
    else:
        result += str(query_array[i])
print (result)
