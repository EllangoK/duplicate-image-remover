from scipy.spatial import distance
import cv2
import os

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)

    if iteration == total:
        print()

def dhash(image, hashSize=8):
    resized_img = cv2.resize(image, (hashSize + 1, hashSize))
    diff = resized_img[:, 1:] > resized_img[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def dhash_path(path, hashSize=8):
    if path.endswith(".webm") or path.endswith(".mp4") or path.endswith(".gif"):
        return None
    image = cv2.imread(path)
    if image is None:
        return None
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return dhash(image, hashSize=hashSize)

def keep_widest_img(data):
    widest_file = max(data, key=lambda i: i[0])
    for item in data:
        if item[1] == widest_file[1]:
            continue
        else:
            os.remove(item[1])

def keep_highest_name(data):
    num_filenames = [(item[1].split('/')[-1].split(',')[0], item[1]) for item in data]
    highest_filename = max(num_filenames, key=lambda i: i[0])
    widest_file = max(data, key=lambda i: i[0])
    img = cv2.imread(widest_file[1])
    for item in data:
        os.remove(item[1])
    cv2.imwrite(highest_filename[1], img)
    pass

if __name__ == '__main__':
    custom = True
    directory = ""

    pic_hashes = {}

    print("Calculating dhashes")
    printProgressBar(0, len(os.listdir(directory)), prefix='Progress:',
                     suffix='Complete', length=60)
    for i, rel_path in enumerate(os.listdir(directory)):
        path = os.getcwd().replace("\\", "/") + "/" + directory + "/" + rel_path
        image_hash = dhash_path(path)
        if image_hash is None:
            continue
        elif image_hash in pic_hashes:
            pic_hashes[image_hash].append([path])
        else:
            pic_hashes[image_hash] = [[path]]
        printProgressBar(i + 1, len(os.listdir(directory)), prefix='Progress:',
                         suffix='Complete', length=60)

    dupes = []
    for key in pic_hashes.keys():
        if len(pic_hashes[key]) > 1:
            dupes.append([i[0] for i in pic_hashes[key]])

    print(dupes)

    for dupe_list in dupes:
        data = [(cv2.imread(path).shape[1], path) for path in dupe_list]
        if custom:
            keep_highest_name(data)
        else:
            keep_widest_img(data)
