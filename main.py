import PIL

import filtros
import functions as f
import utils as u
import plots_and_statistics as p
import numpy as np
import pandas as pd

import streamlit as st

# CODE FOR PAGE CONFIGURATION FRONT END 
st.set_page_config(page_title="Comparar efectos - PSM Universidad de Sevilla", layout="centered")

input_box_image = st.text_input("Imagen a comparar", value=None)
file = st.file_uploader("Sube una imagen", type=["png", "jpg"])

col_options_1,col_options_2,col_options_3,col_options_4 = st.columns(4)
bn = col_options_1.checkbox("Blanco y negro", value=False)
color_check = col_options_2.checkbox("Mascara de color", value=False)
channel_check = col_options_3.checkbox("Cambio de canal RGB", value=False)
fake_check = col_options_4.checkbox("Fake color", value=False)

image = None
if input_box_image != None and file != None:
    image = u.read_image_path(input_box_image)
elif input_box_image != None and file == None:
    image = u.read_image_path(input_box_image)
elif file != None and input_box_image == None:
    image = u.read_image_file(file)
else:
    pass


if image != None:
    
    if image.mode == 'L':
        text='Está subiendo una imagen que está en formato BLANCO y NEGRO. El formato soportado es RGB. Es posible que no tenga todas las opciones de las que dispone la aplicación. Formato de la imagen:',image.mode
        st.warning(text)
    elif image.mode != 'RGB' or image.mode == 'RGB':
        image = image.convert('RGB')
        
        st.subheader("Imagen")
        col_original_1, col_original_2 = st.columns(2)
        col_original_1.image(image,caption='Imagen original')
        col_original_2.image(p.histograma_color(image), caption='Histograma de la imagen original')
        
        if bn != False:
            with st.expander("Blanco y negro"):
                col_1, col_2 = st.columns(2)
                new_image_black_white = f.image_to_gray(imagen=image)
                histograma_bn = p.histograma_blanco_negro(new_image_black_white)
                col_1.image(new_image_black_white,caption='Imagen en blanco y negro')
                col_2.image(histograma_bn, caption='Histograma de la imagen en blanco y negro')

        if color_check != False:
            with st.expander("Mascara de color"):
                col_1, col_2, col_3 = st.columns(3)
                color = col_1.color_picker(label = 'Color de la mascara', value=None)
                new_image_colored = f.image_to_hex_color(image, color)
                histograma_color_mascara = p.histograma_color(new_image_colored)
                col_2.image(new_image_colored,caption='Imagen con mascara del color seleccionado')
                col_3.image(histograma_color_mascara, caption='Histograma de la imagen con mascara')

        if channel_check != False:
            with st.expander("Canales RGB"):
                col_1, col_2, col_3 = st.columns(3)
                channel = col_1.radio("Canal RGB", ["Red","Green","Blue"])
                new_image_channel = f.image_to_one_channel(imagen=image,channel=channel)
                histograma_color_channel = p.histograma_color(new_image_channel)
                col_2.image(new_image_channel,caption='Canal seleccionado de la imagen original')
                col_3.image(histograma_color_channel, caption='Histograma de la imagen con solo un canal')

        if fake_check != False:
            with st.expander("Fake color"):
                col_1, col_2 = st.columns(2)
                x = np.linspace(0, 256, 256)
                tecnica = st.radio("Transformacion de la grafica para entrar en 0 y 1", ["Clipping","Normalizar"])
                string_red = st.text_input("Funcion RED",value='1-0.0039*x')
                st.write('Puede probar tambien con funciones mas complejas, por ejemplo: 0.5*cos(0.1*x-150)+0.5')
                string_green = st.text_input("Funcion GREEN", value='0.0039*x')
                st.write('Puede probar tambien con funciones mas complejas, por ejemplo: 0.5*sin(0.1*x-1)+0.5')
                string_blue = st.text_input("Funcion BLUE", value='0.5')
                st.write('Puede probar tambien con funciones mas complejas, por ejemplo: x/256 - floor(x/256)')
                
                if string_red != '' and string_green != '' and string_blue != '':
                    
                    red = u.string2func(string_red)
                    green = u.string2func(string_green)
                    blue = u.string2func(string_blue)
                    
                    if tecnica == 'Clipping':
                        y_red=u.encuadre(red(x))
                        y_green=u.encuadre(green(x))
                        y_blue=u.encuadre(blue(x))
                    else:
                        y_red=u.normalizacion(red(x))
                        y_green=u.normalizacion(green(x))
                        y_blue=u.normalizacion(blue(x))
                
                    chart_data = pd.DataFrame(
                        {
                            "x": x,
                            "Red": y_red,
                            "Green": y_green,
                            "Blue": y_blue,
                        }
                    )
                    col_2.line_chart(chart_data, x="x", y=["Red", "Blue", "Green"], color=["#0000ff","#00ff00","#ff0000"])
                    new_image_fake_color = p.image_bn_to_fake_color(image,y_red,y_green,y_blue)
                    col_1.image(new_image_fake_color, caption='Imagen en Fake Color de la imagen en Blanco y Negro')
        
        if bn != False:
            with st.expander("Filtros pasa alta y baja"):
                
                col_s_1, col_s_2, col_s_3, col_s_4 = st.columns(4)
                col_t_1, col_t_2, col_t_3, col_t_4 = st.columns(4)
                col_r_1, col_r_2 = st.columns(2)
                
                tam = st.slider("Tamaño de la imagen de la imagen resultante", 512, 1000,step=2)
                slider1 = col_s_1.slider("Sigma pasa de baja ideal", 0, 100)
                f_pasa_baja_ideal = filtros.filtro_pasa_baja_ideal(new_image_black_white,tam,slider1)
                slider2 = col_s_2.slider("Sigma pasa de baja no ideal", 0.0, 1.0,value=0.01)
                f_pasa_baja_no_ideal = filtros.filtro_pasa_baja_no_ideal(new_image_black_white,tam,slider2)
                slider3 = col_s_3.slider("Sigma pasa de alta ideal", 0, 100)
                f_pasa_alta_ideal = filtros.filtro_pasa_alta_ideal(new_image_black_white,tam,slider3)
                slider4 = col_s_4.slider("Sigma pasa de alta no ideal", 0.0, 1.0,value=0.01)
                f_pasa_alta_no_ideal = filtros.filtro_pasa_alta_no_ideal(new_image_black_white,tam,slider4)
                
                #SHOW THE PLOTS
                col_t_1.image(f_pasa_baja_ideal, caption='Filtro pasa de baja ideal')
                col_t_2.image(f_pasa_baja_no_ideal, caption='Filtro pasa de baja no ideal')
                col_t_3.image(f_pasa_alta_ideal, caption='Filtro pasa de alta ideal')
                col_t_4.image(f_pasa_alta_no_ideal, caption='Filtro pasa de alta no ideal')
                
                f_suma = f.image_plus_image(new_image_black_white,f_pasa_alta_no_ideal)
                col_r_1.image(new_image_black_white.resize((tam,tam)), caption='Imagen original en blanco y negro')
                col_r_2.image(f_suma, caption='Sharpening (Imagen original + Filtro pasa alta no ideal)')
                
        if bn != False:
            with st.expander("Binarizacion"):
                col_b_1, col_b_2 = st.columns(2)
                col_b_3, col_b_4 = st.columns(2)
                
                umbral = col_b_1.slider("Umbral", 0, 255,step=1)
                f_binarizacion_umbral = p.binarizacion_por_umbral(new_image_black_white, umbral)
                col_b_2.image(f_binarizacion_umbral, caption='Binarizacion con umbral de {}'.format(umbral))
                
                tam = col_b_3.slider("Numero de vecinos para los que realizar la media", 3, 15,step=2)
                f_binarizacion_entorno = p.binarizacion_entorno(new_image_black_white,tam)
                texto = 'Binarizacion por entorno: Media de vecinos {}x{}'.format(tam, tam)
                col_b_4.image(f_binarizacion_entorno, caption=texto)
                
                
                
        
    else:
        text='Está subiendo una imagen que está en formato no soportado. Los formatos soportados son RGB y Blanco y Negro (L). Vuelva a subir otra imagen con los formatos soportados. Formato de la imagen',image.mode
        st.warning(text)
else:
    pass