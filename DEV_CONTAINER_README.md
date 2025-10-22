# Dev Container Setup for Sleep Health Analysis

This project includes a **Dev Container** configuration that makes it easy to
run the application with all its dependencies in a consistent environment.

## Prerequisites

1. **VS Code** with the **Dev Containers extension** installed

   - Install VS Code: https://code.visualstudio.com/
   - Install Dev Containers extension:
     https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

2. **Docker Desktop** installed and running
   - Windows/Mac: https://www.docker.com/products/docker-desktop
   - Linux: Install Docker Engine

## How to Use

### Method 1: Quick Start

1. Clone this repository
2. Open the project folder in VS Code
3. VS Code will automatically detect the dev container configuration
4. Click "Reopen in Container" when prompted
5. Wait for the container to build (first time may take a few minutes)
6. Run the application with: `python main.py`

### Method 2: Manual Setup

1. Open VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Dev Containers: Open Folder in Container"
4. Select this project folder
5. Wait for the container to build
6. Run the application with: `python main.py`

## Platform-Specific Notes

### Windows

- The dev container will work out of the box
- GUI applications will display properly in the container

### Linux

- You may need to allow X11 forwarding:
  ```bash
  xhost +local:docker
  ```

### macOS

- You may need to install XQuartz for X11 support:
  ```bash
  brew install --cask xquartz
  ```

## What's Included

The dev container automatically:

- ✅ Installs Python 3.13
- ✅ Installs all required Python packages
- ✅ Sets up GUI support for tkinter applications
- ✅ Configures VS Code with Python extensions
- ✅ Provides a consistent development environment

## Troubleshooting

### GUI Not Displaying

If the tkinter GUI doesn't display:

1. **On Linux**: Run `xhost +local:docker` on your host machine
2. **On Windows**: Make sure Docker Desktop is running with WSL2 backend
3. **On macOS**: Install and run XQuartz

### Container Won't Build

- Make sure Docker Desktop is running
- Check your internet connection (container needs to download dependencies)
- Try rebuilding: `Ctrl+Shift+P` → "Dev Containers: Rebuild Container"

## Running Without Dev Container

If you prefer to run locally:

1. Install Python 3.13
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python main.py`
