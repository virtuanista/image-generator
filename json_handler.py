
"""
Funciones para manejar archivos JSON y convertir archivos de texto a JSON.
Permite leer datos estructurados y convertir archivos de texto a formato JSON para su uso en el proyecto.
"""

import json
import os


def get_data(json_file):
    """
    Lee un archivo JSON y retorna los versos y referencias.
    Args:
        json_file (str): Ruta del archivo JSON.
    Returns:
        tuple: (verses, refs) donde ambos son listas o strings según el JSON.
    """
    with open(f'{json_file}', 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
    verses: str = jsonData['verses']
    refs: str = jsonData['references']
    return verses, refs


def txt_to_json(text_file, output_folder):
    """
    Convierte un archivo de texto a formato JSON y lo guarda en la carpeta de salida.
    (Función incompleta: actualmente solo intenta leer el archivo como JSON)
    Args:
        text_file (str): Ruta del archivo de texto.
        output_folder (str): Carpeta donde guardar el JSON generado.
    """
    with open(f'{text_file}', 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
