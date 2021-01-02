import os
# import sys
import numpy as np
# import matplotlib.pyplot as plt
from glob import glob
import cv2

year = "2016"
output_file_num = 62

os.chdir(f"/Users/greg/Pictures/FastFoto/{year}_Xmas")
set = []


def combine_imgs(img_files):
    imgs = []
    num_imgs = len(img_files)
    for img_file in img_files:
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgs.append(img)

    max_h = np.max([i.shape[0] for i in imgs])
    max_w = np.max([i.shape[1] for i in imgs])

    if max_h > max_w:
        # lay them out side by side
        layout = np.zeros((max_h, num_imgs * max_w, 3), np.uint8)
        for i, img in enumerate(imgs):
            h, w = img.shape[0:2]
            layout[:h, i*max_w:i*max_w+w] = img
    else:
        # lay them out below one another
        layout = np.zeros((max_h * num_imgs, max_w, 3), np.uint8)
        for i, img in enumerate(imgs):
            h, w = img.shape[0:2]
            layout[i*max_h:i*max_h+h, :w] = img

    return layout


def right_size(img):
    h, w, c = img.shape
    while h > 800 or w > 1200:
        img = cv2.resize(img, (w//2, h//2))
        h, w, c = img.shape
    return img


running_set = []
for i, file in enumerate(sorted(glob("*.png"))):
    running_set.append(file)
    combined = combine_imgs(running_set)
    rightsized = right_size(combined)
    rightsized = cv2.cvtColor(rightsized, cv2.COLOR_BGR2RGB)
    cv2.imshow("combined", rightsized)
    key = chr(cv2.waitKey(0))
    if key == "n":
        # remove the last image, composite the other ones and write them out
        combined = combine_imgs(running_set[:-1])
        recolored = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
        file_name = f"{year}_num{output_file_num}_card.png"
        cv2.imwrite(file_name, recolored)
        running_set = running_set[-1:]
        output_file_num += 1
    elif key == "x":
        # get rid of the one at the end, don't keep it.
        running_set = running_set[:-1]
    elif key == "q":
        # this is how I pull the rip cord and quit!
        break
    else:
        # for everything else, add an img
        pass

# handle the last one now!!
if len(running_set) > 0:
    combined = combine_imgs(running_set)
    recolored = cv2.cvtColor(combined, cv2.COLOR_BGR2RGB)
    file_name = f"{year}_num{output_file_num}_card.png"
    cv2.imwrite(file_name, recolored)
