<div align="center">


<h1> TikTok Live Recorder🎥</h1>

<em>TikTok Live Recorder is a tool for recording live streaming tiktok.</em>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) [![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

The TikTok Live Recorder is a tool designed to easily capture and save live streaming sessions from TikTok. It records both audio and video, allowing users to revisit and preserve engaging live content for later enjoyment and analysis. It's a valuable resource for creators, researchers, and anyone who wants to capture memorable moments from TikTok live streams.

<img src="https://i.ibb.co/N2TCwVhx/pic.png" alt="image" border="0">

</div>

<div align="left">


  <h1> How To Use </h1>

- [Install on Windows & Linux 💻](#install-on-windows--linux-)
- [Install on Android 📱](#install-on-android-)

</div>


## Install on Windows & Linux 💻

To clone and run this application, you'll need [Git](https://git-scm.com) and [Python3](https://www.python.org/downloads/) and [FFmpeg](https://www.youtube.com/watch?v=OlNWCpFdVMA) installed on your computer. From your command line:

<!-- <img src="https://i.ibb.co/8DkzXZn/image.png" alt="image" border="0"> -->

<be>

</div>

  ```bash
# Clone this repository
$ git clone https://github.com/Michele0303/tiktok-live-recorder
# Go into the repository
$ cd tiktok-live-recorder
# Go into the source code
$ cd src
# Install dependencies
$ pip install -r requirements.txt --break-system-packages
# Run the app on windows
$ python main.py -h
# Run the app on linux
$ python3 main.py -h
  ```

## Install on Android 📱

<b>Install Termux from F-Droid:</b> <a href="https://f-droid.org/packages/com.termux/">HERE</a> - Avoid installing from Play Store to prevent potential issues.

From termux command line:

<be>

</div>

  ```bash
# Update packages
$ pkg update
$ pkg upgrade
# Install git, python3, ffmpeg
$ pkg install git python3 ffmpeg
# Clone this repository
$ git clone https://github.com/Michele0303/tiktok-live-recorder
# Go into the repository
$ cd tiktok-live-recorder
# Go into the source code
$ cd src
# Install dependencies
$ pip install -r requirements.txt --break-system-packages
# Run the app
$ python main.py -h
  ```

<div align="left">

## Guide

- <a href="https://github.com/Michele0303/tiktok-live-recorder/blob/main/GUIDE.md#how-to-set-cookies">How to set cookies in cookies.json</a> 
- <a href="https://github.com/Michele0303/tiktok-live-recorder/blob/main/GUIDE.md#how-to-get-room_id">How to get room_id</a> 
- <a href="https://github.com/Michele0303/tiktok-live-recorder/blob/main/GUIDE.md#how-to-enable-upload-to-telegram">How to enable upload to telegram</a> 

## Multi-Stream Recording 🎬

The TikTok Live Recorder now supports recording multiple live streams simultaneously! You can record from multiple users, URLs, or room IDs using a single command.

### Usage Examples:

```bash
# Record multiple users simultaneously
python main.py -users username1 username2 username3 -mode automatic

# Import usernames from a text file
python main.py -users-file usernames.txt -mode automatic

# Combine command line users and file import
python main.py -users user1 user2 -users-file usernames.txt -mode automatic

# Record multiple streams from URLs
python main.py -urls "https://www.tiktok.com/@user1/live" "https://www.tiktok.com/@user2/live" -mode manual

# Record multiple streams by room IDs
python main.py -room_ids 123456789 987654321 111222333 -mode automatic
```

### Multi-Stream Features:
- **Simultaneous Recording**: Record multiple streams at the same time using threading
- **Individual File Management**: Each stream is saved as a separate file with unique naming
- **User-Specific Folders**: Recordings are automatically organized in folders named after each user
- **Thread-Safe Logging**: Each stream's activities are logged with thread identifiers
- **Graceful Shutdown**: Stop all recordings cleanly with Ctrl+C
- **Same Configuration**: All streams use the same settings (proxy, output directory, duration, etc.)

### Multi-Stream Arguments:
- `-users`: Space-separated list of TikTok usernames
- `-urls`: Space-separated list of TikTok live URLs
- `-room_ids`: Space-separated list of TikTok room IDs

**Note**: You cannot mix single-stream and multi-stream arguments in the same command.

## To-Do List 🔮

- [x] **Automatic Recording**: Enable automatic recording of live TikTok sessions.
- [x] **Authentication:** Added support for cookies-based authentication.
- [x] **Recording by room_id:** Allow recording by providing the room ID.
- [x] **Recording by TikTok live URL:** Enable recording by directly using the TikTok live URL.
- [x] **Using a Proxy to Bypass Login Restrictions:** Implement the ability to use an HTTP proxy to bypass login restrictions in some countries (only to obtain the room ID).
- [x] **Implement a Logging System:** Set up a comprehensive logging system to track activities and errors.
- [x] **Implement Auto-Update Feature:** Create a system that automatically checks for new releases.
- [x] **Send Recorded Live Streams to Telegram:** Enable the option to send recorded live streams directly to Telegram.
- [x] **Multi-Stream Recording:** Record multiple live streams simultaneously with threading support.
- [ ] **Save Chat in a File:** Allow saving the chat from live streams in a file.
- [ ] **Support for M3U8:** Add support for recording live streams via m3u8 format.
- [x] ~~**Watchlist Feature**: Implement a watchlist to monitor multiple users simultaneously~~ (Completed with multi-stream recording)

## Legal ⚖️

This code is in no way affiliated with, authorized, maintained, sponsored or endorsed by TikTok or any of its affiliates or subsidiaries. Use at your own risk.
