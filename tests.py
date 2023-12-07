import PIL
import requests
import numpy as np
import sys
import functions as f
import utils as utilities
import filtros

import cv2
import matplotlib.pyplot as plt

def rgb_to_hsv(rgb):
    # Normalizar los valores RGB
    r, g, b = [x / 255.0 for x in rgb]
    # Calcular el valor mínimo y máximo entre R, G y B
    cmin, cmax = min(r, g, b), max(r, g, b)
    delta = cmax - cmin
    # Calcular el componente de la luminosidad
    v = cmax
    # Calcular la saturación
    if cmax != 0:
        s = delta / cmax
    else:
        s = 0
    # Calcular el matiz
    if delta == 0:
        h = 0
    elif cmax == r:
        h = 60 * (((g - b) / delta) % 6)
    elif cmax == g:
        h = 60 * (((b - r) / delta) + 2)
    elif cmax == b:
        h = 60 * (((r - g) / delta) + 4)

    return (round(h), round(s * 100), round(v * 100))

def hsv_to_rgb(hsv):
    # Desempaquetar los valores HSV
    h, s, v = hsv

    # Calcular c, x, y
    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    y = v - c

    # Definir los valores iniciales de r, g, b
    r, g, b = 0, 0, 0

    # Asignar valores según la sexta parte del círculo en que se encuentra el matiz
    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    elif 300 <= h < 360:
        r, g, b = c, 0, x

    # Añadir los valores y a r, g, b
    r, g, b = r + y, g + y, b + y

    # Convertir a enteros en el rango [0, 255]
    r, g, b = round(r * 255), round(g * 255), round(b * 255)

    return (r, g, b)

def hex_to_hsv(color_hex):
    # Convertir color hexadecimal a formato RGB
    rgb = hex2color(color_hex)

    # Convertir formato RGB a formato HSV
    hsv = rgb_to_hsv(rgb)

    # Escalar los valores de H, S, V al rango [0, 255] y redondear
    h = round(hsv[0] * 255)
    s = round(hsv[1] * 255)
    v = round(hsv[2] * 255)

    return (h, s, v)

def hsv_image(image, hex):
    # EN HSL LOS PIXELS ESTAN DEFINIDOS DE LA SIGUIENTE MANERA: (COLOR (HUE)(EN GRADOS), BRILLO (SATURATION)(CUAN DE CERCANO ES AL BLANCO), OSCURIDAD (VALUE)(CUAN CERCANO ES AL NEGRO))
    imagen = PIL.Image.open(image)
    #imagen.show()
    imagen_hsv = imagen.convert('HSV')
    pixels = imagen_hsv.load()
    #rgb = utilities. hex_to_rgb(hex)
    #color = rgb_to_hsv(rgb)
    color=hex_to_hsv(hex)
    
    old_image = imagen.load()
    ancho, alto = imagen.size
    new_image_rgb = []
    new_image_hsv = []
    x=0; y=0
    while y < alto:
        h = color[0]
        s = pixels[x,y][1]
        v = pixels[x,y][2]
        pixel = (h,s,v)
        new_image_rgb.append(hsv_to_rgb(pixel))
        new_image_hsv.append(pixel)
        x+=1
        if x >= ancho:
            x=0
            y+=1
    
    sol_rgb = PIL.Image.new("RGB", (ancho, alto))
    sol_rgb.putdata(new_image_rgb)
    
    sol_hsv = PIL.Image.new("HSV", (ancho, alto))
    sol_hsv.putdata(new_image_hsv)
    return sol_rgb, sol_hsv



if __name__ == '__main__':

    imagen_pil = PIL.Image.open('piezas.jpg').convert('L')
    imagen = np.array(imagen_pil)
    
    filtros.filtro_pasa_baja_no_ideal(imagen,512,0.01).show()
    filtros.filtro_pasa_baja_ideal(imagen,10).show()
    
    filtros.filtro_pasa_alta_no_ideal(imagen,512,0.01).show()
    filtros.filtro_pasa_alta_ideal(imagen,10).show()
