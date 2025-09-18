import os

NUM_FRAMES: int = 20
PATH_TO_IMAGE: str = "pfp.png"
AUTH_TOKEN: str = os.getenv("AUTH_TOKEN")
USER_ID: str = os.getenv("USER_ID")
API_PATH: str = f"https://not.slack.hackclub.com/api/v4/users/{USER_ID}/image"
FRAME_FILE: str = "current_frame.txt"