from PIL import Image, ImageOps

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def line(x0, y0, x1, y1, image, color):
    steep = False
    # if the line is steep, we transpose the image
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    y = y0
    error = 0
    deltaerr = abs((y1 - y0) / (x1 - x0))
    for x in range(x0, x1):
        # // if transposed, de-transpose
        if steep:
            image[y, x] = color
        else:
            image[x, y] = color
        error += deltaerr
        if error > 0.5:
            y = y + 1 if y1 > y0 else y - 1
            error -= 1.


if __name__ == '__main__':
    img = Image.new('RGB', (255, 255), "black") # create a new black image
    pixels = img.load()
    # for i in range(img.size[0]):    # for every pixel:
    #     for j in range(img.size[1]):
    #         pixels[i,j] = (i, j, 100)
    line(0, 0, 120, 160, pixels, red)
    line(160, 160, 120, 10, pixels, blue)
    line(10, 230, 240, 10, pixels, green)
    ImageOps.flip(img).show()
