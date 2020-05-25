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
MOVEMENT_VARIABLE = 7
BORDER_PROX_LIMIT = 300

MAP_IMAGE_FILE_NAME = "images/narnia.jpg"
STANDING_IMAGE_FILE_NAME = "images/person_standing.png"
LEFT_IMAGE_FILE_NAME = "images/person_skating_left.png"
RIGHT_IMAGE_FILE_NAME = "images/person_skating_right.png"
UP_IMAGE_FILE_NAME = "images/person_skating_up.png"
DOWN_IMAGE_FILE_NAME = "images/person_skating_down.png"


def main():
    # MAKE CANVAS
    canvas = make_canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'adventure')

    # MAKE BACKGROUND
    map_image = Image.open(MAP_IMAGE_FILE_NAME)
    map_image = map_image.resize((MAP_WIDTH, MAP_WIDTH), Image.ANTIALIAS)
    map_photo = ImageTk.PhotoImage(map_image)
    my_map = canvas.create_image(CANVAS_MIDDLE_X, CANVAS_MIDDLE_Y, image=map_photo, anchor=CENTER, state=NORMAL)

    # MAKE PERSON
    standing_image = Image.open(STANDING_IMAGE_FILE_NAME)
    standing_image = standing_image.resize((PERSON_WIDTH, PERSON_WIDTH), Image.ANTIALIAS)
    left_image = Image.open(LEFT_IMAGE_FILE_NAME)
    left_image = left_image.resize((PERSON_WIDTH, PERSON_WIDTH), Image.ANTIALIAS)
    right_image = Image.open(RIGHT_IMAGE_FILE_NAME)
    right_image = right_image.resize((PERSON_WIDTH, PERSON_WIDTH), Image.ANTIALIAS)
    up_image = Image.open(UP_IMAGE_FILE_NAME)
    up_image = up_image.resize((PERSON_WIDTH, PERSON_WIDTH), Image.ANTIALIAS)
    down_image = Image.open(DOWN_IMAGE_FILE_NAME)
    down_image = down_image.resize((PERSON_WIDTH, PERSON_WIDTH), Image.ANTIALIAS)
    standing_photo = ImageTk.PhotoImage(standing_image)
    left_photo = ImageTk.PhotoImage(left_image)
    right_photo = ImageTk.PhotoImage(right_image)
    up_photo = ImageTk.PhotoImage(up_image)
    down_photo = ImageTk.PhotoImage(down_image)
    person = canvas.create_image(CANVAS_MIDDLE_X, CANVAS_MIDDLE_Y, image=standing_photo, anchor=CENTER, state=NORMAL)


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

    canvas.bind("<Button-1>", callback)

    canvas.bind("w", pressed_w)
    canvas.bind("a", pressed_a)
    canvas.bind("s", pressed_s)
    canvas.bind("d", pressed_d)
    canvas.pack()

    while True:
        draw_frame(canvas, my_map, person, standing_photo, left_photo, right_photo, up_photo, down_photo, x_direction, y_direction)
        time.sleep(1/50)


"""
def make_map(canvas):
    map_image = Image.open(MAP_IMAGE_FILE_NAME)
    map_image = map_image.resize((MAP_WIDTH, MAP_WIDTH), Image.ANTIALIAS)
    map_photo = ImageTk.PhotoImage(map_image)
    my_map = canvas.create_image(CANVAS_HEIGHT / 2, CANVAS_WIDTH / 2, image=map_photo, anchor=CENTER, state=NORMAL)
    return my_map
"""
"""
OLD PERSON: RED CIRCLE CREATOR
def make_person(canvas, x, y):
    return canvas.create_oval(x + PERSON_WIDTH/2, y + PERSON_WIDTH/2, x - PERSON_WIDTH/2, y - PERSON_WIDTH/2, fill="red")
"""


def draw_frame(canvas, my_map, person, standing_photo, left_photo, right_photo, up_photo, down_photo, x_direction, y_direction):
    # to test if moving away from border prox limit
    update_person(canvas, person, standing_photo, left_photo, right_photo, up_photo, down_photo, x_direction, y_direction)
    canvas.move(person, MOVEMENT_VARIABLE * x_direction, MOVEMENT_VARIABLE * y_direction)
    if person_out_of_bounds(canvas, person, x_direction, y_direction):
        print("person attempting to go out of bounds")
        canvas.move(person, MOVEMENT_VARIABLE * -x_direction, MOVEMENT_VARIABLE * -y_direction)
    else:
        if is_person_in_middle(canvas, person):
            print("person was not on edge")
        elif person_crossing_prox_lim(canvas, person, x_direction, y_direction):
            print("person crossing prox lim")
            if map_can_keep_moving(canvas, my_map, x_direction, y_direction):
                print("map can keep moving")
                canvas.move(person, MOVEMENT_VARIABLE * -x_direction, MOVEMENT_VARIABLE * -y_direction)
                canvas.move(my_map, MOVEMENT_VARIABLE * -x_direction, MOVEMENT_VARIABLE * -y_direction)
            else: print("map cant keep moving")
        else:
            print("person exiting border prox lim")
            # canvas.move(person, MOVEMENT_VARIABLE * -x_direction, MOVEMENT_VARIABLE * -y_direction)
    canvas.update()


def is_person_in_middle(canvas, person):
    # returns true if person is in the middle, not inside any border prox limits
    print(canvas.bbox(person))
    result = False
    if canvas.bbox(person)[0] > BORDER_PROX_LIMIT and canvas.bbox(person)[1] > BORDER_PROX_LIMIT and canvas.bbox(person)[
        2] < CANVAS_WIDTH - BORDER_PROX_LIMIT and canvas.bbox(person)[3] < CANVAS_HEIGHT - BORDER_PROX_LIMIT:
        result = True
    return result


# BUGGY
def map_can_keep_moving(canvas, my_map, x_direction, y_direction):
    # returns true if map still has pixels to show in direction person trying to go in
    # print(canvas.bbox(my_map))
    result = False
    if x_direction == -1:
        if canvas.bbox(my_map)[0] < 0:
            result = True
    elif y_direction == -1:
        if canvas.bbox(my_map)[1] < 0:
            result = True
    elif x_direction == 1:
        if canvas.bbox(my_map)[2] > CANVAS_WIDTH:
            result = True
    elif y_direction == 1:
        if canvas.bbox(my_map)[3] > CANVAS_HEIGHT:
            result = True
    return result


def person_crossing_prox_lim(canvas, person, x_direction, y_direction):
    # returns true if person has crossed the limit in the direction theyve decided to go in
    result = False
    if x_direction == -1:
        if canvas.bbox(person)[0] <= BORDER_PROX_LIMIT:
            result = True
    elif y_direction == -1:
        if canvas.bbox(person)[1] <= BORDER_PROX_LIMIT:
            result = True
    elif x_direction == 1:
        if canvas.bbox(person)[2] >= CANVAS_WIDTH - BORDER_PROX_LIMIT:
            result = True
    elif y_direction == 1:
        if canvas.bbox(person)[3] > CANVAS_HEIGHT - BORDER_PROX_LIMIT:
            result = True
    return result


def person_out_of_bounds(canvas, person, x_direction, y_direction):
    # says if person is out of bounds
    result = False
    if canvas.bbox(person)[0] < 0 or canvas.bbox(person)[1] < 0 or canvas.bbox(person)[2] > CANVAS_WIDTH or canvas.bbox(person)[3] > CANVAS_HEIGHT:
        result = True
    return result


def update_person(canvas, person, standing_photo, left_photo, right_photo, up_photo, down_photo, x_direction, y_direction):
    # configures direction look of person
    if x_direction == -1:
        canvas.itemconfig(person, image=left_photo)
    elif x_direction == 1:
        canvas.itemconfig(person, image=right_photo)
    elif y_direction == -1:
        canvas.itemconfig(person, image=up_photo)
    elif y_direction == 1:
        canvas.itemconfig(person, image=down_photo)
    else:
        canvas.itemconfig(person, image=standing_photo)




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