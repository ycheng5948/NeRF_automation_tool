import os
import shutil
from pathlib import Path
import json
import sys
import subprocess
from glob import glob
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
SCRIPTS_FOLDER = os.path.join(ROOT_DIR, "scripts")

os_list_dir = os.listdir(ROOT_DIR)
json_files = []
for file in os_list_dir:
  if re.match(r".*\.json$", file):
    print(os.path.join(ROOT_DIR, file))
    json_files.append(file)

# print("list of files and directories using os:")
# for i in os_list_dir:
#     print(ROOT_DIR + "\\" + i)

for i in json_files:
  file_path = os.path.join(ROOT_DIR, i)
  if os.path.isfile(file_path):
    print("json file exists!")
  else:
    print("no json file found.")

# get the current working directory using os
os_working_dir = os.getcwd()
print(os_working_dir)
# get the current working directory using Path
path_working_dir = Path.cwd()
print(path_working_dir)
print('----------------------------------------------')

# get the name of the current file using os
os_file_name = os.path.basename(__file__)
print("file name using os:\n" + os_file_name)
# get the name of the current file using Path
path_file_name = Path(__file__).name
print("file path using Path:\n" + str(path_file_name))
print('----------------------------------------------')

# get the path of the current file's full path using os
os_file_dir = os.path.realpath(__file__)
print("file\'s full path using os:\n" + os_file_dir)
# get the file's parent directory using os
os_file_dir = os.path.dirname(os_file_dir)
print("file\'s parent directory using os:\n" + os_file_dir)
print('----------------------------------------------')

# get the path of the current file's directory using Path
path_file_dir = Path(__file__)
print("file\'s full path using Path:\n" + str(path_file_dir))
# get the file's parent directory using Path
parent_dir = path_file_dir.parent
print("file\'s parent directory using Path:\n" + str(parent_dir))
print('----------------------------------------------')

# list all files and directories in the current directory using os
os_list_dir = os.listdir(os_working_dir)
print("list of files and directories using os:")
for i in os_list_dir:
    print(os_file_dir + "\\" + i)
# list all files and directories in the current directory using Path
path_list_dir = Path.cwd()
print("list of files and directories using Path:")
for i in path_list_dir.iterdir():
    print(i)
print('----------------------------------------------')

# make a new directory same level as the current file if it doesn't exist
if not os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/os_folder'):
    os.makedirs(os.path.dirname(os.path.realpath(__file__)) + '/os_folder')
# delete the new directory if it exists
if os.path.exists(os.path.dirname(os.path.realpath(__file__)) + '/os_folder'):
    shutil.rmtree(os.path.dirname(os.path.realpath(__file__)) + '/os_folder')

# make a new directory same level as the current file if it doesn't exist using path
if not Path(os.path.dirname(__file__) + '/path_folder').exists():
    Path(os.path.dirname(__file__) + '/path_folder').mkdir()
# delete the new directory if it exists using path
if Path(os.path.dirname(__file__) + '/path_folder').exists():
    shutil.rmtree(Path(os.path.dirname(__file__) + '/path_folder'))
print('----------------------------------------------')


############################################################################################
def get_path():
    current_path = os.path.realpath(__file__)
    return current_path

get_path()

def find_and_replace_path(file_path, old_path, new_path):
  """Finds and replaces a specific path within a JSON file.

  Args:
    file_path: The path to the JSON file.
    old_path: The old path to be replaced.
    new_path: The new path to replace the old one.
  """

  with open(file_path, 'r') as f:
    data = json.load(f)

  def replace_path(obj):
    if isinstance(obj, dict):
      for key, value in obj.items():
        if isinstance(value, str) and old_path in value:
          obj[key] = value.replace(old_path, new_path)
        replace_path(value)
    elif isinstance(obj, list):
      for item in obj:
        replace_path(item)

  replace_path(data)

  with open(file_path, 'w') as f:
    json.dump(data, f, indent=2)

# Example usage:
file_path = 'path/to/file.json'
old_path = 'lines that include images'
new_path = 'the relative path of the json file to the images folder'

find_and_replace_path(file_path, old_path, new_path)
############################################################################################333

# get file type
images_name = []
# os_list_dir = os.listdir(os_working_dir)
images = os.listdir(ROOT_DIR + "\\data\\path_test\\test\\new_images")
images_folder = ROOT_DIR + "\\data\\path_test\\test\\new_images"

for i in images:
    if i.split(".")[-1] != "png":
      print(i)
      images_name.append(i)

if len(images_name) == 0:
  print("no files are png")

def do_system(arg):
  print("==== running: " + str({arg}) + " ====")
  err = os.system(arg)
  if err:
    print("FATAL: command failed")
    sys.exit(err)

def convert_to_png(args):
  ffmpeg_binary = "ffmpeg"
  # If FFmpeg isn't found, try automatically downloading it from the internet
  if os.system(f"where {ffmpeg_binary} >nul 2>nul") != 0:
    ffmpeg_glob = os.path.join(ROOT_DIR, "external", "ffmpeg", "*", "bin", "ffmpeg.exe")
    candidates = glob(ffmpeg_glob)
  if not candidates:
    print("FFmpeg not found. Attempting to download FFmpeg from the internet.")
    do_system(os.path.join(SCRIPTS_FOLDER, "download_ffmpeg.bat"))
    candidates = glob(ffmpeg_glob)
  
  if candidates:
     ffmpeg_binary = candidates[0]
  
  if not os.path.isabs(args.images):
    args.images = os.path.join(os.path.dirname(args.video_in), args.images)
  
  # setting up arguments for ffmpeg
  for i in images_name:
    image_abs_path = images_folder + "\\" + i
    png_abs_path = images_folder + "\\" + i.split(".")[0] + ".png"
    print(image_abs_path)
    print(png_abs_path)

    # result = subprocess.run(["ffmpeg", "-i", image_abs_path, png_abs_path], capture_output=True, text=True)
    # print(result.stdout)
    os.system("ffmpeg -i {0} {1}".format(image_abs_path, png_abs_path))
    
  images = "\"" + args.images + "\""
  jpg_images = "\\" + args.images + "\\"

  # ask to overwrite the images folder, and get y/n input
  if not args.overwrite and (input(f"warning! folder '{images}' will be deleted/replaced. continue? (Y/n)").lower().strip()+"y")[:1] != "y":
    sys.exit(1)
  try:
    # Passing Images' Path Without Double Quotes
    shutil.rmtree(args.images)
  except:
    pass
  do_system(f"mkdir {jpg_images}")
  do_system(f"{ffmpeg_binary} -i {image_abs_path} {png_abs_path}/%04d.png")

  do_system("ffmpeg -i {0} {1}.png".format(image_abs_path, png_abs_path))

############################################################################################

package = 'git+https://github.com/facebookresearch/detectron2.git'
subprocess.check_call([sys.executable, "-m", "pip", "install", package])
import detectron2