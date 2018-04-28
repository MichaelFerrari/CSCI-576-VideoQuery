import io
import os
import glob
import csv
from google.cloud import vision
from google.cloud.vision import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/skywish/Downloads/CS576-Final-50c078a717bf.json"

# Instantiates a client
client = vision.ImageAnnotatorClient()


def read_img_label(file_path, csv_path="/Users/skywish/Downloads/Class/576/img_labels.csv"):
    for filename in glob.glob(os.path.join(file_path, '*.rgb')):
        # Loads the image into memory
        with io.open(filename, 'rb') as image_file:
            content = image_file.read()

        image = types.Image(content=content)

        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        with open(csv_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows("{0} ".format())
        print(labels)
        # print('Labels:')
        # for label in labels:
        #     print(label.description)


if __name__ == "__main__":
    # file_path1 = "/Users/skywish/Downloads/Class/576/databse_videos/flowers"
    # read_img_label(file_path1)
    with open("/Users/skywish/Downloads/Class/576/img_labels.csv", 'w', newline='') as f:
        column1 = "File Names"
        column2 = "Feature Values"
        fieldnames = [column1, column2]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
