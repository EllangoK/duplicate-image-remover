#!/usr/bin/python3
# -*- coding: utf-8 -*-

from skimage.metrics import structural_similarity as ssim
from tkinter.filedialog import askdirectory
from collections import defaultdict
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


def merge_common(lists):
    neigh = defaultdict(set)
    visited = set()
    for each in lists:
        for item in each:
            neigh[item].update(each)

    def comp(node, neigh=neigh, visited=visited, vis=visited.add):
        nodes = set([node])
        next_node = nodes.pop
        while nodes:
            node = next_node()
            vis(node)
            nodes |= neigh[node] - visited
            yield node
    for node in neigh:
        if node not in visited:
            yield sorted(comp(node))


def keep_widest_img(data):
    widest_file = max(data, key=lambda i: i[0])
    for item in data:
        if item[1] == widest_file[1]:
            continue
        else:
            os.remove(item[1])


def keep_highest_name(data):
    num_filenames = [(item[1].split('/')[-1].split(',')[0], item[1])
                     for item in data]
    highest_filename = max(num_filenames, key=lambda i: int(i[0]))
    widest_file = max(data, key=lambda i: int(i[0]))
    img = cv2.imread(widest_file[1])
    for item in data:
        os.remove(item[1])
    cv2.imwrite(highest_filename[1], img)


def mse(first_img, second_img):
    err = np.sum((first_img.astype("float") - second_img.astype("float")) ** 2)
    err /= float(first_img.shape[0] * first_img.shape[1])
    return err


def dhash(image, hashSize=8):
    resized_img = cv2.resize(image, (hashSize + 1, hashSize))
    diff = resized_img[:, 1:] > resized_img[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])


def dhash_path(path, hashSize=8):
    if path.endswith(".webm") or path.endswith(".mp4") or path.endswith(".gif"):
        return None
    image = cv2.imread(path, 0)
    if image is None:
        return None
    return dhash(image, hashSize=hashSize)

def remove_duplicates(directory, custom=True):
    image_data = {}
    pic_hashes = {}

    print("Calculating dhashes")
    printProgressBar(0, len(os.listdir(directory)))
    for i, rel_path in enumerate(os.listdir(directory)):
        path = directory + "/" + rel_path
        img = cv2.imread(path, 0)
        if img is None:
            printProgressBar(i + 1, len(os.listdir(directory)))
            continue
        image_data[path] = [img, cv2.resize(
            img, (8, 8), interpolation=cv2.INTER_AREA), img.shape[1]]
        image_hash = dhash(img)
        printProgressBar(i + 1, len(os.listdir(directory)))
        if image_hash is None:
            continue
        elif image_hash in pic_hashes:
            pic_hashes[image_hash].append(path)
        else:
            pic_hashes[image_hash] = [path]

    dupe_list = []
    for key in pic_hashes.keys():
        if len(pic_hashes[key]) > 1:
            dupe_list.append(pic_hashes[key])

    if len(dupe_list) == 0:
        print("No Duplicates Found via Dhash")
    else:
        count = 0
        for i in dupe_list:
            for j in i:
                count += 1
        count -= len(dupe_list)

        print("Deleting " + str(count) + " dupes found via Dhash")
        printProgressBar(0, len(dupe_list))
        for i, dupes in enumerate(dupe_list):
            printProgressBar(i + 1, len(dupe_list))
            data = [(image_data[path][2], path) for path in dupes]
            if custom:
                keep_highest_name(data)
            else:
                keep_widest_img(data)

    paths = [directory + "/" + item for item in os.listdir(directory)]
    for key in image_data:
        if key not in paths:
            image_data[key] = None

    dupe_list = []
    print("Calculating MSE and SSIM")
    printProgressBar(0, len(image_data))
    for i, data in enumerate(image_data):
        mse_ssim = [(key, mse(image_data[data][1], image_data[key][1]), ssim(image_data[data][1], image_data[key][1]))
                    for key in image_data if data is not key and image_data[data] is not None]
        dupe = [item[0]
                for item in mse_ssim if item[2] > 0.9 and item[1] < 2.5]
        if dupe != []:
            dupe.insert(0, data)
            dupe_list.append(dupe)
        printProgressBar(i + 1, len(image_data))
    dupe_list = list(merge_common(dupe_list))

    if len(dupe_list) == 0:
        print("No Duplicates Found")
        sys.exit()
    else:
        count = 0
        for i in dupe_list:
            for j in i:
                count += 1
        count -= len(dupe_list)

        print("Deleting " + str(count) + " dupes found via SSIM and MSE")
        printProgressBar(0, len(dupe_list))
        for i, dupes in enumerate(dupe_list):
            data = [(image_data[path][2], path) for path in dupes]
            if custom:
                keep_highest_name(data)
            else:
                keep_widest_img(data)
            printProgressBar(i + 1, len(dupe_list))


if __name__ == '__main__':
    args = sys.argv[1:]
    directory = ""
    if len(args) == 0:
        Tk().withdraw()
        directory = askdirectory()
    else:
        directory = os.path.abspath(args[0])
    remove_duplicates(directory)
