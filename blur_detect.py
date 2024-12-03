import os
import sys
import cv2
import statistics

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCRIPTS_FOLDER = os.path.join(ROOT_DIR, "scripts")

project_name = input("Enter project name: ")
PROJECT_FOLDER = os.path.join(ROOT_DIR, "data", "nerf", project_name)

# check if project folder exists
if not os.path.exists(PROJECT_FOLDER):
    print("Project folder does not exist. Exiting...")
    sys.exit(1)

images_folder = os.path.join(PROJECT_FOLDER, "images")
images = os.listdir(images_folder)
images_abs_path = [os.path.join(images_folder, i) for i in images]

threshold = 100
blurriness = []

def variance_of_laplacian(image):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(image, cv2.CV_64F).var()

for imagePath in images_abs_path:
    # load the image, convert it to grayscale, and compute the
    # focus measure of the image using the Variance of Laplacian
    # method
    image = cv2.imread(imagePath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    # if the focus measure is less than the supplied threshold,
    # then the image should be considered "blurry"
    if fm < threshold:
        text = "Blurry"
    if fm > threshold:
        text = "Not Blurry"
    
    print('{0:10}{1:10}{2}'.format(imagePath.split("\\")[-1].split('_')[-1], "%.2f" % fm, text))
    blurriness.append(fm)
    
    # show the image
    # cv2.putText(image, "{}: {:.2f}".format(text, fm), (10, 30),
    #     cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    # cv2.imshow("Image", image)
    # key = cv2.waitKey(0)

print(statistics.mean(blurriness))
######################################################################################
# import cv2
# import numpy as np

# def detect_motion_blur(image):
#     # Convert the image to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Calculate the Fourier Transform
#     f = np.fft.fft2(gray)
#     fshift = np.fft.fftshift(f)

#     # Calculate the magnitude spectrum
#     magnitude_spectrum = 20*np.log(np.abs(fshift))

#     # Calculate energy concentration and entropy
#     energy_concentration = np.sum(magnitude_spectrum[0:10, 0:10]) / np.sum(magnitude_spectrum)
#     entropy = -np.sum(magnitude_spectrum * np.log2(magnitude_spectrum + 1e-9))

#     # Set thresholds for motion blur detection
#     energy_threshold = 0.1  # Adjust as needed
#     entropy_threshold = 4.0  # Adjust as needed

#     if energy_concentration > energy_threshold or entropy < entropy_threshold:
#         return True  # Image is likely motion blurred
#     else:
#         return False

# for imagePath in images_abs_path:
#     # load the image, convert it to grayscale, and compute the
#     # focus measure of the image using the Variance of Laplacian
#     # method
#     image = cv2.imread(imagePath)
#     is_motion_blurred = detect_motion_blur(image)
#     # if the focus measure is less than the supplied threshold,
#     # then the image should be considered "blurry"
#     if is_motion_blurred:
#         # print("Image is motion blurred")
#         text = "Motion Blurred"
#     else:
#         # print("Image is not motion blurred")
#         text = "Not Motion Blurred"

#     print('{0:10}{1:10}'.format(imagePath.split("\\")[-1].split('_')[-1], text))

######################################################################################

