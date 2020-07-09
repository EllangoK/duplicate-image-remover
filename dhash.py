from scipy.spatial import distance
import cv2
import os

def dhash(image, hashSize=8):
    resized_img = cv2.resize(image, (hashSize + 1, hashSize))
    diff = resized_img[:, 1:] > resized_img[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def dhash_path(path, hashSize=8):
    if pic.endswith(".webm") or pic.endswith(".mp4") or pic.endswith(".gif"):
        return None
    image = cv2.imread(path)
    if image is None:
        return None
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return dhash(image, hashSize=hashSize)

if __name__ == '__main__':
    directory = ""

    pic_hashes = {}
    dupes = []

    for pic in os.listdir(directory):
        path = os.getcwd() + directory + pic
        image_hash = dhash_path(path)
        if image_hash is None:
            continue
        elif image_hash in pic_hashes:
            pic_hashes[image_hash].append([pic])
        else:
            pic_hashes[image_hash] = [[pic]]

    for key in pic_hashes.keys():
        if len(pic_hashes[key]) > 1:
            print([i[0] for i in pic_hashes[key]])
