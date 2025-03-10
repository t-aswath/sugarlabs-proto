
# Add an AI-assistant to the Write Activity Prototype

## Overview
This project is a **Add an AI-assistant to the Write Activity Prototype** that demonstrates the complete flow of an AI-powered grammar correction tool. The system consists of a **GTK 3.0-based desktop application** that interacts with a **FastAPI backend** powered by a **Hugging Face LLM** via LangChain. The primary goal of this prototype is to validate the workflow from **user input to backend processing and back to the user** while showcasing the feasibility of an AI-based grammar correction system.

## Table of Contents

1.  [Overview](#overview)
2.  [Demo](#demo)
3.  [Features](#features)
4.  [Tech Stack](#tech-stack)
5.  [How It Works](#how-it-works)
6.  [Limitations](#limitations)
7.  [Can be Overcomed](#can-be-overcomed)
8.  [Installation & Setup](#installation--setup)
9.  [Project Structure](#project-structure)
10. [Conclusion](#conclusion)

## Demo
- [youtube](https://youtu.be/bcr_ln06yr8) 

## Features
- **User Interface:** Built with GTK 3.0, featuring a text input box and a button to trigger the grammar check.
- **Backend API:** Developed with FastAPI, exposing an endpoint on port `8000` to handle requests.
- **Grammar Correction:** Identifies incorrect sentences and suggests corrections with explanations.
- **Real-time Updates:** The corrected text replaces the original input in the text box after processing.
- **Notifications:** Displays informative messages about grammar corrections or errors encountered.

## Tech Stack
- **Frontend:** GTK 3.0 (Python)
- **Backend:** FastAPI
- **AI Processing:** Hugging Face LLM, LangChain
- **Communication:** HTTP requests (requests library)
- **Parsing & Formatting:** Regular expressions (re module)

## How It Works
1. **User Input:** The user enters a sentence in the text box.
2. **Grammar Check Trigger:** Clicking the "Check Grammar" button sends the text to the FastAPI backend.
3. **Backend Processing:**
   - The input is formatted into a prompt using LangChain.
   - The LLM analyzes the text and returns corrections if needed.
   - If the sentence is correct, it returns "ok".
4. **Response Handling:**
   - If corrections are found, the parsed result is displayed in a pop-up.
   - The corrected sentence replaces the original text in the input box.
5. **User Interaction:** The user can modify the text and repeat the process as needed.

## Limitations
- **Model Choice:** A free model from Hugging Face is used, limiting quality and control over responses.
- **Unpredictability:** Model output may be inconsistent, potentially breaking the parsing logic.
- **Limited Input Handling:** Designed for **single sentences only**; larger text inputs are not yet optimized.
- **Future Improvements:** Plans to integrate a more robust model, improve UI design, and handle larger text inputs.

## Can Be Overcomed

With a **better model**, more **consistent and accurate responses** can be generated. This improvement alone will be sufficient to fulfill the completeness of this prototype.

## Installation & Setup
### 1. Set Up Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
cd AI
pip install -r requirements.txt
```

### 3. Running the Application
#### Start the Backend
```bash
fastapi dev main.py
```
#### Start the Frontend
```bash
cd ..
python3 window.py
```

Alternatively, you can use the provided `run.sh` script to streamline the setup process. Ensure that the commands align with your machine’s environment before executing.

## Project Structure
```
├── AI/
│   ├── main.py  # FastAPI backend
│   ├── model.py # AI model integration
│   ├── requirements.txt # Python dependencies
├── window.py  # GTK frontend
├── run.sh  # Script to start the application
├── README.md  # Project documentation (this file)
```

## Conclusion
This prototype successfully demonstrates a **proof of concept** for an AI-powered grammar correction system. The next iteration will focus on enhancing accuracy, supporting larger text inputs, and refining the UI/UX for a more seamless experience.

---

**Developed by:** t-aswath
- [github](https://github.com/t-aswath)
- matrix: @t-aswath:matrix.org
- [email](mailto:aswathscid@gmail.com)
