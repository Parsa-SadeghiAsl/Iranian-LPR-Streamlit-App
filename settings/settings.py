from pathlib import Path
import sys

# Get the absolute path of the current file
file_path = Path(__file__).resolve()

# Get the parent directory of the current file
root_path = file_path.parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the relative path of the root directory with respect to the current working directory
ROOT = root_path.relative_to(Path.cwd())

# Sources

VIDEO = 'Video'
WEBCAM = 'Webcam'
RTSP = 'RTSP/Path'


SOURCES_LIST = [VIDEO, WEBCAM, RTSP]


# Videos config
VIDEO_1_PATH = 'videos/test.mp4'

VIDEOS_DICT = {
    'video_1': VIDEO_1_PATH
}

# ML Model config

DETECTION_MODEL = 'models/platedetection.pt'
# In case of your custome model comment out the line above and
# Place your custom model pt file name at the line below 
# DETECTION_MODEL = MODEL_DIR / 'my_detection_model.pt'

READER_MODEL = 'models/OCRplate.pt'

# Webcam
WEBCAM_PATH = 0
