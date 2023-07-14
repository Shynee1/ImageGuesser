from tkinter import *
import tensorflow as tf
from PIL import Image, ImageDraw, ImageGrab
import numpy as np
import process
import random

class Draw():
    def __init__(self, root, item):
        self.root = root
        self.root.title("QuickDraw")
        self.root.geometry("810x530")
        background_color = "#ffbb00"
        self.root.configure(background = background_color)
        self.model = tf.keras.models.load_model('models/QuickDraw.h5')
        self.model.predict(np.zeros([1, 28, 28, 1]))

        self.strokes = []
        self.x = []
        self.y = []

        self.pointer = "black"
        self.pointer_size = 10

        text = Label(root,
                     text = "Draw: " + item,
                     bg = background_color,
                     font = ("Comic Sans", 25),
                     foreground = "black",
                     justify = CENTER)
        text.pack()

        self.background = Canvas(self.root, 
                                 bg = "white", 
                                 bd = 5, 
                                 relief = FLAT,
                                 height = 470, 
                                 width = 810)
        self.background.place(x = 0, y = 50)

        self.clear_screen = Button(self.root, 
                                   text = "Clear Screen", 
                                   bg = "white",
                                   command = self.clear_screen,
                                   width = 15, 
                                   height = 2, 
                                   relief = SOLID)
        self.clear_screen.place(x = 10, y = 5)

        self.guess_text = Label(root,
                     text = "Guess: ...",
                     bg = background_color,
                     font = ("Comic Sans", 20),
                     foreground = "black",
                     justify = CENTER)
        self.guess_text.place(x = 575, y = 5)

        self.background.bind("<B1-Motion>", self.paint)
        self.background.bind("<ButtonRelease-1>", self.mouse_lift)

    def clear_screen(self):
        self.background.delete("all")
        self.strokes = []

    def mouse_lift(self, event):
        self.strokes.append([self.x, self.y])
        self.x = []
        self.y = []

        image = process.processStrokes(self.strokes)

        img = np.array(image)
        img = (img.astype('float32')) / 255
        img = np.reshape(img, (1, 28, 28, 1))

        pred = self.model.predict(img)[0]
        pred_class = list(pred).index(max(pred))
        
        print(max(pred))
        
        if pred_class == 0.0:
            self.guess_text.config(text="Guess: Bandage")
        elif pred_class == 1.0:
            self.guess_text.config(text="Guess: Cell Phone")
        elif pred_class == 2.0:
            self.guess_text.config(text="Guess: Hamburger")
        elif pred_class == 3.0:
            self.guess_text.config(text="Guess: Pizza")
        elif pred_class == 4.0:
            self.guess_text.config(text="Guess: Sailboat")
        elif pred_class == 5.0:
            self.guess_text.config(text="Guess: Sheep")
        elif pred_class == 6.0:
            self.guess_text.config(text="Guess: Star")
        elif pred_class == 7.0:
            self.guess_text.config(text="Guess: Television")
        else:
            print(pred_class)

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
    draw = ["Bandage", "Cell Phone", "Hamburger", "Pizza", "Sailboat", "Sheep", "Star", "Television"]
    p = Draw(root, random.choice(draw))
    root.mainloop()