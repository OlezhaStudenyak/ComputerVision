import numpy as np
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt


def image_read(file_name: str) -> dict:
    image = Image.open(file_name)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    plt.imshow(image)
    plt.show()
    image_info = {"image_file": image, "image_draw": draw, "image_width": width, "image_height": height,
                  "image_pix": pix}

    return image_info


def brightness_change(source_file: str, destination_file: str, delta: int) -> None:
    image_info = image_read(source_file)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    for i in range(width):
        for j in range(height):
            r = min(255, max(0, pix[i, j][0] + delta))
            g = min(255, max(0, pix[i, j][1] + delta))
            b = min(255, max(0, pix[i, j][2] + delta))
            draw.point((i, j), (r, g, b))

    plt.imshow(image)
    plt.show()
    image.save(destination_file, "JPEG")
    del draw

    return


def shades_of_gray(source_file: str, destination_file: str) -> None:
    image_info = image_read(source_file)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    for i in range(width):
        for j in range(height):
            r = pix[i, j][0]
            g = pix[i, j][1]
            b = pix[i, j][2]
            av = (r + g + b) // 3
            draw.point((i, j), (av, av, av))

    plt.imshow(image)
    plt.show()
    image.save(destination_file, "JPEG")
    del draw

    return


def negative(source_file: str, destination_file: str) -> None:
    image_info = image_read(source_file)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    for i in range(width):
        for j in range(height):
            r = 255 - pix[i, j][0]
            g = 255 - pix[i, j][1]
            b = 255 - pix[i, j][2]

            draw.point((i, j), (r, g, b))

    plt.imshow(image)
    plt.show()
    image.save(destination_file, "JPEG")
    del draw

    return


def green_tint(source_file: str, destination_file: str) -> None:
    image_info = image_read(source_file)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    gradient_matrix = np.linspace(0, 1, width * height)

    for i in range(width):
        for j in range(height):
            draw_green_tint(draw, pix, i, j, int(gradient_matrix[j * i] * 255))

    plt.imshow(image)
    plt.show()
    image.save(destination_file, "JPEG")
    del draw

    return


def green_tint_spiral_order_in(source_file: str, destination_file: str):
    image_info = image_read(source_file)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    seen = [[0 for _ in range(height)] for _ in range(width)]
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    x = 0
    y = 0
    di = 0

    depth = 0
    iteration = width * height
    iteration_for_rise = iteration // 255

    gradient_matrix = np.linspace(0, 1, width * height)

    # Iterate from 0 to R * C - 1
    for i in range(width * height):

        if i % iteration_for_rise == 0:
            depth = depth + 1

        draw_green_tint(draw, pix, x, y, int(gradient_matrix[i] * 255))

        seen[x][y] = True
        cr = x + dr[di]
        cc = y + dc[di]

        if (0 <= cr and cr < width and 0 <= cc and cc < height and not (seen[cr][cc])):
            x = cr
            y = cc
        else:
            di = (di + 1) % 4
            x += dr[di]
            y += dc[di]

    plt.imshow(image)
    plt.show()

    image.save(destination_file, "JPEG")
    del draw

    return


def green_tint_spiral_order_out(source_file: str, destination_file: str):
    image_info = image_read(source_file)
    image = image_info["image_file"]
    draw = image_info["image_draw"]
    width = image_info["image_width"]
    height = image_info["image_height"]
    pix = image_info["image_pix"]

    seen = [[0 for _ in range(height)] for _ in range(width)]
    dr = [0, 1, 0, -1]
    dc = [1, 0, -1, 0]
    x = 0
    y = 0
    di = 0

    depth = 0
    iteration = width * height
    iteration_for_rise = iteration // 255

    gradient_matrix = np.linspace(0, 1, width * height)

    for i in range(width * height):

        if i % iteration_for_rise == 0:
            depth = depth + 1

        draw_green_tint(draw, pix, x, y, int(gradient_matrix[width * height - i - 1] * 255))

        seen[x][y] = True
        cr = x + dr[di]
        cc = y + dc[di]

        if (0 <= cr and cr < width and 0 <= cc and cc < height and not (seen[cr][cc])):
            x = cr
            y = cc
        else:
            di = (di + 1) % 4
            x += dr[di]
            y += dc[di]

    plt.imshow(image)
    plt.show()

    image.save(destination_file, "JPEG")
    del draw

    return


def draw_green_tint(draw, pix, x, y, depth):
    r = pix[x, y][0]
    g = pix[x, y][1]
    b = pix[x, y][2]
    tr = int(0.272 * r + 0.534 * g + 0.131 * b)
    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
    tb = int(0.393 * r + 0.769 * g + 0.189 * b)
    r = min(255, tr)
    g = min(255, tg + depth)
    b = min(255, tb)

    draw.point((x, y), (r, g, b))


if __name__ == "__main__":
    source_file = 'image.png'

    brightness_change(source_file, "brightness.jpg", 100)
    shades_of_gray(source_file, "shades_of_gray.jpg")
    negative(source_file, "negative.jpg")
    green_tint(source_file, "green_tint.jpg")
    green_tint_spiral_order_in(source_file, "green_tint_spiral_order_in.jpg")
    green_tint_spiral_order_out(source_file, "green_tint_spiral_order_out.jpg")
