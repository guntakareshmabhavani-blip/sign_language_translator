# AI-Based Sign Language to Speech & Text Translator

A real-time system that recognizes hand sign gestures using computer vision and machine learning, then converts them into spoken text using Windows text-to-speech — helping bridge communication for sign language users.

## Overview

This project uses a webcam to detect hand landmarks in real time, classifies the hand gesture using a trained machine learning model, and outputs the result as both on-screen text and audible speech.

## Tech Stack

- **Python** – core programming language
- **OpenCV** – webcam capture and frame processing
- **MediaPipe** – real-time hand landmark detection (21 key points per hand)
- **scikit-learn (Random Forest Classifier)** – gesture classification model
- **pywin32 (SAPI)** – Windows text-to-speech output
- **pandas / NumPy** – data handling

## How It Works

1. **Data Collection** (`collect_data.py`) — Captures hand landmark coordinates (x, y, z for 21 points) via webcam and saves labeled samples to a CSV file for each sign.
2. **Model Training** (`train_model.py`) — Trains a Random Forest Classifier on the collected landmark data and evaluates accuracy on a held-out test set.
3. **Real-Time Prediction** (`predict.py`) — Captures live video, detects hand landmarks, predicts the sign using the trained model, displays it on screen, and speaks it aloud.

## Signs Supported

- Hello
- Thank You
- Yes
- No
- Please

(Easily extendable — add more signs by collecting more labeled data.)

## Results

- **Model Accuracy:** 99% on test data
- **Real-time inference:** Smooth, low-latency predictions from live webcam feed

## Setup & Usage

1. Install dependencies:
