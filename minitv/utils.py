from PIL import Image,ImageEnhance


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

def open_inactive_image(filepath, size, reduce=(40, 40)):
    img = Image.open(filepath)
    img = img.resize((size[0]-reduce[0], size[1]-reduce[1]), Image.ANTIALIAS)
    new_im = Image.new("RGBA", size, (0, 0, 0, 0))
    new_im.paste(img, (20, 20))
    
    enhancer = ImageEnhance.Brightness(new_im)
    new_im = enhancer.enhance(0.75)

    """    A = new_im.getchannel('A')

    # Make all opaque pixels into semi-opaque
    newA = A.point(lambda i: 200 if i>0 else 0)

    # Put new alpha channel back into original image and save
    new_im.putalpha(newA)"""

    return new_im
