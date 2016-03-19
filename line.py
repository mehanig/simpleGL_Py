from PIL import Image, ImageOps

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def line(x0, y0, x1, y1, image, color):
    steep = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
    if x0 > x1:
        x0, x1 = x1, x0
    for x in range(x0, x1):
        t = (x-x0) / (x1 - x0)
        y = int(y0 * (1. - t) + y1 * t)
        image[x, y] = color

if __name__ == '__main__':
    img = Image.new('RGB', (255, 255), "black") # create a new black image
    # pixels = ImageOps.flip(img).load()
    pixels = img.load()
    # for i in range(img.size[0]):    # for every pixel:
    #     for j in range(img.size[1]):
    #         pixels[i,j] = (i, j, 100)
    line(200, 200, 160, 160, pixels, red)
    img.show()
