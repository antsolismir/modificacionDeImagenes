import PIL
import numpy as np
import cv2

def filtro_pasa_baja_ideal(imagen, tam, d0):
    imagen = np.array(imagen)
    # Calcular la transformada de Fourier 2D de la imagen de entrada
    f_transformada = np.fft.fft2(imagen)
    # Centrar la transformada de Fourier
    f_transformada_centro = np.fft.fftshift(f_transformada)

    # Crear un filtro paso bajo ideal
    filas, columnas = imagen.shape
    centro_fila, centro_columna = filas // 2, columnas // 2
    mascara = np.zeros((filas, columnas))
    for i in range(filas):
        for j in range(columnas):
            distancia = np.sqrt((i - centro_fila)**2 + (j - centro_columna)**2)
            if distancia <= d0:
                mascara[i, j] = 1

    # Aplicar el filtro multiplicándolo con la transformada de Fourier centrada
    f_transformada_filtrada = f_transformada_centro * mascara

    # Calcular la inversa de la transformada de Fourier para obtener la imagen filtrada
    imagen_filtrada = np.fft.ifft2(np.fft.ifftshift(f_transformada_filtrada)).real

    #tam = int(tam/2)
    sol = PIL.Image.fromarray(imagen_filtrada)
    return sol.convert('L').resize((tam,tam))

def filtro_pasa_alta_ideal(imagen, tam, d0):
    imagen = np.array(imagen.convert('L'))
    # Calcular la transformada de Fourier 2D de la imagen de entrada
    f_transformada = np.fft.fft2(imagen)
    # Centrar la transformada de Fourier
    f_transformada_centro = np.fft.fftshift(f_transformada)

    # Crear un filtro paso bajo ideal
    filas, columnas = imagen.shape
    centro_fila, centro_columna = filas // 2, columnas // 2
    mascara = np.zeros((filas, columnas))
    for i in range(filas):
        for j in range(columnas):
            distancia = np.sqrt((i - centro_fila)**2 + (j - centro_columna)**2)
            if distancia <= d0:
                mascara[i, j] = 1

    # Aplicar el filtro multiplicándolo con la transformada de Fourier centrada
    f_transformada_filtrada = f_transformada_centro * (1-mascara)

    # Calcular la inversa de la transformada de Fourier para obtener la imagen filtrada
    imagen_filtrada = np.fft.ifft2(np.fft.ifftshift(f_transformada_filtrada)).real

    sol = PIL.Image.fromarray(imagen_filtrada)
    return sol.convert('L').resize((tam,tam))

def filtro(imagen, tam, sigma):
    imagen = np.array(imagen)
    tam1 = int(tam/2)
    # Creamos un filtro pasa bajas gaussiano de dimensiones 512x512
    F1=np.arange(-tam1,tam1,1)
    F2=np.arange(-tam1,tam1,1)
    [X,Y]=np.meshgrid(F1,F2)
    R=np.sqrt(X**2+Y**2)
    R=R/np.max(R)
    sigma = sigma
    # Redimensionamos la imagen a 512x512
    image = cv2.resize(imagen,(tam,tam))
    # Establecemos el tipo de dato de intensidad como float
    gray_f=np.float64(image)
    # Calculamos la transformada discreta de fourier 2D
    Fimg=np.fft.fft2(gray_f)
    # Movemos el origen al centro de la imagen (bajas frecuencias) (es el espectro)
    Fsh_Image=np.fft.fftshift(Fimg)
    # Filtro pasa bajas con función gaussiana
    fPB = np.exp(-(R**2)/(2*sigma**2))
    fPA = 1-np.exp(-(R**2)/(2*sigma**2))
    return Fsh_Image, fPB, fPA

def filtro_pasa_baja_no_ideal(imagen, tam, sigma):
    imagen = np.array(imagen)
    espectro, fPB, _= filtro(imagen, tam, sigma)
    # Aplicamos el filtro gaussiano al espectro de la imagen (Imagen x Máscara)
    FFt_filtered_PB=espectro*fPB
    # Recuperamos la imagen calculando la transformada inversa de fourier del espectro ya filtrado
    ImageFiltered_PB = np.fft.ifft2(np.fft.ifftshift(FFt_filtered_PB))
    # Normalizamos las imagenes para mostrarlas en pantalla
    ImageFilteredN_PB = cv2.normalize(abs(ImageFiltered_PB), None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)
    #Lo tranformamos en imagen
    filtradaPB = PIL.Image.fromarray(ImageFilteredN_PB)
    return filtradaPB

def filtro_pasa_alta_no_ideal(imagen,tam,sigma):
    imagen = np.array(imagen)
    espectro, _, fPA = filtro(imagen, tam, sigma)
    # Aplicamos el filtro gaussiano al espectro de la imagen (Imagen x Máscara)
    FFt_filtered_PA=espectro*fPA
    # Recuperamos la imagen calculando la transformada inversa de fourier del espectro ya filtrado
    ImageFiltered_PA = np.fft.ifft2(np.fft.ifftshift(FFt_filtered_PA))
    # Normalizamos las imagenes para mostrarlas en pantalla
    ImageFilteredN_PA = cv2.normalize(abs(ImageFiltered_PA), None, alpha = 0, beta = 255, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_8U)
    #Lo tranformamos en imagen
    filtradaPA = PIL.Image.fromarray(ImageFilteredN_PA)
    return filtradaPA
