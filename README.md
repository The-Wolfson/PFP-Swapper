# PFP Swapper

A Python script that automatically the colour of your profile picture on Slack using GitHub Actions every 5 minutes.

## How It Works

1. Takes a base image (`pfp.png`)
2. Calculates the current frame based on the GitHub Actions run number
3. Shifts the hue of the image by the appropriate amount
4. Uploads the modified image as your new Slack profile picture

## Setup

### Prerequisites

- A Slack workspace where you have permission to change your profile picture
- A GitHub account
- A base profile picture image (PNG format recommended)

### Usage

1. **Fork this repository**

2. **Add your profile picture**
   - Add your base profile picture as `pfp.png` in the root directory
   - PNG format is recommended

3. **Get your Slack token**
   - Go to [Slack API](https://api.slack.com/apps)
   - Create a new app or use an existing one
   - Navigate to "OAuth & Permissions"
   - Add the `users.profile:write` scope
   - Install the app to your workspace
   - Copy the "User OAuth Token" (starts with `xoxp-`)

4. **Configure GitHub Secrets**
   - Go to your repository Settings → Secrets and variables → Actions
   - Add a new secret named `AUTH_TOKEN` with your Slack token as the value

5. **Enable GitHub Actions**
   - The workflow will automatically start running every 5 minutes
   - You can also trigger it manually from the Actions tab

## Configuration

You can customize the behavior by modifying `config.py`:

- `NUM_FRAMES`: Number of hue variations (default: 60)
- `PATH_TO_IMAGE`: Path to your base image file (default: "pfp.png")

## File Structure

```
pfp-swapper/
├── main.py                 # Main script that handles image processing and Slack API
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── pfp.png                 # Your base profile picture
├── .github/
│   └── workflows/
│       └── pfp-swapper.yml # GitHub Actions workflow
└── README.md               # This file
```

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

---

Built with love using `Python` in Newcastle, Australia
