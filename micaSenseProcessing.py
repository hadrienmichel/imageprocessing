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
import imageio
import json
# import tifffile
import exiftool
# MicaSense imageprocessing toolbox imports
from micasense import image, capture, panel, imageset, dls, plotutils, utils

'''Accessing files locations'''
mainPath = os.path.join('.','data','test')#os.path.join('D:\\OneDrive','OneDrive - Universite de Liege','01.Fieldwork','04.Drones','02.Tests','01.Colonster','23.02.14.Tests','MicaSense')
calibrationPath = glob.glob(os.path.join(mainPath, 'IMG_0007_*.tif'))#mainPath,'0005SET','000','IMG_0056_*.tif'))
imagesPath = None

'''Processing of the calibration panel data'''
dlsOrientationVector = np.array([0,0,-1])
cap = capture.Capture.from_filelist(calibrationPath)
for img in cap.images:
    print(f'Band nb. {img.meta.band_index()} ({img.meta.band_name()}):')
    print(f'\t- Dark Level: {np.array(img.meta.black_level()).mean()}')
    print(f'\t- Image specific calibration:\n\t\to a1 = {img.meta.radiometric_cal()[0]}\n\t\to a2 = {img.meta.radiometric_cal()[1]}\n\t\to a3 = {img.meta.radiometric_cal()[1]}')
    print(f'\t- Exposure time: {img.meta.exposure()}')
    print(f'\t- ISO: {img.meta.get_item("EXIF:ISOSpeed")}')
    print(f'\t- Bits per pixel: {img.meta.bits_per_pixel()}')
# RedEdge-P Downwelling Light Sensor (DLS) values
# plt.scatter(cap.center_wavelengths(), cap.dls_irradiance(), color='b', label='DLS Sensor')
# plt.scatter(cap.center_wavelengths(), cap.panel_irradiance(), color='r', label='Calibration Panel')
# plt.xlabel('Wavelength (nm)')
# plt.ylabel('Irradiance ($W/m^2/nm$)')
# plt.legend()

# fig, ax = plt.subplots()
# wavelengths = np.linspace(0, 2000, 1000)
# def gaussian(x, mu, sig):
#     return (np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.))))/(np.sqrt(2*np.pi)*sig)
# for img in cap.images:
#     center = img.meta.center_wavelength()
#     bandwidth = img.meta.bandwidth()
#     std = bandwidth/(2*math.sqrt(2*math.log(2)))
#     amplitude = gaussian(wavelengths, center, std)
#     ax.plot(wavelengths, amplitude, label=img.meta.band_name())
# ax.set_xlabel('Wavelength (nm)')
# ax.set_ylabel('Relative Amplitude (/)')
# ax.legend()

# cap.plot_raw()
# cap.plot_vignette()
# cap.plot_undistorted_reflectance(np.multiply(cap.dls_irradiance(),cap.panel_irradiance()))
# plt.show(block=True)

# cap.save_capture_as_rgb()
if os.environ.get('exiftoolpath') is not None:
    exiftoolPath = os.path.normpath(os.environ.get('exiftoolpath'))
else:
    exiftoolPath = None
dlsIrradiance = cap.dls_irradiance()
panelIrradiance = cap.panel_irradiance()
# for the export of the images, use imageio
for i, img in enumerate(cap.images):
    fileName, ext = os.path.splitext(img.path)
    name = "{0}".format(fileName[:-1] + 'post_' + str(i+1) + ext)
    values = img.undistorted_reflectance(dlsIrradiance[i]*panelIrradiance[i])
    metaDataOriginal = img.meta.get_all()
    imageio.imwrite(name, values)
    metaData = json.dumps(metaDataOriginal)
    with exiftool.ExifTool(exiftoolPath) as exift:
        exift.execute(b"-tagsFromFile", bytes(img.path, encoding='utf8'), bytes(name, encoding='utf8'))
    os.remove(name+'_original')
###
# Now, the processing pipeline seem to be: 
# - Pre-process the images for vignetting and reflectance correction 
#       - panel correction (f(t)=a+b*t from initial and last calibration)
#       - dls correction (f(t) from dls sensor)
#       - ratio for shadows from clouds = 1??? or 1/6??? How to build this? (can be ignored if constant accross the measure) 
# - Building orthophoto using ODM (WebODM) with the option to change scale to reflectance turned off
#       - This approach builds the orthophotos after aligning the different images
# - Building orthophoto using ODM for the panchromatic image 
# - Aligne both orthophotos
# - Pansharpen the images using ??? (PCA pansharpening of CNN???)
# - Profit??? :p