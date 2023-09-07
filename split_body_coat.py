import cv2
import numpy as np
import os

def process_image(img, coat_out, body_out):
    all_values = []
    coat = np.zeros_like(img)
    body = np.zeros_like(img)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if all(img[i][j] != 0):
                all_values.append(int(img[i][j][2]) - int(img[i][j][0]) - int(img[i][j][1]))

    m = np.mean(all_values)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if int(img[i][j][2]) - int(img[i][j][0]) - int(img[i][j][1]) <= min(m, -45):
                coat[i][j] = img[i][j]
            else:
                body[i][j] = img[i][j]

    cv2.imwrite(coat_out, coat)
    cv2.imwrite(body_out, body)

path_in = './t1/'
coat_out = './4cls_coat/'
body_out = './4cls_body/'

for img_path in os.listdir(path_in):
    img = cv2.imread(path_in + img_path)
    process_image(img, coat_out + img_path, body_out + img_path)
    print(img_path)
