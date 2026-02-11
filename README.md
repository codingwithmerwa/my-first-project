# my-first-project
An AI-powered gaze tracking system using MediaPipe and OpenCV to translate iris movement into directional commands for assistive robotics


This is my first major Computer Science project. It uses AI-driven computer vision to track a user's iris and translate eye movement into directional commands (LEFT, RIGHT, UP, DOWN).

# The Purpose
Designed as the "Brain" for assistive technology, this software allows individuals with limited mobility to control a robot or a computer interface using only their eyes.

# How it Works
1. **MediaPipe Face Mesh**: Detects 468 facial landmarks.
2. **Iris Refinement**: Specifically targets Landmark 468 (the pupil center).
3. **Gaze Ratio Math**: Calculates the relative position of the iris between the eye corners and eyelids.
4. **Logic Thresholds**: Translates these ratios into commands with a "deadzone" to prevent accidental movement.

##  Built With
* Python 3.10
* OpenCV (Computer Vision)
* MediaPipe (AI/Machine Learning)
* NumPy (Mathematical calculations
