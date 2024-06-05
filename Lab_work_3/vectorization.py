from graphics import *
import numpy as np
import math as mt

st = 100
Pyramid = np.array([[0, 0, 0, 1],
                    [st, 0, 0, 1],
                    [st / 2, st * mt.sqrt(3) / 2, 0, 1],
                    [st / 2, st * mt.sqrt(3) / 6, st * mt.sqrt(2), 1]])


def shift_xyz(Figure, l, m, n):
    f = np.array([[1, 0, 0, l], [0, 1, 0, m], [0, 0, 1, n], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)

    return Prxy


def insert_x(Figure, TetaG):
    TetaR = (3 / 14 * TetaG) / 180
    f = np.array(
        [[1, 0, 0, 0], [0, mt.cos(TetaR), mt.sin(TetaR), 0], [0, -mt.sin(TetaR), mt.cos(TetaR), 0], [0, 0, 0, 1]])
    ft = f.T
    Prxy = Figure.dot(ft)

    return Prxy


def dimetri(Figure, TetaG1, TetaG2):
    TetaR1 = (3 / 14 * TetaG1) / 180
    TetaR2 = (3 / 14 * TetaG2) / 180
    f1 = np.array(
        [[mt.cos(TetaR1), 0, -mt.sin(TetaR1), 0], [0, 1, 0, 0], [mt.sin(TetaR1), 0, mt.cos(TetaR1), 0], [0, 0, 0, 1]])
    ft1 = f1.T
    Prxy1 = Figure.dot(ft1)
    f2 = np.array(
        [[1, 0, 0, 0], [0, mt.cos(TetaR2), mt.sin(TetaR2), 0], [0, -mt.sin(TetaR2), mt.cos(TetaR2), 0], [0, 0, 0, 1]])
    ft2 = f2.T
    Prxy2 = Prxy1.dot(ft2)

    return Prxy2


def create_basic_polynomial(x_values, i):
    def basic_polynomial(x):
        divider = 1
        result = 1
        for j in range(len(x_values)):
            if j != i:
                result *= (x - x_values[j])
                divider *= (x_values[i] - x_values[j])
        return result / divider

    return basic_polynomial


def create_lagrange_polynomial(x_values, y_values):
    basic_polynomials = []
    for i in range(len(x_values)):
        basic_polynomials.append(create_basic_polynomial(x_values, i))

    def lagrange_polynomial(x):
        result = 0
        for i in range(len(y_values)):
            result += y_values[i] * basic_polynomials[i](x)
        return result

    return lagrange_polynomial


def vectorization(x1, y1, x2, y2, win):
    x_values = brez(x1, y1, x2, y2)[0]
    y_values = brez(x1, y1, x2, y2)[1]

    dx = abs(x1 - x2)
    dy = abs(y1 - y2)

    x_vectorized = []
    y_vectorized = []

    if dx > dy:
        lag_pol = create_lagrange_polynomial(x_values, y_values)

        for i in range(len(x_values)):
            x_vectorized.append(x_values[i])
            y_vectorized.append(lag_pol(x_values[i]))

            obj = Point(x_values[i], y_values[i])
            obj.setFill('yellow')
            obj.draw(win)
    else:
        lag_pol = create_lagrange_polynomial(y_values, x_values)

        for i in range(len(x_values)):
            y_vectorized.append(y_values[i])
            x_vectorized.append(lag_pol(y_values[i]))

            obj = Point(x_values[i], y_values[i])
            obj.setFill('yellow')
            obj.draw(win)

    for i in range(len(x_values)):
        obj = Point(x_vectorized[i], y_vectorized[i])
        obj.setFill('blue')
        obj.draw(win)

    return vectorization


def brez(x1, y1, x2, y2):
    x_values = []
    y_values = []

    dx = x2 - x1
    dy = y2 - y1
    sign_x = 1 if dx > 0 else -1 if dx < 0 else 0
    sign_y = 1 if dy > 0 else -1 if dy < 0 else 0
    if dx < 0: dx = -dx
    if dy < 0: dy = -dy
    if dx > dy:
        pdx, pdy = sign_x, 0
        es, el = dy, dx
    else:
        pdx, pdy = 0, sign_y
        es, el = dx, dy
    x, y = x1, y1
    error, t = el / 2, 0

    while t < el:
        error -= es
        if error < 0:
            error += el
            x += sign_x
            y += sign_y
        else:
            x += pdx
            y += pdy
        t += 1

        x_values.append(x)
        y_values.append(y)

    return x_values, y_values


def create_polygon(win, points, fill_color):
    obj = Polygon(*points)
    obj.setFill(fill_color)
    obj.draw(win)


def PrlpdWizReal_G(PrxyDIM, Xmax, Ymax, Zmax, win):
    Ax = PrxyDIM[0, 0]; Ay = PrxyDIM[0, 1]; Az = PrxyDIM[0, 2]
    Bx = PrxyDIM[1, 0]; By = PrxyDIM[1, 1]; Bz = PrxyDIM[1, 2]
    Cx = PrxyDIM[2, 0]; Cy = PrxyDIM[2, 1]; Cz = PrxyDIM[2, 2]
    Dx = PrxyDIM[3, 0]; Dy = PrxyDIM[3, 1]; Dz = PrxyDIM[3, 2]

    FlagF = 1 if (abs(Az - Zmax) > abs(Dz - Zmax)) else 2

    FlagR = 1 if (abs(Dx - Xmax) > abs(Bx - Xmax)) else 2

    FlagP = 1 if (abs(Ay - Ymax) > abs(Dy - Ymax)) else 2

    if FlagP == 2:
        create_polygon(win, [Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy)], 'orange')
    if FlagP == 1:
        create_polygon(win, [Point(Ax, Ay), Point(Cx, Cy), Point(Dx, Dy)], 'violet')
    if FlagR == 1:
        create_polygon(win, [Point(Ax, Ay), Point(Bx, By), Point(Dx, Dy)], 'indigo')
    if FlagR == 2:
        create_polygon(win, [Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy)], 'indigo')
    if FlagF == 2:
        create_polygon(win, [Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy)], 'blue')
    if FlagF == 1:
        create_polygon(win, [Point(Ax, Ay), Point(Bx, By), Point(Cx, Cy), Point(Dx, Dy)], 'green')

    return PrlpdWizReal_G


if __name__ == '__main__':
    # ----------------------------------- початкові параметри ------------------------------
    xw = 600
    yw = 600
    st = 50
    TetaG1 = 20
    TetaG2 = 120
    l = (xw / 2) - st
    m = (yw / 2) - st
    n = m

    win = GraphWin("3-D векторна піраміда з трикутною основою, проекція на ХУ", xw, yw)
    win.setBackground('white')
    Pyr1 = shift_xyz(Pyramid, l, m, n)

    Pyr2 = dimetri(Pyr1, TetaG1, TetaG2)

    # Видалення невидимих граней методом алгоритму художника
    PrlpdWizReal_G(Pyr2, (xw * 2), (yw * 2), (yw * 2), win)

    win.getMouse()
    win.close()
