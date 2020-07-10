#!/usr/bin/python3
# -*- coding: utf-8 -*-

from skimage.metrics import structural_similarity as ssim
from tkinter.filedialog import askdirectory
from tkinter import Tk
import numpy as np
import cv2
import sys
import os


def printProgressBar(iteration, total, prefix='Progress:', suffix='Complete', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    if iteration == total:
        print()

def mse(first_img, second_img):
    err = np.sum((first_img.astype("float") - second_img.astype("float")) ** 2)
    err /= float(first_img.shape[0] * first_img.shape[1])
    return err

if __name__ == '__main__':
    args = sys.argv[1:]
    directory = ""
    if len(args) == 0:
        Tk().withdraw()
        directory = askdirectory()
    else:
        directory = os.path.abspath(args[0])
	
    image_data = []

    print("Loading Image, Grayscaling and Rescaling")
    printProgressBar(0, len(os.listdir(directory)))
    for i, rel_path in enumerate(os.listdir(directory)):
        path = directory + "/" + rel_path
        img = cv2.imread(path, 0)
        if img is None:
            printProgressBar(i + 1, len(os.listdir(directory)))
            continue
        image_data.append(
            [path, cv2.resize(img, (16, 16), interpolation=cv2.INTER_AREA)])
        printProgressBar(i + 1, len(os.listdir(directory)))
	
    dupe_list = []

    print("\nCalculating MSE and SSIM")
    printProgressBar(0, len(image_data))
    for i, data in enumerate(image_data):
        mse_ssim = [(item[0], mse(data[1], item[1]), ssim(data[1], item[1]))
               for item in image_data if data[0] is not item[0]]
        dupe = [(data[0], item[0]) for item in mse_ssim if item[2] > 0.9 and item[1] < 1]
        if dupe != []:
            dupe_list.append(dupe)
        printProgressBar(i + 1, len(image_data))