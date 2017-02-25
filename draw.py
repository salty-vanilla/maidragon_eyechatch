# -*- coding: utf-8 -*-

from PIL import Image, ImageFont, ImageDraw
from images2gif import writeGif
import argparse


def get_bg_image(size=(1920, 1080), color=(251, 233, 61)):
    return Image.new('RGB', size=size, color=color)


def get_font(font_size):
    return ImageFont.truetype("./fonts/meiryo.ttc", font_size)


def inner(msg, font_size):
    font = get_font(font_size=font_size)
    sizes = [font.getsize(text) for text in msg]
    w = max([size[0] for size in sizes])
    h = max([size[1] for size in sizes])

    return w, h


def calc_coord(canvas, msg, offset):
    for font_size in range(500, 0, -10):
        width = canvas.width
        height = canvas.height
        center = (width // 2, height // 2)

        offset_left_x = int(width * offset)
        offset_right_x = width - offset_left_x

        max_w, max_h = inner(msg, font_size)

        pos = [i for i in range(-(len(msg) // 2), len(msg) // 2 + 1)]
        coord = []

        for cha, p in zip(msg, pos):
            x = center[0] + p * int(max_w * 3 / 2)
            y = center[1] - (max_h // 2)
            coord.append((x, y))

        if coord[0][0] > offset_left_x and coord[-1][0] + max_w < offset_right_x:
            return coord, font_size


def draw(canvas, msg, color="#000000", offset=0.2):
    default_msg = "・" * len(msg)
    coord, font_size = calc_coord(canvas=canvas, msg=msg, offset=offset)
    font = get_font(font_size=font_size)

    dst_imgs = []

    for i in range(len(msg) + 1):
        txt = msg[:i] + default_msg[i:]
        img = canvas.copy()
        draw = ImageDraw.Draw(img)
        for (x, y), cha in zip(coord, txt):
            draw.text((x, y), cha, fill=color, font=font)
        dst_imgs.append(img)

    return dst_imgs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('msg', metavar='msg', type=str,
                        help='Message to draw.')
    parser.add_argument('result_prefix', metavar='res_prefix', type=str,
                        default="result",
                        help='Prefix for the saved results.')
    parser.add_argument('--duration', type=float, default=0.5, required=False,
                        help='Duration of animation.')

    args = parser.parse_args()
    msg = args.msg
    result_prefix = args.result_prefix
    duration = args.duration

    canvas = get_bg_image()
    imgs = draw(canvas, msg)

    writeGif(result_prefix + ".gif", imgs, duration=duration)


if __name__ == "__main__":
    main()

