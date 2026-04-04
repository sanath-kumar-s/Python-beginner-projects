<h1 align="center">
    <img src="assets/logo.png" width = "28"> exeflow
</h1>

<p align = "center">
    <i align="center"> Where Python Scripts Become Real Applications. </i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" />
  <img src="https://img.shields.io/badge/Platform-Windows-lightgrey" />
  <img src="https://img.shields.io/badge/UI-CustomTkinter-purple" />
  <img src="https://img.shields.io/badge/Bundler-PyInstaller-orange" /><br>
  <img src="https://img.shields.io/badge/AI-Groq--Powered-black" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</p>

![Application Screenshot](assets/picture1.png)

**ExeFlow** is a desktop tool that converts Python scripts into professional, distributable software with a single click.

It removes the complexity of packaging, dependency handling, and asset bundling by providing a modern graphical interface and automated build workflow. This allows developers—especially beginners—to turn `.py` files into `.exe` applications without manually dealing with command-line tools like PyInstaller.

## Features

- Convert Python scripts into executable applications instantly
- Built-in asset bundling (icons, images, audio)
- Splash screen and console configuration
- AI assistance for build configuration and debugging
- Real-time build logs and status tracking
- Fully customizable build settings through an intuitive UI

---

## Installation

After cloning the repository, install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
python main.py
```

The GUI will launch and you can begin configuring your build.

---

## How to Use

### 1. File Data Section

This section contains the core information required to build your executable:

- **Final App Name** – Name of the generated executable
- **Python File** – Select the `.py` file you want to compile
- **App Icon** – Choose an `.ico` file for your application icon

---

### 2. Additional Items Section

Here you can include external assets required by your script:

- **Image Folder** – Required if your script uses image assets
- **Audio Folder** – Required if your script uses audio files

If these folders are needed by your script but not provided, the build will fail.

---

### 3. Additional Settings Section

This section allows deeper customization of the build:

- **One-File Toggle** – Build into a single executable file
- **No Console** – Hide terminal window for GUI applications
- **Final Build Location** – Choose where the compiled app will be saved
- **Splash Image** – Optional splash screen during startup
- **Additional Command Extension** – Extra PyInstaller arguments for advanced users

---

### 4. Building the Executable

After filling all fields, click:

```
Build EXE
```

The build process will start immediately.

A **log box** at the bottom of the window displays real-time compilation output so you can monitor progress and debug errors if they occur.

---

## AI Assistance Panel

On the left side of the application, ExeFlow provides an integrated AI assistant designed specifically for build-related tasks.

It helps with:

- identifying missing dependencies
- suggesting packaging fixes
- generating correct build arguments

---

## AI Configuration

To use AI features, you must provide your API key.

Open `main.py` and update:

```python
self.client = Groq(api_key="YOUR_API_KEY")
self.model = "your-preferred-model"
```

You can change the model by modifying `self.model` directly below the client configuration.

---

## Why ExeFlow Exists

Beginners often struggle when converting Python scripts into executables due to:

- complex PyInstaller commands
- missing dependency errors
- incorrect asset bundling
- confusion around icons, splash screens, and console settings

ExeFlow solves this by replacing manual configuration with a structured graphical workflow, making the build process predictable and beginner-friendly.

---

## Technologies Used

ExeFlow is built using:

- **customtkinter** – modern UI framework for Tkinter
- **tkinter** – file dialogs and system integration
- **subprocess** – running PyInstaller build commands
- **threading** – keeping the UI responsive during builds
- **Pillow (PIL)** – image handling and splash screen processing
- **Groq API** – AI-powered assistance and automation
- **json & os modules** – configuration and file management

---

## Project Structure

```
ExeFlow/
│
├── main.py
├── requirements.txt
├── assets/
└── README.md
```

---

## Notes

Before building an executable, ensure that all Python packages used by your script are installed in the environment. Missing dependencies will cause the build to fail.

---

## Contributer

**Sanath K S**
