
"""
Script principal para la generación de imágenes motivacionales.
Configura los parámetros principales y ejecuta el proceso de creación de posts.
"""

import os
import post_handler
import image_utils as helper



# Tema de las frases (debe coincidir con el nombre del archivo en sources/text_data)
TOPIC = "quotes"
# Mostrar el autor debajo de la frase (si está disponible)
SHOW_AUTHOR = False
# Nombre del cliente (usado para la carpeta de salida y CSV)
CUSTOMER_NAME = "virtuanista"
# Número de posts a generar (-1 para todos los disponibles en el archivo de texto)
NUM_OF_POSTS = 46




# Definición de rutas principales
project_dir = os.getcwd().replace("\\", "/")
images_folder = f"{project_dir}/sources/images/{TOPIC}"
images_folder_cropped = f"{images_folder}/cropped"
images_folder_cropped_darken = f"{images_folder_cropped}/darken"
text_file = f"{project_dir}/sources/text_data/{TOPIC}.txt"
quote_font = f"{project_dir}/sources/fonts/MouldyCheeseRegular-WyMWG.ttf"
author_font = f"{project_dir}/sources/fonts/MangabeyRegular-rgqVO.otf"
output_folder = f"{project_dir}/generated/{TOPIC}"
logo_file = f"{project_dir}/sources/logo.png"



if __name__ == "__main__":
    """
    Ejecuta el proceso principal de generación de imágenes motivacionales.
    Llama a la función create_posts con los parámetros definidos arriba.
    """
    post_handler.create_posts(
        images_folder=images_folder_cropped_darken,
        text_file=text_file,
        quote_font=quote_font,
        author_font=author_font,
        output_folder=output_folder,
        logo_file=logo_file,
        customer_name=CUSTOMER_NAME,
        number_of_posts=NUM_OF_POSTS,
        show_author=SHOW_AUTHOR
    )