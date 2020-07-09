#!/usr/bin/python3
# -*- coding: utf-8 -*-

from skimage.metrics import structural_similarity as ssim
from tkinter.filedialog import askdirectory
import matplotlib.pyplot as plt
from tkinter import Tk
import numpy as np
import cv2

def mse(firstImg, secondImg):
    err = np.sum((firstImg.astype("float") - secondImg.astype("float")) ** 2)
    err /= float(firstImg.shape[0] * firstImg.shape[1])
    return err


def compare_images(imageA, imageB, title):
	# compute the mean squared error and structural similarity
	# index for the images
	m = mse(imageA, imageB)
	s = ssim(imageA, imageB)
	# setup the figure
	fig = plt.figure(title)
	plt.suptitle("MSE: %.2f, SSIM: %.2f" % (m, s))
	# show first image
	ax = fig.add_subplot(1, 2, 1)
	plt.imshow(imageA, cmap=plt.cm.gray)
	plt.axis("off")
	# show the second image
	ax = fig.add_subplot(1, 2, 2)
	plt.imshow(imageB, cmap=plt.cm.gray)
	plt.axis("off")
	# show the images
	plt.show()


if __name__ == '__main__':
    Tk().withdraw()
    directory = askdirectory()

	first = cv2.resize(first, (8, 8), interpolation=cv2.INTER_AREA)
	second = cv2.resize(second, (8, 8), interpolation=cv2.INTER_AREA)

	fig = plt.figure("Images")
	images = ("3929,8bs6kf.png", first), ("2459,54rgx8.png", second)

	for (i, (name, image)) in enumerate(images):
		# show the image
		ax = fig.add_subplot(1, 3, i + 1)
		ax.set_title(name)
		plt.imshow(image, cmap=plt.cm.gray)
		plt.axis("off")

	plt.show()
	compare_images(cv2.cvtColor(first, cv2.COLOR_BGR2GRAY),
				cv2.cvtColor(second, cv2.COLOR_BGR2GRAY), "first vs. second")
