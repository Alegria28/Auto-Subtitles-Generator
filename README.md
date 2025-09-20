# Automatic Subtitle Generator

This project is a desktop tool to automatically generate subtitles for a video file and then burn them into it. It uses `openai-whisper` for audio-to-text transcription, `MoviePy` for video manipulation, and `Tkinter` with `python-vlc` for the graphical interface.

## Features

*   Graphical user interface to select and preview the video.
*   Video playback controls (pause, progress bar, volume).
*   Options to customize the appearance of subtitles (font, size, color, position).
*   Selection of the AI model for transcription (`Tiny`, `Base`, `Small`, `Medium`, `Large`, `Turbo`).
*   Video processing in a Docker container to keep the environment clean and reproducible.

## Requirements

*   **Python 3:** To run the interface script.
*   **Docker:** To run the processing container.
*   **VLC:** Required for video playback in the interface.
*   **GNOME Terminal:** Used to display the Docker process. The script can be adapted for other terminals.

### System Dependencies

Before running the local script (`main.py`), make sure you have the following tools installed on your system:

*   **VLC Media Player:** The GUI uses it to play the video.
    *   On Debian/Ubuntu: `sudo apt-get install vlc`
    *   On macOS (with Homebrew): `brew install vlc`
    *   On Windows: Download it from the [official site](https://www.videolan.org/vlc/).

*   **Tkinter:** The library for the graphical interface. It is included in many Python installations, but in some Linux distributions, it may need to be installed separately.
    *   On Debian/Ubuntu: `sudo apt-get install python3-tk`

## Local Environment Setup

An automated installation script is provided to configure the project's environment and dependencies.

### Automatic Installation (Linux/macOS)

For Linux and macOS users, simply run the following command from the project root. This script will create a virtual environment, activate it, and install all the necessary libraries.

**Important:** You must run the script using the `source` command for the virtual environment to be activated correctly in your terminal.

```bash
source setup.sh
```

> **Why `source`?**
> It is crucial to use `source setup.sh` (or its shortcut `. setup.sh`) instead of `./setup.sh`. By using `source`, the script modifies your current terminal session, activating the virtual environment in it. If you run it as `./setup.sh`, the environment will only be activated in a temporary process that closes when the script finishes, and it will have no effect on your terminal.

Once executed, you will see the environment name (`venv`) appear at the beginning of your terminal line, indicating that it is active and ready to use.

## Steps to Generate a Video

Follow these steps in order to generate a video with subtitles:

### 1. Run the Main Application

Make sure you have the virtual environment activated if you followed the setup steps. Then, run the interface script:

```bash
python main.py
```

### 2. Select Video and Configure Subtitles

When you start the application, a window will open for you to select the video file. Once selected, the application will display the video and the options to configure the subtitles.

Use the interface to adjust subtitle options such as font, size, color, position, and the AI model.

### 3. Generate the Video

When you are ready, click the **"Generate Subtitles"** button.

This will open a new terminal window that automates the entire process:
1.  **Builds the Docker image** (`docker build`).
2.  **Runs the container** (`docker run`) to process the video.
3.  **Displays the progress** of the transcription and video generation.

The transcription process can take several minutes, depending on the length of the video and the power of your machine.

### 4. Get the Result

Done! When the process in the new terminal finishes, you will find the final video with the embedded subtitles in `sharedFolder/videoWithSubtitles.mp4`.