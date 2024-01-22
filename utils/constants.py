# Third-party library imports
from PIL import Image

# Base Colors
DARK = "#222831"
GREY = "#393E46"
TURQUOISE = "#00ADB5"
DARK_TURQUOISE = "#00959C"
WHITE = "#EEEEEE"

FILE_TYPES = (
    ("PNG files", "*.png"),
    ("BMP files", "*.bmp"),
    ("JPEG files", "*.jpeg"),
    ("All files", "*.*"),
)
RESAMPLE_METHOD = Image.BICUBIC
WATERMARK_TAG = "watermark"
BASE_SIZE = 60
