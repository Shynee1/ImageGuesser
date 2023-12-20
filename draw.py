from tkinter import *
import tensorflow as tf
from PIL import Image, ImageTk
import numpy as np
import process
import time
import random

classes = [
    "Banana", 
    "Bandage", 
    "Book", 
    "Cake", 
    "Camera", 
    "Cell Phone", 
    "Face", 
    "Hamburger", 
    "Pizza", 
    "Sailbot", 
    "Sheep", 
    "Star", 
    "Sword", 
    "Television", 
    "Effiel Tower"
]

class Draw():
    def __init__(self, root):
        self.root = root
        self.root.title("QuickDraw")
        self.root.geometry("810x530")
        background_color = "#ffbb00"
        self.root.configure(background = background_color)
        # Load model from file
        self.model = tf.keras.models.load_model('models/QuickDraw.h5')
        self.model.predict(np.zeros([1, 28, 28, 1]))
        self.expected_class = random.choice(classes)

        self.strokes = []
        self.x = []
        self.y = []

        self.pointer = "black"
        self.pointer_size = 10

        # --- GUI Setup -----
        self.expected_class_label = Label(root,
                     text = "Draw: " + self.expected_class,
                     bg = background_color,
                     font = ("Comic Sans", 25),
                     foreground = "black",
                     justify = CENTER)
        self.expected_class_label.pack()

        self.background = Canvas(self.root, 
                                 bg = "white", 
                                 bd = 5, 
                                 relief = FLAT,
                                 height = 470, 
                                 width = 810)
        self.background.place(x = 0, y = 50)

        self.clear_screen_button = Button(self.root, 
                                   text = "Clear Screen", 
                                   bg = "white",
                                   command = self.clear_screen,
                                   width = 15, 
                                   height = 2, 
                                   relief = SOLID)
        self.clear_screen_button.place(x = 10, y = 5)

        self.guess_text = Label(root,
                     text = "Guess: ...",
                     bg = background_color,
                     font = ("Comic Sans", 20),
                     foreground = "black",
                     justify = CENTER)
        self.guess_text.place(x = 575, y = 5)

        # Bind callbacks
        self.background.bind("<B1-Motion>", self.paint)
        self.background.bind("<ButtonRelease-1>", self.mouse_lift)

    # Clears all drawings on the screen
    def clear_screen(self):
        self.background.delete("all")
        self.strokes = []

    # Completely resets for the next round
    def reset_game(self):
        self.clear_screen()
        self.expected_class = random.choice(classes)
        self.expected_class_label.config(text = "Draw: " + self.expected_class)

    # Recursive function to create a new instance of every object in a nested list
    def create_new_objects(self, nested_list):
        if isinstance(nested_list, list):
            return [self.create_new_objects(item) for item in nested_list]
        else:
            return nested_list

    # Mouse callback that sends strokes to model
    def mouse_lift(self, event):
        self.strokes.append([self.x, self.y])
        self.x = []
        self.y = []

        # Process strokes into proper data format
        s = self.create_new_objects(self.strokes)
        image = process.processStrokes(s)

        # Convert to numpy array
        img = np.array(image)
        img = (img.astype('float32')) / 255
        img = np.reshape(img, (1, 28, 28, 1))

        pred = self.model.predict(img)[0]
        pred_class = list(pred).index(max(pred))
        
        print(max(pred))
        
        # Load new round after item has been guessed
        self.guess_text.config(text = "Guess: " + classes[pred_class])
        if classes[pred_class] == self.expected_class:
            root.after(300, lambda: self.reset_game())

    # Mouse callback to handle drawing on the screen
    def paint(self, event):
        self.x.append(event.x)
        self.y.append(event.y)

        x1, y1 = (event.x - 3), (event.y - 3)
        x2, y2 = (event.x + 3), (event.y + 3)

        self.background.create_oval(x1, y1, x2, y2, 
                                    fill = self.pointer,
                                    outline = self.pointer, 
                                    width = self.pointer_size)

if __name__ == "__main__":
    root = Tk()
    p = Draw(root)
    root.mainloop()