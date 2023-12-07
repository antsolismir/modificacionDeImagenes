import PIL

import filtros
import functions as f
import utils as u
import plots_and_statistics as p

import streamlit as st

# CODE FOR PAGE CONFIGURATION FRONT END 
st.set_page_config(page_title="Comparar efectos - PSM Universidad de Sevilla", layout="centered")

input_box_image = st.text_input("Imagen a comparar")
file = st.file_uploader("Sube una imagen", type=["png", "jpg"])

image = None
if input_box_image != '' and file != None:
    image = u.read_image_path(input_box_image)
elif input_box_image != '' and file == None:
    image = u.read_image_path(input_box_image)
elif file != None and input_box_image == '':
    image = u.read_image_file(file)
else:
    pass


if image != None:
    
    if image.mode == 'L':
        text='Está subiendo una imagen que está en formato BLANCO y NEGRO. El formato soportado es RGB. Es posible que no tenga todas las opciones de las que dispone la aplicación. Formato de la imagen:',image.mode
        st.warning(text)
    elif image.mode != 'RGB' or image.mode == 'RGB':
        image = image.convert('RGB')
        tab1, tab2 = st.tabs(["Colores", "Transformaciones"])
        tab1.write("Tratamiento de color de la imagen")
        tab2.write("Tratamiento de pixels de la imagen")
        with tab1.expander("Filtros de color"):
        #OPTIONS OF THE IMAGE#
            col_options_1, col_options_2 = st.columns(2)
            color = col_options_1.color_picker(label = 'Cambia el color de la imagen:')
            channel = col_options_2.radio("Elige un canal", ["Red","Green","Blue"])

            #SHOW THE IMAGE
            col_image_1, col_image_2, col_image_3, col_image_4, col_image_5 = st.columns(5)
            col_image_1.image(image,caption='Imagen original')
            
            new_image_black_white = f.image_to_gray(imagen=image)
            col_image_2.image(new_image_black_white,caption='Imagen en blanco y negro')
                
            if color != None:
                new_image_colored = f.image_to_hex_color(image, color)
                col_image_3.image(new_image_colored,caption='Imagen con mascara del color seleccionado')

            if channel != None:
                new_image_channel = f.image_to_one_channel(imagen=image,channel=channel)
                col_image_4.image(new_image_channel,caption='Canal seleccionado de la imagen original')
            
            new_image_fake_color, plot_fake_color = p.image_bn_to_fake_color(image)
            col_image_5.image(new_image_fake_color, caption='Imagen en Fake Color de la imagen en Blanco y Negro')
            
        with tab1.expander("Datos y estadisticas de color"):
            
            col_plots_1, col_plots_2, col_plots_3 = st.columns(3)
            col_plots_4, col_plots_5 = st.columns(2)
            
            histograma_imagen_original = p.histograma_color(image)
            histograma_bn = p.histograma_blanco_negro(new_image_black_white)
            histograma_color_mascara = p.histograma_color(new_image_colored)
            histograma_color_channel = p.histograma_color(new_image_channel)
            histograma_fake_color = plot_fake_color
            
            #SHOW THE PLOTS
            col_plots_1.image(histograma_imagen_original, caption='Histograma de la imagen original')
            col_plots_2.image(histograma_bn, caption='Histograma de la imagen en blanco y negro')
            col_plots_3.image(histograma_color_mascara, caption='Histograma de la imagen con mascara')
            col_plots_4.image(histograma_color_channel, caption='Histograma de la imagen con solo un canal')
            col_plots_5.image(histograma_fake_color, caption='Histograma de la imagen en fake color')
            
        with tab2.expander("Filtros pasa alta y baja"):
            
            col_s_1, col_s_2, col_s_3, col_s_4 = st.columns(4)
            col_t_1, col_t_2, col_t_3, col_t_4 = st.columns(4)
            
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
            st.image(new_image_black_white.resize((tam,tam)), caption='Imagen original en blanco y negro')
            st.image(f_suma, caption='Sharpening (Imagen original + Filtro pasa alta no ideal)')

        #binarizacion,grafica = p.varianza_minima(new_image_black_white)
        #st.image(binarizacion)
        #st.image(grafica)
    else:
        text='Está subiendo una imagen que está en formato no soportado. Los formatos soportados son RGB y Blanco y Negro (L). Vuelva a subir otra imagen con los formatos soportados. Formato de la imagen',image.mode
        st.warning(text)
else:
    pass