# NeRF_automation_tool<br/>
A personal project of creating a python tool to speed up the process of preparing input images for colmap camera detection and Instant-NeRF training.

![GUI](https://github.com/user-attachments/assets/0dd569ba-02c0-40f0-a55c-1f7fe29dad44)

## Synopsis
By using the [Fast Fourier Transform](https://pyimagesearch.com/2020/06/15/opencv-fast-fourier-transform-fft-for-blur-detection-in-images-and-video-streams/) the motion blur in each image can be quantified.<br/>
After comparing the results of using <ins>**Variation of Laplacian**</ins> with that of <ins>**Fast Fourier Transform**</ins>, the latter produces a more accurate blurriness for images extract from videos.<br/>
Since the images can be taken on various devices/by different persons(professional or not); it's impossible to set a fixed threshold to determine if a given image is blurry or not. Thus, the threshold is determined by the given set of images' blurriness mean and standard deviation(σ).
```
Threshold = Mean - Standard deviation
```
Any image with a blurriness below the threshold will be considered blurry.<br/><br/>
With the help of nerf_automation, it should speed up the process of filtering colmap output images. Sending sharper and clearer images back to colmap, it can better determine camera transforms and locations. Correct camera transforms and location should increase accuracy for Instant-NeRF results. Sharp/less blurry images would also help Instant-NeRF generate better results.

## Requirements

The tool calls for `PyQt5`, `numpy`, `imutils`, and `opencv`; please make sure all modules are installed before running.<br/>
Most should have been installed if instant-ngp was installed properly.

A requirement.txt has been provided, you can simply run `pip install -r requirements.txt` to install all necessary modules<br/>
> Please don't mix it up with instant-ngp's requirements.txt

<br/>
Files should be placed under the correct structure as shown below:<br/>

```
.
├─ instant-ngp(Root Folder)\
│  ├─ instant-ngp.exe
│  ├─ Scripts\
│  │  ├─ nerf_automation.py
│  │  ├─ nerf_automation.exe
│  │  ├─ colmap2nerf.py
│  │  ├─ ...
│  │
│  └─ data\
│     └─ nerf\
│        ├─ fox\
│        └─ project_folder\
│           ├─ video.mp4/mov (optional)
│           ├─ transformed.json (will be generated after converting)
│           └─ images\
│              ├─ 0001.jpg
│              ├─ 0002.jpg
│              ├─ 0003.jpg
│              ├─ ...
```
- Please make sure that the `nerf-automation.py` is placed in the `scripts folder` along with other instant-ngp scripts
- If `images folder` isn't present but a video file was given, a transformed.json file might be generated while extracting images from the video. The process of writing the first transformed.json file usually endsup failing due to permissions errors. However, the first json file will eventually be overwritten and replaced by the later one while colmap processes the sharper/filtered images.
## Process
**1. Set up Project Folder<br/>**<br/>
	Type in the project name to find the desired project folder or hit `browse` button and select project folder<br/>
	The first image should automatically show in the preview window<br/>

  > Please make sure that the images have been extracted from the video and placed in `images` folder<br/>
  > If only a video file was found in the project folder, a pop-up window with the colmap2nerf code would be provided in `Show Details`<br/>
  > If more than one video is present, only the first video's path would be taken and run if `Run for me` button was clicked<br/>
<br/>

**2. Check Bluriness<br/>**<br/>
  Click `Check Blurriness` to start calculating each image's blurriness<br/>
  > Depending on the number of images given, it might take a while to calculate each image's blurriness<br/>
  
  Once blurriness was calculated, each image's blurriness will be shown on the right side with the set of images' blurriness mean and standard deviation(σ) for comparison<br/>
  Detailed blurriness can be found in the output text browser at the bottom<br/>
  Use `Show all` to show all images and `Show Blurry` to show only blurry ones<br/>
  `Previous` and `Next` buttons are located below the preview window for switching through images<br/>

  > The threshold to determine if an image is blurry is calculated by mean - std<br/>
<br/>

**3. Check or uncheck options<br/>**<br/>
  Make sure desired options are checked before hitting `Run` button<br/>
  - <ins>Auto-filter blurry images</ins>: Default checked, will automatically delete blurry images after hitting `Run` button
  - <ins>Manually check blurry images</ins>: Won't delete blurry images, instead keeping all for later process allowing the user to filter manually
  - <ins>Outdoor scene</ins>: Check if the project images/video were taken outdoors, will set the [aabb_scale](https://github.com/NVlabs/instant-ngp/blob/master/docs/nerf_dataset_tips.md#existing-datasets) as 16, while the default value is 8
  - <ins>Run Instant-NeRF</ins>: Open and start Instant-NeRF training with the transformed.json file from colmap and the images

  > Since the threshold is determined by the mean and std of images' blurriness<br/>
  > If most images are blurry, it is recommended to re-run and re-filter several times until all images are considered sharp 
<br/>

**4. Hit `Run` button and enjoy!**<br/>

## References
[OpenCV Fast Fourier Transform (FFT) for blur detection in images and video streams](https://pyimagesearch.com/2020/06/15/opencv-fast-fourier-transform-fft-for-blur-detection-in-images-and-video-streams/) <br/>
[Blur detection with OpenCV](https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/) <br/>
[Tips for training NeRF models with Instant Neural Graphics Primitives](https://github.com/NVlabs/instant-ngp/blob/master/docs/nerf_dataset_tips.md) <br/>
[Blur dataset](https://www.kaggle.com/datasets/kwentar/blur-dataset)
