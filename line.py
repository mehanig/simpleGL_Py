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


def line_2p(p1, p2, image, color):
    line(p1[0], p1[1], p2[0], p2[1], image, color)


def triangle(t0, t1, t2, image, color):
    # line_2p(t0, t1, image, color)
    # line_2p(t1, t2, image, color)
    # line_2p(t2, t0, image, color)

    if t0[1] > t1[1]:
        t0, t1 = t1, t0
    if t0[1] > t2[1]:
        t0, t2 = t2, t0
    if t1[1] > t2[1]:
        t1, t2 = t2, t1

    # line_2p(t0, t1, image, color)
    # line_2p(t1, t2, image, color)
    # line_2p(t2, t0, image, color)
    total_height = t2[1]-t0[1]
    for y in range(t0[1], t1[1]):
        segm_height = t1[1]-t0[1]+1
        alpha = (y-t0[1])/total_height
        beta = (y-t0[1])/segm_height
        Ax = int(t0[0] + (t2[0]-t0[0])*alpha)
        Bx = int(t0[0] + (t1[0]-t0[0])*beta)
        if Ax > Bx:
            Ax, Bx = Bx, Ax
        for pos in range(Ax, Bx):
            image[pos, y] = color




if __name__ == '__main__':
    width = 499
    height = 499
    img = Image.new('RGB', (width+1, height+1), "black") # create a new black image
    pixels = img.load()

    # model = Model('african_head.obj')
    # for face in model.faces:
    #     len_face = len(face)
    #     for j in range(len_face):
    #         v0 = model.verts[face[j]]
    #         v1 = model.verts[face[(j+1) % len_face]]
    #         x0 = (v0.x+1.) * width/2.
    #         y0 = (v0.y+1.) * height/2.
    #         x1 = (v1.x+1.) * width/2.
    #         y1 = (v1.y+1.) * height/2.
    #         # print('call:', int(x0), int(y0), int(x1), int(y1))
    #         line(int(x0), int(y0), int(x1), int(y1), pixels, green)

    tr0 = [[10, 70], [50, 160], [70, 80]]
    tr1 = [[180, 50], [150, 1], [70, 180]]
    tr2 = [[180, 150], [120, 160], [130, 180]]

    triangle(tr0[0], tr0[1], tr0[2], pixels, red)
    triangle(tr1[0], tr1[1], tr1[2], pixels, blue)
    triangle(tr2[0], tr2[1], tr2[2], pixels, green)

    ImageOps.flip(img).show()

