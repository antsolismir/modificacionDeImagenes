import PIL
import utils as utilities

###################################
#                                 #
# This is where the magic happens #
#                                 #
###################################

# METHODS TO CREATE IMAGES
def create_image(color, ancho, alto):
    tam_x=ancho
    tam_y=alto
    
    pixels = []
    red,green,blue = utilities.hex_to_rgb(color)
    x=0
    y=0
    while y < tam_y:
        pixels.append((red, green, blue))
        x+=1
        if x >= tam_x:
            x=0
            y+=1
    im = PIL.Image.new("RGB", (ancho, alto))
    im.putdata(pixels)
    return im
#============================#

# METHODS TO CHANGE IMAGE COLOR
def image_to_one_channel(imagen,channel):
    #imagen = PIL.Image.open(image)
    old_image = imagen.load()
    ancho, alto = imagen.size
    new_image = []
    x=0; y=0
    while y < alto:
        pixel = utilities.check_channel(old_image[x,y],channel)
        new_image.append(pixel)
        x+=1
        if x >= ancho:
            x=0
            y+=1
    
    sol = PIL.Image.new("RGB", (ancho, alto))
    sol.putdata(new_image)
    return sol

def image_to_hex_color(imagen, color_hex):
    #imagen = PIL.Image.open(imagen_path)
    ancho, alto = imagen.size

    rgb = utilities.hex_to_rgb(color_hex)
    pixels_imagen = imagen.load()
    imagen_combinada = []

    x=0; y=0
    while y < alto:
        red, green, blue = pixels_imagen[x,y]
        intensidad = int((299/1000)*red) + int((587/1000)*blue) + int((114/1000)*green)
        r_mascara=rgb[0];g_mascara=rgb[1];b_mascara=rgb[2]
        
        r_combinado = (intensidad * r_mascara) // 255
        g_combinado = (intensidad * g_mascara) // 255
        b_combinado = (intensidad * b_mascara) // 255
        
        imagen_combinada.append((r_combinado,g_combinado,b_combinado))
        x+=1
        if x >= ancho:
            x=0
            y+=1

    sol = PIL.Image.new("RGB", (ancho, alto))
    sol.putdata(imagen_combinada)
    return sol

def image_to_gray(imagen):
    #La formula para cambiar de color (RGB) a blanco y negro (gris) es la siguiente: Y = 0.299xR + 0.587xG + 0.114xB
    #imagen = PIL.Image.open(image)
    old_image = imagen.load()
    ancho, alto = imagen.size
    new_image = []
    x=0; y=0
    while y < alto:
        red = old_image[x,y][0]; blue = old_image[x,y][1]; green = old_image[x,y][2]
        luminance = int((299/1000)*red) + int((587/1000)*blue) + int((114/1000)*green)
        new_image.append(luminance)
        x+=1
        if x >= ancho:
            x=0
            y+=1
    
    sol = PIL.Image.new("L", (ancho, alto))
    sol.putdata(new_image)
    return sol

def image_plus_image(imagen1,imagen2):
    #La formula para cambiar de color (RGB) a blanco y negro (gris) es la siguiente: Y = 0.299xR + 0.587xG + 0.114xB
    #imagen = PIL.Image.open(image)
    ancho, alto = imagen2.size
    imagen1 = imagen1.resize(imagen2.size)
    imagen2 = imagen2.load()
    imagen1 = imagen1.load()
    new_image = []
    x=0; y=0
    while y < alto:
        luminance = (imagen1[x,y]+imagen2[x,y])/2
        new_image.append(luminance)
        x+=1
        if x >= ancho:
            x=0
            y+=1
    
    sol = PIL.Image.new("L", (ancho, alto))
    sol.putdata(new_image)
    return sol
#============================#