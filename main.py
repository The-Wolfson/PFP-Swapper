# Profile Picture Swapper - Cycles through hue-shifted versions of an image
from PIL import Image, ImageFile
import numpy as np
import colorsys
import requests
import os
import io
import config

def shift_hue(img: ImageFile.ImageFile, shift: float):
    """
    Shifts the hue of an image by a specified amount.

    Args:
        img: Input image file
        shift: Hue shift amount (0.0 to 1.0, where 1.0 = full color wheel)

    Returns:
        Image with shifted hue
    """
    # Convert to RGBA to preserve transparency
    img = img.convert("RGBA")
    # Convert PIL image to numpy array for pixel manipulation
    arr = np.array(img)
    # Separate color channels (red, green, blue, alpha)
    r, g, b, a = np.rollaxis(arr, axis=-1)

    # Convert RGB values to HSV color space for hue manipulation
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(r/255., g/255., b/255.)
    # Shift hue and wrap around using modulo to stay in 0-1 range
    h = (h + shift) % 1.0
    # Convert back to RGB color space
    r, g, b = np.vectorize(colorsys.hsv_to_rgb)(h, s, v)

    # Update the array with new RGB values (convert back to 0-255 range)
    arr[...,0] = (r*255).astype(np.uint8)
    arr[...,1] = (g*255).astype(np.uint8)
    arr[...,2] = (b*255).astype(np.uint8)
    arr[...,3] = a  # Preserve original alpha channel
    return Image.fromarray(arr)

last_frame = 0
# Frame tracking: Load the last used frame number from file
if os.path.exists(config.FRAME_FILE):
    with open(config.FRAME_FILE, "r") as f:
        last_frame = int(f.read().strip())

# Calculate next frame in the cycle (wraps back to 0 after NUM_FRAMES)
next_frame = (last_frame + 1) % config.NUM_FRAMES

# Load the base image that will be hue-shifted
img: ImageFile.ImageFile = Image.open(config.PATH_TO_IMAGE)

# Calculate hue step: divide full color wheel by number of frames
HUE_STEP = 1.0 / config.NUM_FRAMES
# Apply hue shift based on current frame position
shifted_img = shift_hue(img, HUE_STEP * next_frame)

# Prepare HTTP headers for API authentication
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {config.AUTH_TOKEN}"
}

# Convert shifted image to bytes for upload
img_bytes = io.BytesIO()
shifted_img.save(img_bytes, format="PNG")
img_bytes.seek(0)  # Reset buffer position for reading
files = {
    "image": ("frame.png", img_bytes, "image/png")
}

# Upload the new profile picture via API
response = requests.post(config.API_PATH, headers=headers, files=files)
print(config.API_PATH)
# Check if upload was successful
if response.status_code == 200:
    print(f"Updated profile photo to Hue {HUE_STEP * next_frame:.2f} (Frame {next_frame})")
else:
    print("Error:", response, response.headers, response.text)

# Save current frame number for next execution
with open(config.FRAME_FILE, "w") as f:
    f.write(str(next_frame))