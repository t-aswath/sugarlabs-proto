
# Add an AI-assistant to the Write Activity Prototype

## Overview
This project is a **Add an AI-assistant to the Write Activity Prototype** that demonstrates the complete flow of an AI-powered grammar correction tool. The system consists of a **GTK 3.0-based desktop application** that interacts with a **FastAPI backend** powered by a **Ollama (llama3.2:3B)** via LangChain and Ollama-python. The primary goal of this prototype is to validate the workflow from **user input to backend processing and back to the user** while showcasing the feasibility of an AI-based grammar correction system.

## Table of Contents

1.  [Overview](#overview)
2.  [Demo](#demo)
3.  [Features](#features)
4.  [Tech Stack](#tech-stack)
5.  [How It Works](#how-it-works)
6.  [Limitations](#limitations)
7.  [TODO](#todo)
8.  [Installation & Setup](#installation--setup)
9.  [Project Structure](#project-structure)
10. [Conclusion](#conclusion)

# Demo
- [Iteration 1 (youtube)](https://youtu.be/bcr_ln06yr8) 
- [Iteration 2 (youtube)](https://youtu.be/g9cTgEII5sc) 
- [Iteration 3 (youtube)](https://youtu.be/FP7PB_yGwtI) 

# Features
- **Real-time grammar checking**: Detects errors as the user types.
- **AI-powered suggestions**: Uses a language model to provide corrections.
- **Sentence highlighting**: Marks incorrect sentences for easy identification.
- **Sidebar results panel**: Displays grammar errors and explanations.
- **Spinner indicator**: Shows the status of the grammar check request.
- **Auto-complete suggestions**: Provides context-aware corrections.

# Tech Stack
- **Backend**: FastAPI, Python, Ollama (Llama3.2:3B model)
- **Frontend**: GTK (PyGObject)
- **AI Processing**: LangChain, Async Ollama Client

# How It Works
1. **User inputs text** into the GTK-based editor.
2. **Text is monitored** for changes, triggering a grammar check when typing stops for a few seconds, set to `3 sec` for dev purposes.
3. **Grammar check request** is sent to a FastAPI backend running an AI model.
4. **Model processes the text** and returns corrections in JSON format.
5. **Results are displayed** in the sidebar, highlighting errors in the text editor.
6. **User can accept or reject** the corrections and continue typing.

# Achievements in Iteration 1
- Implemented a **working grammar correction model** using LangChain and Ollama.
- Designed a **GTK-based GUI** with an editable text area 
- Set up **FastAPI backend** for handling grammar check requests.

# Achievements in Iteration 2
- **Integrated real-time typing detection** to automatically trigger grammar checks.
- **Added** a **sidebar** for displaying results and **spinner** to indicate the status of the request.
- **Enhanced text highlighting** for more accurate sentence correction display.
- **Improved error handling** for server requests.

# Achievements in Iteration 3
- **Added** **auto-complete suggestions** for context-aware corrections.
- **Improved** the **accuracy of sentence indexing** for better highlighting.
- **Enhanced result formatting** for better readability.
- **Used Pydantic schemas** for JSON response formatting.
- **Refactored** the **backend** for better performance and readability.

# Limitations
- **Model response time**: The AI model processing may introduce delays.
- **Lack of debounce**: Rapid input changes trigger excessive requests.

# TODO

- check TODO.md

# Installation & Setup

```sh
git clone https://github.com/t-aswath/sugarlabs-proto.git
cd sugarlabs-proto
bash setup.sh
bash run.sh
```

# Project Structure

```plaintext
AI/                    # Backend
  ├── main.py          # FastAPI server
  ├── model.py         # AI model integration
  ├── pdtypes.py       # Pydantic schemas
  ├── requirements.txt # Dependencies
.gitignore             # Git ignore rules
README.md              # Project documentation
run.sh                 # Shell script to run the project
setup.sh               # Setup script
TODO.md                # Task management
window.py              # GTK-based GUI (frontend)
```

# Conclusion
This prototype successfully demonstrates a **proof of concept** for **Add an AI-assistant to the Write Activity** project

---

**Developed by:** t-aswath
- [github](https://github.com/t-aswath)
- matrix: @t-aswath:matrix.org
- [email](mailto:aswathscid@gmail.com)
