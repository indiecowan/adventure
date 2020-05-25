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
BORDER_PROX_LIMIT = 300
IMAGE_FILE_NAME = "images/grass.jpeg"


def main():
    # MAKE CANVAS
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'adventure')
    # MAKE BACKGROUND
    image = Image.open(IMAGE_FILE_NAME)
    image = image.resize((MAP_WIDTH, MAP_WIDTH), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    my_map = canvas.create_image(CANVAS_HEIGHT/2, CANVAS_WIDTH/2, image=photo, anchor=CENTER)
    # MAKE PERSON
    person = make_person(canvas, CANVAS_MIDDLE_X, CANVAS_MIDDLE_Y)
    # what is the border of background?
    print(canvas.bbox(my_map))

    ##### TRYING TO CAPTURE KEYBOARD CLICKS #####
    x_direction = 0
    y_direction = 0



    def callback(event):
        nonlocal canvas
        canvas.focus_set()
        print("clicked at " + str(event.x) + " " + str(event.y))
        print("map bbox = " + str(canvas.bbox(my_map)), "map coords = " + str(canvas.coords(my_map)))

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
        draw_frame(canvas, person, my_map, x_direction, y_direction)
        time.sleep(1/50)


def make_person(canvas, x, y):
    return canvas.create_oval(x + PERSON_WIDTH/2, y + PERSON_WIDTH/2, x - PERSON_WIDTH/2, y - PERSON_WIDTH/2, fill="red")


def draw_frame(canvas, person, my_map, x_direction, y_direction):
    # TODO: stop person at border of image
    # to test if moving away from border prox limit
    canvas.move(person, MOVEMENT_VARIABLE * x_direction, MOVEMENT_VARIABLE * y_direction)
    if is_person_on_edge(canvas, person) == False:
        print("person was not on edge")
    # map_in_frame(canvas, my_map, x_direction, y_direction)
    elif map_in_frame(canvas, my_map, x_direction, y_direction):
        canvas.move(person, MOVEMENT_VARIABLE * -x_direction, MOVEMENT_VARIABLE * -y_direction)
        canvas.move(my_map, MOVEMENT_VARIABLE * -x_direction, MOVEMENT_VARIABLE * -y_direction)
    else:
        print("else")
        # canvas.move(person, MOVEMENT_VARIABLE * -x_direction, MOVEMENT_VARIABLE * -y_direction)
    canvas.update()


def is_person_on_edge(canvas, person):
    if canvas.coords(person)[0] > BORDER_PROX_LIMIT and canvas.coords(person)[1] > BORDER_PROX_LIMIT and canvas.coords(person)[
        2] < CANVAS_WIDTH - BORDER_PROX_LIMIT and canvas.coords(person)[3] < CANVAS_HEIGHT - BORDER_PROX_LIMIT:
        return False
    return True

# BUGGY
def map_in_frame(canvas, my_map, x_direction, y_direction):
    print(canvas.coords(my_map))
    print(canvas.bbox(my_map))
    result = False
    # and canvas.coords(my_map)[2] > CANVAS_WIDTH and canvas.coords(my_map)[3] > CANVAS_HEIGHT
    if canvas.bbox(my_map)[0] <= 0 and canvas.bbox(my_map)[1] <= 0 and canvas.bbox(my_map)[2] >= CANVAS_WIDTH and canvas.bbox(my_map)[3] >= CANVAS_HEIGHT:
        result = True
    return result



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