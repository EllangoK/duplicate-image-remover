from scipy.spatial import distance
import cv2
import os

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

if __name__ == '__main__':
    remove_lower = True
    directory = ""

    pic_hashes = {}

    for rel_path in os.listdir(directory):
        path = os.getcwd().replace("\\", "/") + "/" + directory + "/" + rel_path
        print(path)
        image_hash = dhash_path(path)
        if image_hash is None:
            continue
        elif image_hash in pic_hashes:
            pic_hashes[image_hash].append([path])
        else:
            pic_hashes[image_hash] = [[path]]

    dupes = []
    for key in pic_hashes.keys():
        if len(pic_hashes[key]) > 1:
            dupes.append([i[0] for i in pic_hashes[key]])

    print(dupes)

    for dupe_list in dupes:
        widths = [(cv2.imread(path).shape[1], path) for path in dupe_list]
        max_width = (0, 0)
        for item in widths:
            if max_width is (0, 0):
                max_width = item
            elif item[0] > max_width[0]:
                max_width = item
            elif item[0] == max_width[0]:
                if remove_lower:
                    if int(item[1].split('/')[-1].split(',')[0]) >= int(max_width[1].split('/')[-1].split(',')[0]):
                        print(max_width[0], item[0], max_width[1] + " is deleted instead of " +item[1])
                        #os.remove(max_width[1])
                        max_width = item
                    else:
                        print(item[0], max_width[0], item[1] + " is deleted instead of " + max_width[1])
                        #os.remove(item[1])
                else:
                    print(item[0], max_width[0], item[1] + " is deleted instead of " + max_width[1])
                    #os.remove(item[1])
            else:
                print(item[0], max_width[0], item[1] + " is deleted instead of " + max_width[1])
                #os.remove(item[1])
