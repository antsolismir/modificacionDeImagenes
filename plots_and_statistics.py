from PIL import Image
import PIL
import requests
import numpy as np
import matplotlib.pyplot as plt
import utils as utilities
import functions as f
import cv2
import statistics as s

def histograma_blanco_negro(imagen):
    ancho, alto = imagen.size
    matrix = np.zeros([256])
    if imagen.mode != 'L':
        imagen = imagen.convert("L")
    imagen = imagen.load()
    x=0
    y=0
    while y < alto:
        matrix[imagen[x,y]] += 1
        x+=1
        if x >= ancho:
            x=0
            y+=1
    
    x = np.arange(len(matrix))
    y = np.array(matrix)
    plt.title("Histograma de la imagen en blanco y negro")
    plt.xlabel("Rango de grises") 
    plt.ylabel("Numero de pixeles") 
    plt.bar(x, y, color ="blue") 
    grafica = utilities.fig2img(plt.gcf())
    plt.clf()
    return grafica

def rgb_to_hsl(rgb):
    r, g, b = rgb
    
    r = r/255.0
    g = g/255.0
    b = b/255.0
    
    maximo = max(r, g, b)
    minimo = min(r, g, b)
    delta = maximo - minimo

    # Calcular el componente Lightness
    L = (maximo + minimo)/2.0
    
    if maximo == minimo:
        S = 0.0
        H = 0.0
    else:
        S = (maximo - minimo)/(1.0 - abs(2.0 * L - 1.0))
        
        # Calcular el componente Hue
        if maximo == r:
            H = (g - b) / delta
        elif maximo == g:
            H = 2.0 + (b - r) / delta
        else:
            H = 4.0 + (r - g) / delta

        if H != None:
            H = H * 60.0
            if H < 0.0:
                H = H + 360.0

    return (int(H), int(S*100), int(L*100))

def histograma_color(imagen):
    ancho, alto = imagen.size
    matrix = np.zeros([360])
    if imagen.mode != 'RGB':
        imagen = imagen.convert("RGB")
    imagen = imagen.load()
    x=0
    y=0
    while y < alto:
        pixel_hsl = rgb_to_hsl(imagen[x,y])
        matrix[pixel_hsl[0]] += 1
        x+=1
        if x >= ancho:
            x=0
            y+=1
    
    x = np.arange(len(matrix))
    y = np.array(matrix)
    plt.title("Histograma de la imagen a color")
    plt.xlabel("Rango de colores (0 Rojo, 120 Verde, 240 Azul, 360 Rojo)") 
    plt.ylabel("Numero de pixeles") 
    plt.bar(x, y, color ="red")
    grafica = utilities.fig2img(plt.gcf())
    plt.clf()
    return grafica

def image_bn_to_fake_color(imagen,y_red,y_green,y_blue):
    
    imagen = imagen.convert('L')
    
    #SE GUARDA EN UN UNA TUPLA DE TUPLAS, CUYAS TUPLAS SON CADA TRIO RGB QUE SUSTITUIRA
    #AL TONO DE GRIS 
    grafica_rgb = tuple(zip(y_red, y_green, y_blue))
    
    old_image = imagen.load()
    ancho, alto = imagen.size
    new_image = []
    x=0; y=0
    while y < alto:
        tono_gris = old_image[x,y]
        red = int(grafica_rgb[tono_gris][0]*255)
        green = int(grafica_rgb[tono_gris][1]*255)
        blue = int(grafica_rgb[tono_gris][2]*255)
        pixel = (red,green,blue)
        new_image.append(pixel)
        x+=1
        if x >= ancho:
            x=0
            y+=1
    
    sol = PIL.Image.new("RGB", (ancho, alto))
    sol.putdata(new_image)
    return sol

def varianza_minima(imagen):
    # Convertir la imagen a escala de grises
    imagen_gris = imagen.convert('L')
    pixels = list(imagen_gris.getdata())

    # Número de iteraciones máximo
    max_iteraciones = 10

    # Inicializar umbral inicial
    umbral = (np.mean(pixels) + np.max(pixels)) / 2

    for iteracion in range(max_iteraciones):
        # Calcular los valores medios de los dos segmentos
        segmento_0 = [pixel for pixel in pixels if pixel <= umbral]
        segmento_1 = [pixel for pixel in pixels if pixel > umbral]

        mu_1 = np.mean(segmento_0)
        mu_2 = np.mean(segmento_1)

        # Calcular el umbral para esta iteración
        nuevo_umbral = (mu_1 + mu_2) / 2

        # Verificar si el umbral ha convergido
        if abs(nuevo_umbral - umbral) < 0.5:
            break

        umbral = nuevo_umbral

    # Binarizar la imagen con el umbral final
    nueva_imagen = Image.new('L', imagen_gris.size)
    nuevos_pixels = [0 if pixel <= umbral else 255 for pixel in pixels]
    nueva_imagen.putdata(nuevos_pixels)
    
    grafica = histograma_blanco_negro(nueva_imagen)

    return nueva_imagen, grafica

def sliding(imagen):
    pass

def varianza(imagen):
    ancho, alto = imagen.size
    if imagen.mode != 'L':
        imagen = imagen.convert("L")
    imagen = imagen.load()
    new_array=[]
    x=0
    y=0
    while y < alto:
        new_array.append(imagen[x,y]) 
        x+=1
        if x >= ancho:
            x=0
            y+=1
            
    return s.mean(new_array)

def binarizacion_por_umbral(imagen, umbral):
    ancho, alto = imagen.size
    if imagen.mode != 'L':
        imagen = imagen.convert("L")
    imagen = imagen.load()
    new_image=[]
    x=0
    y=0
    while y < alto:
        if imagen[x,y] > umbral:
            new_image.append(255)
        else:
            new_image.append(0) 
        x+=1
        if x >= ancho:
            x=0
            y+=1
    
    sol = PIL.Image.new("L", (ancho, alto))
    sol.putdata(new_image)
    return sol

def binarizacion_entorno(imagen, entorno):
    ancho, alto = imagen.size
    if imagen.mode != 'L':
        imagen = imagen.convert("L")
    imagen = np.array(imagen)
    new_image = np.zeros_like(imagen,dtype=np.uint8)
    
    for y in range(alto):
        for x in range(ancho):
            #Asigana los valores dependiendo de la cantidad de pixeles con los que se quiere hacer la media 
            if entorno in range(3, 16, 2): 
                y1 = y - (entorno // 2)
                y2 = y + (entorno // 2) + 1
                x1 = x - (entorno // 2)
                x2 = x + (entorno // 2) + 1
            else:
                y1 = y - 1
                y2 = y + 2
                x1 = x - 1
                x2 = x + 2
            vecinos = []
            for i in range(max(0,y1), min(alto, y2)):
                for j in range(max(0, x1), min(ancho, x2)):
                    if (i, j) != (y, x):
                        vecinos.append(imagen[i, j])

            media = sum(vecinos) / len(vecinos)
            if imagen[y, x] > media:
                new_image[y, x] = 255
            else:
                new_image[y, x] = 0

    return Image.fromarray(new_image, 'L')

if __name__ == '__main__':
    pass    
    '''
    imagen_binarizada = binarizar_por_media_entorno('mujer.jpg')
    cv2.imshow('Imagen Binarizada', imagen_binarizada)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''