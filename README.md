# 🎬 Automatic Subtitle Generator

This project is a desktop tool to automatically generate subtitles for a video file and then burn them into it. It uses `openai-whisper` for audio-to-text transcription, `MoviePy` for video manipulation, and `Tkinter` with `python-vlc` for the graphical interface. 🎥

## ✨ Features

*   🖼️ **Graphical User Interface:** Easy-to-use interface to select and preview your video.
*   👁️ **Live Subtitle Preview:** See how your subtitles will look in real-time as you adjust settings like font, size, and color.
*   🎨 **Full Customization:**
    *   Choose from a wide variety of fonts.
    *   Adjust font size and color.
    *   Select a standard position (Top, Middle, Bottom).
    *   🖱️ **Click to Position:** Set a custom subtitle position simply by clicking on the video preview.
*   ✍️ **Transcription Correction:** Review and edit the AI-generated transcription word by word before generating the final video.
*   🤖 **AI Model Selection:** Choose the `openai-whisper` model that best fits your needs (`Tiny`, `Base`, `Small`, `Medium`, `Large`).
*   📦 **Isolated Environment:** Video processing occurs inside a Docker container to ensure a clean and reproducible workflow.
*   ⏯️ **Playback Controls:** Includes pause/play, a seek bar, and volume control for the video preview.

## 🛠️ Requirements

*   **Python 3.12+** & **Pyenv**: To manage the Python version and run the interface script. 🐍
*   **Docker:** To run the processing container. 🐳
*   **VLC:** Required for video playback in the interface. 📼
*   **GNOME Terminal:** Used to display the Docker process. The script can be adapted for other terminals. 💻

### System Dependencies

The `setup.sh` script will attempt to install these for you on Debian/Ubuntu systems.

*   **VLC Media Player:** The GUI uses it to play the video.
*   **Tkinter:** The library for the graphical interface.
*   **Microsoft Core Fonts:** Provides common fonts like Arial, Times New Roman, etc.

## 🚀 Local Environment Setup

An automated installation script is provided to configure the project's environment and dependencies on Linux systems.

### Automatic Installation (Linux)

For Linux users, simply run the following command from the project root. This script will check for dependencies, install the correct Python version with `pyenv`, create a virtual environment, and install all the necessary libraries.

**Important:** You must run the script using the `source` command for the virtual environment to be activated correctly in your terminal.

```bash
source setup.sh
```

> **🤔 Why `source`?**
> It is crucial to use `source setup.sh` (or its shortcut `. setup.sh`) instead of `./setup.sh`. By using `source`, the script modifies your current terminal session, activating the virtual environment in it. If you run it as `./setup.sh`, the environment will only be activated in a temporary process that closes when the script finishes, and it will have no effect on your terminal.

Once executed, you will see the environment name (`venv`) appear at the beginning of your terminal line, indicating that it is active and ready to use.

## 📝 Steps to Generate a Video

Follow these steps in order to generate a video with subtitles:

### 1. Run the Main Application

Make sure you have the virtual environment activated (by running `source venv/bin/activate` if you're in a new terminal). Then, run the interface script:

```bash
python main.py
```

### 2. Select Video and Configure Subtitles

When you start the application, a window will open for you to select the video file. Once selected, the application will display the video and the options to configure the subtitles.

Use the interface to adjust subtitle options. You will see a live preview of your changes. To set a custom position, simply click on the video.

### 3. Generate the Video

When you are ready, click the **"Generate Subtitles"** button.

This will open a new terminal window that automates the entire process:
1.  **Builds the Docker image** (`docker build`).
2.  **Runs the container** (`docker run`) to process the video.
3.  **Transcribes the audio** using the selected AI model.
4.  **Displays the progress** of the transcription and video generation.

The transcription process can take several minutes, depending on the length of the video and the power of your machine. ⏳

### 4. Correct the Transcription

Once the AI transcription is complete, the script running in the new terminal will pause and show you the generated text. You will have the option to correct any words that were transcribed incorrectly.

Follow the on-screen instructions to edit words by their number or continue if everything looks correct.

### 5. Get the Result

Done! 🎉 When the process in the new terminal finishes, you will find the final video with the embedded subtitles in the `sharedFolder/`. The output file will be named `[original_video_name]-subtitled.mp4`.