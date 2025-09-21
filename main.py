"""
Profile Picture Swapper for Slack

This script automatically updates a Slack profile picture by cycling through
different hue variations of a base image. It's designed to be run periodically
(e.g., via cron job) to create an animated profile picture effect.

The script:
1. Loads a base image from the file system
2. Calculates which frame in the animation cycle to show
3. Shifts the hue of the image to create a color variation
4. Uploads the modified image as the user's Slack profile picture
"""

from PIL import Image, ImageFile
import numpy as np
import colorsys
import io
import config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def shift_hue(img: ImageFile.ImageFile, shift: float):
    """
    Shifts the hue of an image by a specified amount.

    This function converts an image to HSV color space, modifies the hue channel,
    and converts back to RGB while preserving the alpha channel for transparency.

    Args:
        img: Input image file (PIL Image object)
        shift: Hue shift amount (0.0 to 1.0, where 1.0 = full color wheel rotation)

    Returns:
        PIL Image object with shifted hue and preserved transparency
    """
    # Convert to RGBA to preserve transparency (alpha channel)
    img = img.convert("RGBA")

    # Convert PIL image to numpy array for efficient pixel manipulation
    arr = np.array(img)

    # Separate color channels (red, green, blue, alpha) for processing
    # rollaxis moves the color channel dimension from last to first
    r, g, b, a = np.rollaxis(arr, axis=-1)

    # Convert RGB values to HSV color space for hue manipulation
    # Normalize RGB values to 0-1 range (from 0-255) for colorsys functions
    h, s, v = np.vectorize(colorsys.rgb_to_hsv)(r/255., g/255., b/255.)

    # Shift hue and wrap around using modulo to stay in 0-1 range
    h = (h + shift) % 1.0

    # Convert back to RGB color space with modified hue
    r, g, b = np.vectorize(colorsys.hsv_to_rgb)(h, s, v)

    # Update the array with new RGB values (convert back to 0-255 range)
    arr[...,0] = (r*255).astype(np.uint8)  # Red channel
    arr[...,1] = (g*255).astype(np.uint8)  # Green channel
    arr[...,2] = (b*255).astype(np.uint8)  # Blue channel
    arr[...,3] = a  # Preserve original alpha channel (transparency)

    # Convert numpy array back to PIL Image object
    return Image.fromarray(arr)

# Calculate which frame in the animation cycle to display
# Uses modulo to cycle through frames: 0, 1, 2, ..., NUM_FRAMES-1, 0, 1, ...
next_frame = config.RUN_NUMBER % config.NUM_FRAMES

# Load the base image from the configured file path
img: ImageFile.ImageFile = Image.open(config.PATH_TO_IMAGE)

# Calculate the hue shift amount for this frame
# Divides the full color wheel (1.0) by the number of frames for smooth transitions
HUE_STEP = 1.0 / config.NUM_FRAMES

# Apply the hue shift to create the current frame's image
shifted_img = shift_hue(img, HUE_STEP * next_frame)

# Convert the PIL Image to bytes for Slack API upload
# Use BytesIO to create an in-memory file-like object
img_bytes = io.BytesIO()
shifted_img.save(img_bytes, format="PNG")  # Save as PNG to preserve transparency
img_bytes.seek(0)  # Reset file pointer to beginning for reading

# Initialize Slack API client with authentication token
client = WebClient(token=config.AUTH_TOKEN)

# Upload the modified image as the user's profile picture
try:
    response = client.users_setPhoto(image=img_bytes)
    print(f"Updated profile photo to Hue {HUE_STEP * next_frame:.2f} (Frame {next_frame})")
except SlackApiError as e:
    # Handle Slack API errors gracefully
    assert e.response["error"]
    print("Error:", e)