
"""
Módulo para la generación de imágenes motivacionales.
Contiene funciones para crear directorios de salida y generar imágenes con frases, autores y logotipo.
"""

import os
import random
import re
import textwrap
import time
from string import ascii_letters

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

import image_utils as helper
import json_handler


def create_dirs(output_folder, customer_name):
    """
    Crea el directorio de salida para el cliente si no existe.
    Args:
        output_folder (str): Ruta base de salida.
        customer_name (str): Nombre del cliente.
    Returns:
        str: Ruta completa del directorio creado.
    """
    output_path = f"{output_folder}/{customer_name}"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    return output_path


def create_posts(images_folder, text_file, quote_font, author_font, output_folder, customer_name, number_of_posts, logo_file: str = None, show_author : bool = False):
    """
    Genera imágenes con frases motivacionales y opcionalmente el autor y logo.
    Args:
        images_folder (str): Carpeta con las imágenes de fondo.
        text_file (str): Archivo de texto con las frases.
        quote_font (str): Ruta de la fuente para la frase.
        author_font (str): Ruta de la fuente para el autor.
        output_folder (str): Carpeta de salida.
        customer_name (str): Nombre del cliente.
        number_of_posts (int): Número de posts a generar (-1 para todos).
        logo_file (str, opcional): Ruta del logo a insertar.
        show_author (bool): Si se muestra el autor.
    """
    with open(text_file, 'r', encoding='utf-8') as file:
        quotes = file.readlines()

    if number_of_posts == -1:
        number_of_posts = len(quotes) - 1

    run_time_average = 0
    if number_of_posts > 1:
        start_time_total = time.time()

    image_num = list()
    image_files = [f"{images_folder}/{file}" for file in os.listdir(images_folder) if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg")]
    random_for_image = random.randint(0, len(image_files) - 1)
    for i in range(number_of_posts):
        image_num.append((random_for_image + i) % len(image_files))
    random.shuffle(image_num)

    # Columnas para hoja de cálculo
    spreadsheet_col1 = list()
    spreadsheet_col2 = list()
    spreadsheet_col3 = list()

    output_path = create_dirs(output_folder, customer_name)

    for i in range(number_of_posts):
        start_time = time.time()
        print(f"Creando Post #{i}")

        author_text = ""
        quote_text = ""
        text = quotes[i]
        quote = text.split(":::")
        quote_text = quote[0]
        if show_author and quote_text != text:
            author_text = quote[1]
            if author_text.rstrip(" ") == "":
                author_text = None

        random_image_num = image_num[0]
        del image_num[0]
        image_file = image_files[random_image_num]

        image_license = image_file.split('/')
        image_license = image_license[len(image_license)-1]
        image_license = image_license.split('-')
        image_license = image_license[len(image_license)-1].rstrip(".jpg")

        file_name = f"/{i}-{image_license}.jpg"
        create_post(image_file=image_file, quote_text=quote_text,
                         quote_font=quote_font, author_font=author_font, output_path=output_path, file_name=file_name,
                         logo_file=logo_file, customer_name=customer_name, author_text=author_text)

        spreadsheet_col1.append(file_name.strip("/"))
        spreadsheet_col2.append(author_text)
        spreadsheet_col3.append(quote_text)

        end_time = time.time()
        run_time = end_time - start_time
        run_time_average += run_time
        print(f"\033[0;34m LISTO #{i}, Tiempo de ejecución:", round(run_time, 2), "segundos! \033[0m", output_path)

    helper.add_sheets(file_names=spreadsheet_col1, output_path=output_path, customer_name=customer_name,
                      authors=spreadsheet_col2, quotes=spreadsheet_col3)

    if number_of_posts > 1:
        run_time_average /= number_of_posts
        end_time_total = time.time()
        run_time_total = end_time_total - start_time_total
        print(f"\n\033[0;32m¡Listo! Se generaron {number_of_posts} posts para {customer_name}!"
              f"\nTiempo total:", round(run_time_total, 2), "segundos = ", round(run_time_total / 60, 2), " minutos!",
              f"\nTiempo promedio:", round(run_time_average, 2), "segundos!\033[0m")


def create_post(image_file, quote_text, quote_font, author_font, output_path, file_name, logo_file, customer_name, author_text: str = None):
    """
    Genera una imagen con la frase, autor y logo (opcional).
    Args:
        image_file (str): Ruta de la imagen de fondo.
        quote_text (str): Frase a mostrar.
        quote_font (str): Ruta de la fuente para la frase.
        author_font (str): Ruta de la fuente para el autor.
        output_path (str): Carpeta de salida.
        file_name (str): Nombre del archivo de salida.
        logo_file (str, opcional): Ruta del logo.
        customer_name (str): Nombre del cliente.
        author_text (str, opcional): Autor de la frase.
    Returns:
        str: Ruta del archivo generado.
    """
    img = Image.open(image_file)
    quote_font = ImageFont.truetype(font=f'{quote_font}', size=75)
    draw = ImageDraw.Draw(im=img)
    max_char_count = 25
    new_text = textwrap.fill(text=quote_text, width=max_char_count)
    new_text = new_text.replace(" ", "  ")
    x_logo = 0
    y_logo = 1100
    x_text = img.size[0] / 2
    y_text = img.size[1] / 2
    position = (x_text, y_text)
    shadow_color = (0, 0, 0, 128)
    shadow_position = (x_text+5, y_text+5)
    draw.text(shadow_position, new_text, font=quote_font, fill=shadow_color, anchor='mm', align='center')
    draw.text(position, text=new_text, font=quote_font, fill=(255, 255, 255, 255), anchor='mm', align='center')
    if author_text is not None:
        author_font = ImageFont.truetype(font=f'{author_font}', size=45)
        num_of_lines = new_text.count("\n") + 1
        line_height = 55
        text_height = line_height * num_of_lines + 40
        author_position = (position[0], position[1] + text_height)
        draw.text(author_position, text=author_text, font=author_font, fill=(255, 255, 255, 255), anchor='mm', align='center')
    if logo_file is not None:
        img_logo = Image.open(logo_file)
        alpha = 1
        enhancer = ImageEnhance.Brightness(img_logo)
        img_logo_darken = enhancer.enhance(alpha)
        img_with_logo = Image.new('RGBA', img.size, (0, 0, 0, 0))
        img_with_logo.paste(img, (0, 0))
        img_with_logo.paste(img_logo_darken, (int(x_logo), int(y_logo)), mask=img_logo_darken)
        img_with_logo_rgb = img_with_logo.convert("RGB")
        img_with_logo_rgb.save(f"{output_path}/{file_name}")
        return f"{output_path}/{file_name}"
    img.save(f"{output_path}/{file_name}")
    return f"{output_path}/{file_name}"

