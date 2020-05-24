"""
FILENAME: main.py
-------------------
run around on a map
"""

import tkinter
import time
import math
from tkinter import *
from PIL import ImageTk, Image
import os

CANVAS_WIDTH = 1400      # Width of drawing canvas in pixels
CANVAS_HEIGHT = 800    # Height of drawing canvas in pixels
CANVAS_MIDDLE_X = CANVAS_WIDTH/2
CANVAS_MIDDLE_Y = CANVAS_HEIGHT/2
PERSON_WIDTH = 75
MAP_WIDTH = 4000
MOVEMENT_VARIABLE = 5
IMAGE_FILE_NAME = "images/grass.jpeg"


def main():
    # MAKE CANVAS
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'adventure')
    # MAKE BACKGROUND
    image = Image.open(IMAGE_FILE_NAME)
    photo = ImageTk.PhotoImage(image)
    my_map = canvas.create_image(0, 0, image=photo, anchor=NW)
    # MAKE PERSON
    person = make_person(canvas, CANVAS_MIDDLE_X, CANVAS_MIDDLE_Y)
    # TODO:
    # what is the border of background?
    print(canvas.bbox(my_map))

    ##### TRYING TO CAPTURE KEYBOARD CLICKS #####
    x_direction = 0
    y_direction = 0



    def callback(event):
        nonlocal canvas
        canvas.focus_set()
        print("clicked at " + str(event.x) + " " + str(event.y))
        # print("window dimensions are " + canvas.coords())

    def pressed_w(event):
        print("pressed w")
        nonlocal y_direction
        nonlocal x_direction
        if y_direction == -1: y_direction = 0
        else:
            y_direction = -1
            x_direction = 0
        print(x_direction, y_direction)
        # canvas.move(person, 0, -10)


    def pressed_a(event):
        print("pressed a")
        nonlocal y_direction
        nonlocal x_direction
        if x_direction == -1:
            x_direction = 0
        else:
            x_direction = -1
            y_direction = 0
        print(x_direction, y_direction)
        # canvas.move(person, -10, 0)

    def pressed_s(event):
        print("pressed s")
        nonlocal y_direction
        nonlocal x_direction
        if y_direction == 1:
            y_direction = 0
        else:
            y_direction = 1
            x_direction = 0
        print(x_direction, y_direction)
        # canvas.move(person, 0, 10)

    def pressed_d(event):
        print("pressed d")
        nonlocal y_direction
        nonlocal x_direction
        if x_direction == 1:
            x_direction = 0
        else:
            x_direction = 1
            y_direction = 0
        print(x_direction, y_direction)
        # canvas.move(person, 10, 0)


    canvas.bind("<Button-1>", callback)

    canvas.bind("w", pressed_w)
    canvas.bind("a", pressed_a)
    canvas.bind("s", pressed_s)
    canvas.bind("d", pressed_d)
    canvas.pack()

    while True:
        draw_frame(canvas, person, x_direction, y_direction)
        time.sleep(1/50)


def make_person(canvas, x, y):
    return canvas.create_oval(x + PERSON_WIDTH/2, y + PERSON_WIDTH/2, x - PERSON_WIDTH/2, y - PERSON_WIDTH/2, fill="red")


def draw_frame(canvas, person, x_direction, y_direction):
    canvas.move(person, MOVEMENT_VARIABLE * x_direction, MOVEMENT_VARIABLE * y_direction)
    canvas.update()


######## DO NOT MODIFY ANY CODE BELOW THIS LINE ###########


# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
def make_canvas(width, height, title):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    return canvas


if __name__ == '__main__':
    main()