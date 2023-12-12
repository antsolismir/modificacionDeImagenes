from PIL import Image
import PIL
import requests
import numpy as np
import io
import re
import matplotlib.pyplot as plt

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

def normalizacion(array):
    maximo = max(array)
    minimo = min(array)
    n_array = []
    for valor in array:
        if maximo == minimo:
            n_array.append(maximo)
        else:
            n_array.append((valor - minimo) / (maximo - minimo))
            
    return n_array

replacements = {
    'sin' : 'np.sin',
    'cos' : 'np.cos',
    'exp': 'np.exp',
    'sqrt': 'np.sqrt',
    'floor': 'np.floor',
    'ceil': 'np.ceil',
    '^': '**',
}

allowed_words = [
    'x',
    'sin',
    'cos',
    'sqrt',
    'exp',
    'floor',
    'ceil',
]

def string2func(string):
    try:
        lista = list()
        for word in re.findall('[a-zA-Z_]+', string):
            lista.append(word)
            if word not in allowed_words:
                raise ValueError(
                    '"{}" is forbidden to use in math expression'.format(word)
                )

        for old, new in replacements.items():
            string = string.replace(old, new)
            
        if string.find('x') == -1:
            string += '+0*x'
        
        def func(x):
            return eval(string)
        
        return func
    except Exception as e:
        return e

if __name__ == '__main__':
    x = np.linspace(0, 256, 256)
    y = 0.5+0.0*x
    print(normalizacion(y))