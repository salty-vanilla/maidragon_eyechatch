from PIL import Image


def get_bg_image(size=(1920, 1080), color=(251, 233, 61)):
    return Image.new('RGB', size=size, color=color)


def get_font(fontsize):


def calc_place(image, msg):
    width = image.width
    height = image.height



image = get_bg_image()
calc_place(image=image, msg="aaaaa")
