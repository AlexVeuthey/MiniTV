from PIL import Image


def open_resize_image(filepath, size):
    img = Image.open(filepath)
    img = img.resize(size, Image.ANTIALIAS)
    return img


def open_nothover_image(filepath, size):
    img = Image.open(filepath)
    img = img.resize((size[0]-40, size[1]-40), Image.ANTIALIAS)

    new_im = Image.new("RGBA", size, (0, 0, 0, 0))

    new_im.paste(img, (20, 20))

    return new_im
