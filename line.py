from collections import namedtuple

from PIL import Image, ImageOps

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)


class Model:
    Point = namedtuple('Point', ['x', 'y', 'z'])

    def __init__(self, path):
        self.verts = []
        self.faces = []
        with open(path) as file:
            for f_line in file:
                if f_line.startswith('v '):
                    _, x, y, z = f_line.split()
                    self.verts.append(Model.Point(float(x), float(y), float(z)))
                if f_line.startswith('f '):
                    values = map(lambda _x: _x.split('/')[0], f_line.split())
                    self.faces.append(list(map(lambda _x: int(_x)-1, list(values)[1:])))


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
    dx = x1 - x0
    dy = y1 - y0
    derror2 = abs(dy) * 2
    error2 = 0
    for x in range(x0, x1):
        # // if transposed, de-transpose
        if steep:
            image[y, x] = color
        else:
            image[x, y] = color
        error2 += derror2
        if error2 > dx:
            y = y + 1 if y1 > y0 else y - 1
            error2 -= dx*2


if __name__ == '__main__':
    width = 1999
    height = 1999
    img = Image.new('RGB', (width+1, height+1), "black") # create a new black image
    pixels = img.load()
    model = Model('african_head.obj')
    for face in model.faces:
        len_face = len(face)
        for j in range(len_face):
            v0 = model.verts[face[j]]
            v1 = model.verts[face[(j+1) % len_face]]
            x0 = (v0.x+1.) * width/2.
            y0 = (v0.y+1.) * height/2.
            x1 = (v1.x+1.) * width/2.
            y1 = (v1.y+1.) * height/2.
            # print('call:', int(x0), int(y0), int(x1), int(y1))
            line(int(x0), int(y0), int(x1), int(y1), pixels, green)
    ImageOps.flip(img).show()

