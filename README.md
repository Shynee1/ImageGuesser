# Image Guesser
Want to test your drawing skills? See if my neural network can guess what you are drawing! \
This model has been trained on Google's [QuickDraw](https://quickdraw.withgoogle.com/data) dataset to recognize hand-drawn doodles

## Table of Contents
- [Features](#features)
- [Setup & Installation](#setup--installation)
- [Project Information](#project-information)

## Features
The CNN can recognize 15 different types of drawings:
- `Banana`
- `Bandage`
- `Book`
- `Cake`
- `Camera`
- `Cell Phone`
- `Face`
- `Hamburger` 
- `Pizza`
- `Sailboat` 
- `Sheep`
- `Star` 
- `Sword`
- `Television`
- `Effiel Tower`

## Setup & Installation
1. Clone the repository:
   ```bash
   $ git clone https://github.com/Shynee1/ImageGuesser.git
   $ cd ImageGuesser
   ```
2. Install dependencies:
   ```bash
   $ pip install -r requirements.txt
   ```
3. Load dataset:
   ```bash
   $ python load_data.py
   ```
4. Train model:
   ```bash
   $ python model.py
   ```
5. Run program
   ```bash
   $ python draw.py
   ```
## Project Information
This project was made as my final project for Brown University's summer AI program. 
