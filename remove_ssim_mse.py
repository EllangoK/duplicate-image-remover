#!/usr/bin/python3
# -*- coding: utf-8 -*-

from skimage.metrics import structural_similarity as ssim
from tkinter.filedialog import askdirectory
from collections import defaultdict
from tkinter import Tk
from tqdm import tqdm
import numpy as np
import cv2
import sys
import os

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
    a = cv2.imwrite(highest_filename[1], img)

def mse(first_img, second_img):
    err = np.sum((first_img.astype("float") - second_img.astype("float")) ** 2)
    err /= float(first_img.shape[0] * first_img.shape[1])
    return err

if __name__ == '__main__':
    custom = True
    args = sys.argv[1:]
    directory = ""
    if len(args) == 0:
        Tk().withdraw()
        directory = askdirectory()
    else:
        directory = os.path.abspath(args[0])
	
    image_data = []

    print("Loading Image, Grayscaling and Rescaling")
    for rel_path in tqdm(os.listdir(directory)):
        path = directory + "/" + rel_path
        img = cv2.imread(path, 0)
        if img is None:
            continue
        image_data.append(
            [path, cv2.resize(img, (8, 8), interpolation=cv2.INTER_AREA)])
	
    dupe_list = []
    print("\nCalculating MSE and SSIM")
    for data in tqdm(image_data):
        mse_ssim = [(item[0], mse(data[1], item[1]), ssim(data[1], item[1]))
               for item in image_data if data[0] is not item[0]]
        dupe = [item[0] for item in mse_ssim if item[2] > 0.9 and item[1] < 2.5]
        if dupe != []:
            dupe.insert(0, data[0])
            dupe_list.append(dupe)

    dupe_list = list(merge_common(dupe_list))

    if len(dupe_list) == 0:
        print("No Duplicates Found")
        sys.exit()

    count = 0
    for i in dupe_list:
        for j in i:
            count += 1
    count -= len(dupe_list)

    print("\nDeleting " + str(count) + " dupes")
    for dupes in tqdm(dupe_list):
        data = [(cv2.imread(path).shape[1], path) for path in dupes]
        if custom:
            keep_highest_name(data)
        else:
            keep_widest_img(data)
