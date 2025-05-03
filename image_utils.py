
"""
Funciones utilitarias para el procesamiento de imágenes y manejo de archivos de texto/csv.
Incluye utilidades para recortar, oscurecer imágenes, crear carpetas y manipular textos.
"""

import csv
from PIL import Image, ImageEnhance
import os


def split_string(string, max_chars_per_line):
    """
    Divide un string en varias líneas para que ninguna supere el máximo de caracteres indicado.
    Intenta equilibrar el número de palabras por línea.
    Args:
        string (str): Texto a dividir.
        max_chars_per_line (int): Máximo de caracteres por línea.
    Returns:
        str: Texto dividido en líneas.
    """
    words = string.split()
    lines = []
    current_line = ""
    for word in words:
        if len(current_line + " " + word) > max_chars_per_line:
            lines.append(current_line.strip())
            current_line = ""
        current_line += " " + word
    if current_line:
        lines.append(current_line.strip())

    num_lines = len(lines)
    if num_lines > 1:
        total_words = len(words)
        ideal_words_per_line = (total_words + num_lines - 1) // num_lines
        excess_words = total_words - ideal_words_per_line * (num_lines - 1)

        even_lines = []
        i = 0
        while i < num_lines - 1:
            line_words = words[:ideal_words_per_line]
            if excess_words > 0:
                line_words.append(words[ideal_words_per_line])
                excess_words -= 1
                words.pop(ideal_words_per_line)
            even_lines.append(" ".join(line_words))
            words = words[ideal_words_per_line:]
            i += 1
        even_lines.append(" ".join(words))
        return "\n".join(even_lines)
    else:
        return lines[0]


def darken_images(images_folder, output_folder):
    """
    Oscurece todas las imágenes de una carpeta y guarda el resultado en otra carpeta.
    Args:
        images_folder (str): Carpeta de imágenes originales.
        output_folder (str): Carpeta de salida para imágenes oscurecidas.
    """
    dark = 0.5

    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):

            filepath = os.path.join(images_folder, filename)
            img = Image.open(filepath)


            enhancer = ImageEnhance.Brightness(img)


            dark_img = enhancer.enhance(dark)


            dark_img.save(f"{output_folder}/{filename}")


def cut_images_old(images_folder, output_folder):
    """
    Recorta imágenes al tamaño 1080x1350 centrando el recorte.
    Args:
        images_folder (str): Carpeta de imágenes originales.
        output_folder (str): Carpeta de salida para imágenes recortadas.
    """

    target_size = (1080, 1350)

    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):

            filepath = os.path.join(images_folder, filename)
            img = Image.open(filepath)
            resize_ration = min(target_size[0] / img.width, target_size[1] / img.height)


            width, height = img.size


            left = (width - target_size[0]) // 2
            top = (height - target_size[1]) // 2
            right = left + target_size[0]
            bottom = top + target_size[1]


            img = img.crop((left, top, right, bottom))


            img.save(f"{output_folder}/{filename}")


def cut_images(images_folder, output_folder):
    """
    Recorta imágenes para que tengan la proporción 1080x1350 y luego las redimensiona si es necesario.
    Args:
        images_folder (str): Carpeta de imágenes originales.
        output_folder (str): Carpeta de salida para imágenes recortadas.
    """

    desired_ratio = 1080 / 1350


    for filename in os.listdir(images_folder):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):

            img = Image.open(os.path.join(images_folder, filename))


            width, height = img.size
            ratio = width / height


            if ratio > desired_ratio:

                new_width = round(height * desired_ratio)
                new_height = height
            else:

                new_width = width
                new_height = round(width / desired_ratio)


            left = (width - new_width) / 2
            top = (height - new_height) / 2
            right = left + new_width
            bottom = top + new_height
            img = img.crop((left, top, right, bottom))


            if img.size != (1080, 1350):
                img = img.resize((1080, 1350))


            img.save(os.path.join(output_folder, filename))


def create_new_topic_dirs(topic, project_dir):
    """
    Crea la estructura de carpetas necesaria para un nuevo tema.
    Args:
        topic (str): Nombre del tema.
        project_dir (str): Ruta base del proyecto.
    """

    if not os.path.exists(f"{project_dir}/customers/{topic}"):
        os.makedirs(f"{project_dir}/customers/{topic}")

    if not os.path.exists(f"{project_dir}/sources/images/{topic}"):
        os.makedirs(f"{project_dir}/sources/images/{topic}")
        os.makedirs(f"{project_dir}/sources/images/{topic}/cropped")
        os.makedirs(f"{project_dir}/sources/images/{topic}/cropped/darken")


def fix_text_syntax(font: str, text_file):
    """
    Corrige caracteres problemáticos en el archivo de texto según la fuente seleccionada.
    Args:
        font (str): Ruta de la fuente.
        text_file (str): Ruta del archivo de texto a corregir.
    """
    with open(text_file, 'r', encoding="utf-8") as file:
        lines = file.readlines()


    if font.__contains__("Bebas"):

        file = open(text_file, "r")
        replaced_content = ""


        for line in file:

            line = line.strip()


            new_line = line.replace("’", "'").replace("’", "'")


            replaced_content = replaced_content + new_line + "\n"


        file.close()


        write_file = open(text_file, "w")


        write_file.write(replaced_content)


        write_file.close()

def add_sheets(file_names: str, output_path: str, customer_name: str, authors: str, quotes: str):
    """
    Crea un archivo CSV con los nombres de archivo, autores y frases generadas.
    Args:
        file_names (list): Lista de nombres de archivo.
        output_path (str): Carpeta donde se guarda el CSV.
        customer_name (str): Nombre del cliente (nombre del archivo CSV).
        authors (list): Lista de autores.
        quotes (list): Lista de frases.
    """
    with open(f'{output_path}/{customer_name}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Reference", "Verse"])
        for i in range(len(file_names)):
            writer.writerow([file_names[i], authors[i], quotes[i]])