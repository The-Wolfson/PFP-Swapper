# PFP Swapper
A simple python script that integrates with GitHub actions to change the colour of your Mattermost profile picture over the course of a day.

## Features

- Cycles through a configurable number of hue-shifted images (`NUM_FRAMES`)
- Uses a local image (`pfp.png`) as the base profile picture
- Automatically uploads the modified image to a remote API
- Tracks frame progression to ensure smooth cycling between color variations
- Preserves image transparency

## How it works

1. Loads the last used frame number from `current_frame.txt`.
2. Calculates the next hue-shifted frame.
3. Loads the base image and applies a hue shift.
4. Converts the resulting image to bytes and uploads it via an authenticated API request.
5. Saves the frame number for the next run.

## Configuration

Edit `config.py` to set:

- `NUM_FRAMES`: Number of color variations in the cycle
- `PATH_TO_IMAGE`: Path to your base profile image
- `AUTH_TOKEN`: Authentication token for the API (can be set in your environment)
- `USER_ID`: Your user ID for the remote API
- `API_PATH`: Endpoint for uploading the image

## Usage

1. Place your base profile picture as `pfp.png` in the project directory.
2. Set the required environment variables in your GitHub config (`AUTH_TOKEN`, `USER_ID`).
3. Run the GitHub Actions cron job
