import random
import math
from collections import namedtuple

from PIL import Image, ImageOps

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
randcolor = lambda: (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
gray_intencify = lambda x: (int(255 * x), int(255 * x), int(255 * x))

Point2d = namedtuple('Point2d', ['x', 'y'])
Point3d = namedtuple('Point3d', ['x', 'y', 'z'])


class Model:
    Point = namedtuple('Point', ['x', 'y', 'z'])

    def __init__(self, path):
        self.verts = []
        self.faces = []
        with open(path) as file:
            for f_line in file:
                if f_line.startswith('v '):
                    _, x, y, z = f_line.split()
                    self.verts.append(Point3d(float(x), float(y), float(z)))
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
    t0 = Point2d(*t0)
    t1 = Point2d(*t1)
    t2 = Point2d(*t2)
    if t0.y > t1.y:
        t0, t1 = t1, t0
    if t0.y > t2.y:
        t0, t2 = t2, t0
    if t1.y > t2.y:
        t1, t2 = t2, t1

    total_height = t2.y-t0.y
    for i in range(total_height):
        second_half = i > t1.y-t0.y or t1.y == t0.y
        segm_height = t2.y-t1.y if second_half else t1.y-t0.y
        alpha = i/total_height
        beta = (i-(t1.y-t0.y))/segm_height if second_half else i/segm_height
        Ax = int(t0.x + (t2.x-t0.x)*alpha)
        Bx = int(t1.x + (t2.x-t1.x)*beta) if second_half else int(t0.x + (t1.x-t0.x)*beta)
        if Ax > Bx:
            Ax, Bx = Bx, Ax
        for pos in range(Ax, Bx):
            image[pos, t0.y+i] = color


def cross_product(_v1, _v2):
    c = [_v1[1]*_v2[2] - _v1[2]*_v2[1],
         _v1[2]*_v2[0] - _v1[0]*_v2[2],
         _v1[0]*_v2[1] - _v1[1]*_v2[0]]
    return Point3d(*c)


def vect3d_minus(_v1, _v2):
    return Point3d(_v1.x-_v2.x, _v1.y-_v2.y, _v1.z-_v2.z)


def vect3d_mult(_v1, _v2):
    return _v1.x*_v2.x + _v1.y*_v2.y + _v1.z*_v2.z


def normalize(_v):
    norm = math.sqrt(_v.x ** 2 + _v.y ** 2 + _v.z ** 2)
    mult = 1/norm
    return Point3d(_v.x*mult, _v.y*mult, _v.z*mult)


if __name__ == '__main__':
    width = 699
    height = 699
    img = Image.new('RGB', (width+1, height+1), "black") # create a new black image
    pixels = img.load()

    model = Model('african_head.obj')
    light_dir = Point3d(0, 0, -1)
    for face in model.faces:
        len_face = len(face)
        triangle_coords = []
        world_coords = []
        for j in range(len_face):
            v0 = model.verts[face[j]]
            v1 = model.verts[face[(j+1) % len_face]]
            x0 = (v0.x+1.) * width/2
            y0 = (v0.y+1.) * height/2
            triangle_coords.append([int(x0), int(y0)])
            world_coords.append(v0)
        v1 = vect3d_minus(world_coords[2], world_coords[0])
        v2 = vect3d_minus(world_coords[1], world_coords[0])
        normal = normalize(cross_product(v1, v2))
        intencity = vect3d_mult(normal, light_dir)
        if intencity > 0:
            triangle(triangle_coords[0], triangle_coords[1], triangle_coords[2], pixels, gray_intencify(intencity))

    ImageOps.flip(img).show()

