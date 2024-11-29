#!/usr/bin/env python3

import os
import shutil
from pathlib import Path
import json
import sys
import subprocess
from glob import glob
import re

# setting up project's lcoations
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCRIPTS_FOLDER = os.path.join(ROOT_DIR, "scripts")

project_name = input("Enter project name: ")
PROJECT_FOLDER = os.path.join(ROOT_DIR, "data", "nerf", project_name)

# check if project folder exists
if not os.path.exists(PROJECT_FOLDER):
    print("Project folder does not exist. Exiting...")
    sys.exit(1)

# converting images to jpg using ffmpeg
def convert_jpg(images_name):
  # ask if user wants to convert images to png
  answer = input("Convert them to continue? (Y/n)").lower().strip()
  
  if answer == "y":
    for i in images_name:
      image_abs_path = images_folder + "\\" + i
      jpg_abs_path = images_folder + "\\" + i.split(".")[0] + ".jpg"
      print(image_abs_path)
      print(jpg_abs_path)
      os.system("ffmpeg -i {0} {1}".format(image_abs_path, jpg_abs_path))
      # result = subprocess.run(["ffmpeg", "-i", image_abs_path, png_abs_path], capture_output=True, text=True)
      # print(result.stdout)    
  if answer == "n":
    print('Will not convert files to png. Exiting...')
    sys.exit(1)
  else:
    print('Invalid input. Exiting...')
    sys.exit(1)

# check file type
images_name = []
images_folder = os.path.join(PROJECT_FOLDER, "images")
images = os.listdir(images_folder)
images_abs_path = [os.path.join(images_folder, i) for i in images]

for i in images:
    if i.split(".")[-1] != "jpg":
      print(i)
      images_name.append(i)

if len(images_name) == 0:
  print("All files are jpg, nothing to convert.")
else:
  print('Above files are not jpg...')
  convert_jpg(images_name)


# Check if images' blurriness
blury = []
def check_blurriness(images):
  # check if opencv is installed
  try:
    import cv2
  except ModuleNotFoundError:
    input("OpenCV is not installed. Press enter to install it.")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
    import cv2

  img = cv2.imread(images)
  value_of_blur = cv2.Laplacian(img, cv2.CV_64F).var()
  print(value_of_blur)
  if value_of_blur < 500:
    print('Image is blurry')
    blury.append(images.split('.')[-2])
  else:
    print('Image is not blurry')

  # preview the blury images
  for i in blury:
    show = cv2.imread(images)

for i in images_abs_path:
  check_blurriness(i)

# import cv2
# img = cv2.imread('C:\\Users\\test\\Downloads\\instant-ngp-master\\data\\nerf\\test\\images\\experiment.jpg')
# value_of_blur = cv2.Laplacian(img, cv2.CV_64F).var()
# print(value_of_blur)

# if value_of_blur < 500:
#    print('Image is blurry')
# else:
#     print('Image is not blurry')