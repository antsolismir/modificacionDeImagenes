from PIL import Image
import PIL
import requests
import numpy as np
import io

def check_channel(array,channel):
    red = 0; blue = 0; green = 0
    if channel == 'Red':
        red = array[0]
    elif channel == 'Green':
        green = array[1]
    elif channel == 'Blue':
        blue = array[2]
    else:
        raise Exception("Sorry, only channels: red, green and blue.")
    return (red,green,blue)

def hex_to_rgb(hex):
    if hex[0] == '#':
        hex = hex.replace('#', '')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def read_image_path(path):
    image = PIL.Image.open('img/generic_error.png')
    try:
        if path[0:4]=='http':
            image=PIL.Image.open(requests.get(path, stream=True).raw)
        else:
            try:
                image=PIL.Image.open(path)
            except:
                pass
        return image
    except:
        return image

def read_image_file(file):
    image = PIL.Image.open('img/generic_error.png')
    try:
        image = PIL.Image.open(file)
    except Exception as e:
        print(e)
    return image

def fig2img(fig): 
    buf = io.BytesIO() 
    fig.savefig(buf) 
    buf.seek(0) 
    img = Image.open(buf) 
    return img

def encuadre(array):
    sol = list()
    for n in array:
        if n >= 1:
            sol.append(1)
        elif n<=0:
            sol.append(0)
        else:
            sol.append(n)
    return sol