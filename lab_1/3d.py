from graphics import *
import numpy as np
import math as mt
import time

xw = 600
yw = 600
st = 200

# Define the vertices of the triangular-based pyramid
figure = np.array([[0, 0, 0, 1],    # Point A
                   [st, 0, 0, 1],   # Point B
                   [st / 2, st * mt.sqrt(3) / 2, 0, 1],  # Point C (base triangle)
                   [st / 2, st / (2 * mt.sqrt(3)), st * 2, 1]])  # Point D (apex)

def create_win(title):
    win = GraphWin(title, xw, yw)
    win.setBackground('white')
    return win

def move_center(figure):
    m = xw / 3
    f = np.array([[1, 0, 0, m], [0, 1, 0, m], [0, 0, 1, m], [0, 0, 0, 1]])  # по строках
    ft = f.T
    Prxy = figure.dot(ft)
    return Prxy

def dimetri(figure, TetaG1, TetaG2):
    TetaR1 = (3 / 14 * TetaG1) / 180
    TetaR2 = (3 / 14 * TetaG2) / 180

    f1 = np.array(
        [[mt.cos(TetaR1), 0, -mt.sin(TetaR1), 0], [0, 1, 0, 0], [mt.sin(TetaR1), 0, mt.cos(TetaR1), 0], [0, 0, 0, 1]])
    ft1 = f1.T
    Prxy1 = figure.dot(ft1)

    f2 = np.array(
        [[1, 0, 0, 0], [0, mt.cos(TetaR2), mt.sin(TetaR2), 0], [0, -mt.sin(TetaR2), mt.cos(TetaR2), 0], [0, 0, 0, 1]])
    ft2 = f2.T
    Prxy2 = Prxy1.dot(ft2)
    return Prxy2

def draw(figure, outlineColor):
    A = Point(figure[0, 0], figure[0, 1])
    B = Point(figure[1, 0], figure[1, 1])
    C = Point(figure[2, 0], figure[2, 1])
    D = Point(figure[3, 0], figure[3, 1])

    # Draw base triangle
    base = Polygon(A, B, C)
    base.setOutline(outlineColor)
    base.draw(win)

    # Draw sides of the pyramid
    side1 = Polygon(A, B, D)
    side1.setOutline(outlineColor)
    side1.draw(win)

    side2 = Polygon(B, C, D)
    side2.setOutline(outlineColor)
    side2.draw(win)

    side3 = Polygon(C, A, D)
    side3.setOutline(outlineColor)
    side3.draw(win)

win = create_win("3-D Pyramid")

Figure1 = move_center(figure)
Figure2 = dimetri(Figure1, 180, -90)
draw(Figure2, "black")
time.sleep(1)
draw(Figure2, "gray")
time.sleep(1)
draw(Figure2, "dark gray")
time.sleep(1)
draw(Figure2, "light gray")
time.sleep(1)
draw(Figure2, "white")

win.getMouse()
win.close()
