'''
Author: Hadrien Michel
mail: hadrien[dot]michel[at]uliege[dot]be

This program aims at preprossesing of MicaSense RedEdge-P data.
It will take as inputs the raw images from the camera and convert
them into reflectance images that can be used for post-processing
using OpenDroneMap or any other photogrametry tool.

It is heavily based on the MicaSense imageprocessing library
provided by MicaSense (https://github.com/micasense/imageprocessing).

List of updates:
----------------
    - 23/03/02: Creation and startup
'''
# Common library imports
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os, glob
import math
# MicaSense imageprocessing toolbox imports
from micasense import image, capture, panel, imageset, dls, plotutils, utils

'''Accessing files locations'''
mainPath = os.path.join('D:\\OneDrive','OneDrive - Universite de Liege','01.Fieldwork','04.Drones','02.Tests','01.Colonster','23.02.14.Tests','MicaSense')
calibrationPath = glob.glob(os.path.join(mainPath,'0005SET','000','IMG_0056_*.tif'))

'''Processing of the calibration panel data'''
cap = capture.Capture.from_filelist(calibrationPath)
for img in cap.images:
    print(f'Band nb. {img.meta.band_index()} ({img.meta.band_name()}):')
    print(f'\t- Dark Level: {np.array(img.meta.black_level()).mean()}')
    print(f'\t- Image specific calibration:\n\t\to a1 = {img.meta.radiometric_cal()[0]}\n\t\to a2 = {img.meta.radiometric_cal()[1]}\n\t\to a3 = {img.meta.radiometric_cal()[1]}')
    print(f'\t- Exposure time: {img.meta.exposure()}')
    print(f'\t- ISO: {img.meta.get_item("EXIF:ISOSpeed")}')
    print(f'\t- Bits per pixel: {img.meta.bits_per_pixel()}')
#     radianceImage, L, V, R = utils.raw_image_to_radiance(img.meta, img.raw())
#     fig, ax = plt.subplots(2,2)
#     i = 0
#     for val in [radianceImage, L, V, R]:
#         ax[i]
# cap.plot_vignette()
# plt.show(block=True)




