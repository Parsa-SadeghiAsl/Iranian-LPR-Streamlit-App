# Iranian-LPR-Streamlit-App

user-friendly License Plate Recognition (LPR) application built using Streamlit.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
This webapp is an user-friendly License Plate Recognition (LPR) application built using Streamlit. Designed specifically for Iranian license plates, this app leverages cutting-edge machine learning models to accurately detect and recognize license plate numbers from images or live video streams.
The core functionality of Iranian PlateVision is powered by YOLO (You Only Look Once) for object detection and OCR (Optical Character Recognition). The YOLOv8 model enables fast and accurate detection of license plates, while the OCR model accurately extracts the alphanumeric characters from the detected license plates.
The Streamlit webapp was developed with inspiration and assistance provided by the [ yolov8-streamlit-detection-tracking
](https://github.com/CodingMantras/yolov8-streamlit-detection-tracking) GitHub repository, which provided valuable insights and resources during the development process.

![Screenshot from 2024-06-06 12-59-42](https://github.com/Parsa-SadeghiAsl/Iranian-LPR-Streamlit-App/assets/101510809/45a2a2e3-7695-4f67-9019-272d1dcd2825)



## Features

- **Streamlit Interface**: Offers an intuitive and interactive user interface powered by Streamlit, allowing users to easily upload images or access live video feeds for real-time plate recognition.
- **Database Integration**: Seamlessly integrates with databases for storing and managing recognized license plate data, facilitating easy retrieval and analysis.
- **Accurate License Plate Recognition**: Utilizes YOLO (You Only Look Once) for precise detection of license plates, followed by OCR for accurate extraction of license plate numbers.

## Installation

### 1. Clone the repository:
   ```bash
   git clone https://github.com/Parsa-SadeghiAsl/Iranian-LPR-Streamlit-App.git
   ```
### 2. Navigate to the project directory:
   ```bash
   cd ./Iranian-LPR-Streamlit-App
   ```
### 3. Make 'setup.sh' executable:
   ```bash
   chmod +x setup.sh
   ```
### 4. Run the setup script to create a virtual environment and install dependencies:
   ```bash
   ./setup.sh
   ```

## Usage

### 1. Run the Streamlit web-application:
   ```bash
   ./webapp.sh
   ```
### 2. Open your web browser and navigate to `http://localhost:8501` to view the application.

### 3. Offline Videos For LPR can be added/changed through 'setting.py' file:

specific instruction will be provided in the future...

