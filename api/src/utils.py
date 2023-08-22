
from PIL import Image, ImageDraw


def geom_plotter(target_img, ref_bounds, geom, color):
    # calculates relative coordinate points
    x1, y1, x2, y2 = ref_bounds
    ix, iy = target_img.size

    gxs, gys = geom.exterior.xy

    xs = [(x - x1) * (ix / (x2 - x1)) for x in gxs]
    ys = [(y2 - y) * (iy / (y2 - y1)) for y in gys]

    coor_seq = list(zip(xs, ys))
    
    outline_draw = ImageDraw.Draw(target_img)
    outline_draw.polygon(coor_seq, outline=color, width=4)
    im = Image.blend(target_img, target_img.copy(), 1)

    inner_draw = ImageDraw.Draw(im)
    inner_draw.polygon(coor_seq, fill=color)
    return Image.blend(target_img, im, 0.4)


def point_plotter(target_img, ref_bounds, point, color, radius=7):

    x1, y1, x2, y2 = ref_bounds
    ix, iy = target_img.size

    [(x, y)] = point

    ex = (x - x1) * (ix / (x2 - x1))
    ey = (y2 - y) * (iy / (y2 - y1))
    
    point = list([(ex - radius, ey - radius), (ex + radius, ey + radius)])
  
    draw = ImageDraw.Draw(target_img)
    draw.ellipse(point, outline=color, fill="white", width=5)

    return target_img