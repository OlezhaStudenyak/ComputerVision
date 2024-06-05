import math

from graphics import *
import time
import numpy as np

xw = 600
yw = 600

st = 60
side = 60
half_side = side / 2
h = math.sqrt(side ** 2 - half_side ** 2)

teta_d = 90
teta = (3 / 14 * teta_d) / 180

Sx = 2
Sy = 1.5


def create_win(title):
    win = GraphWin(title, xw, yw)
    win.setBackground('white')
    return win


def draw_triangle(win, poit_a, poit_b, poit_c):
    obj = Polygon(poit_a, poit_b, poit_c)
    obj.draw(win)


def create_start_triangle():
    x1 = st
    y1 = yw - st
    x2 = x1 + half_side
    y2 = y1 - h
    x3 = x1 + side
    y3 = y1
    return np.array([[x1, y1], [x2, y2], [x3, y3]])


def move_poit(x, y):
    a = np.array([[x, y, 1]])
    f = np.array([[1, 0, half_side], [0, 1, -h], [0, 0, 1]])
    ft = f.T
    total = a.dot(ft)
    return total


def move_poit_plus(x, y, plus):
    a = np.array([[x, y, 1]])
    f = np.array([[1, 0, half_side + plus], [0, 1, -h - plus], [0, 0, 1]])
    ft = f.T
    total = a.dot(ft)
    return total


def rotate_point(x, y):
    a = np.array([[x, y, 1]])
    f = np.array([[math.cos(teta), -math.sin(teta), 0], [math.sin(teta), math.cos(teta), 0], [0, 0, 1]])
    ft = f.T
    total = a.dot(ft)
    return total

def scale_point(x, y):
    a = np.array([[x, y, 1]])
    f = np.array([[Sx, 0, 0], [0, Sy, 0], [0, 0, 1]])
    ft = f.T
    total = a.dot(ft)
    return total


# Moving
win = create_win("2-D Moving")

poit = create_start_triangle()
x1 = poit[0, 0]
y1 = poit[0, 1]
x2 = poit[1, 0]
y2 = poit[1, 1]
x3 = poit[2, 0]
y3 = poit[2, 1]
draw_triangle(win, Point(x1, y1), Point(x2, y2), Point(x3, y3))

stop = xw / side
stop = float(stop)
ii = int(stop)

for i in range(ii):
    time.sleep(0.3)

    total = move_poit(x1, y1)
    x1 = total[0, 0]
    y1 = total[0, 1]

    total = move_poit(x2, y2)
    x2 = total[0, 0]
    y2 = total[0, 1]

    total = move_poit(x3, y3)
    x3 = total[0, 0]
    y3 = total[0, 1]

    draw_triangle(win, Point(x1, y1), Point(x2, y2), Point(x3, y3))

win.getMouse()
win.close()

# Rotating
win = create_win("2-D Rotating")

poit = create_start_triangle()
x1 = poit[0, 0]
y1 = poit[0, 1]
x2 = poit[1, 0]
y2 = poit[1, 1]
x3 = poit[2, 0]
y3 = poit[2, 1]

draw_triangle(win, Point(x1, y1), Point(x2, y2), Point(x3, y3))

stop = xw / side * 6
stop = float(stop)
ii = int(stop)

for i in range(ii):
    time.sleep(0.3)

    total = move_poit(x1, y1)
    total = rotate_point(total[0, 0], total[0, 1])
    x1 = total[0, 0]
    y1 = total[0, 1]

    total = move_poit(x2, y2)
    total = rotate_point(total[0, 0], total[0, 1])
    x2 = total[0, 0]
    y2 = total[0, 1]

    total = move_poit(x3, y3)
    total = rotate_point(total[0, 0], total[0, 1])
    x3 = total[0, 0]
    y3 = total[0, 1]

    draw_triangle(win, Point(x1, y1), Point(x2, y2), Point(x3, y3))

win.getMouse()
win.close()

# Scaling
win = create_win("2-D Scaling")

poit = create_start_triangle()
x1 = poit[0, 0]
y1 = poit[0, 1]
x2 = poit[1, 0]
y2 = poit[1, 1]
x3 = poit[2, 0]
y3 = poit[2, 1]

draw_triangle(win, Point(x1, y1), Point(x2, y2), Point(x3, y3))

total = move_poit_plus(x1, y1, 100)
total = scale_point(total[0, 0], total[0, 1])
x1 = total[0, 0]
y1 = total[0, 1]

total = move_poit_plus(x2, y2, 100)
total = scale_point(total[0, 0], total[0, 1])
x2 = total[0, 0]
y2 = total[0, 1]

total = move_poit_plus(x3, y3, 100)
total = scale_point(total[0, 0], total[0, 1])
x3 = total[0, 0]
y3 = total[0, 1]

draw_triangle(win, Point(x1, y1), Point(x2, y2), Point(x3, y3))

win.getMouse()
win.close()
