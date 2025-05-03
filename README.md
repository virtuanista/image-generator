# Generador de Imágenes Motivacionales

Este proyecto permite generar imágenes motivacionales de alta calidad, listas para publicar en redes sociales, a partir de frases inspiradoras y fondos personalizados. El sistema automatiza el proceso de recorte, oscurecimiento de imágenes y superposición de textos/frases, permitiendo personalizar fuentes, autores y logotipos.

## ¿Para qué sirve este proyecto?

- Crear contenido visual motivacional para Instagram, Facebook, LinkedIn, etc.
- Automatizar la generación de posts para marcas personales, empresas o clientes.
- Ahorrar tiempo en la edición manual de imágenes y textos.
- Mantener una estética profesional y coherente en todas las publicaciones.

## Características principales

- Recorte automático de imágenes a formato vertical (1080x1350 px).
- Oscurecimiento de imágenes para mejorar la legibilidad del texto.
- Inserción de frases motivacionales y autores (opcional).
- Personalización de fuentes y logotipo.
- Generación de archivos CSV con el detalle de cada imagen creada.
- Estructura modular y fácil de adaptar a nuevos temas o clientes.

## Estructura del proyecto

```
image_utils.py           # Funciones utilitarias para imágenes y textos
json_handler.py          # Utilidades para manejo de JSON
main.py                  # Script principal de ejecución
post_handler.py          # Lógica de generación de imágenes
sources/
  images/                # Imágenes originales por tema
  fonts/                 # Fuentes tipográficas
  logo.png               # Logotipo opcional
  text_data/             # Archivos de frases motivacionales
/generated/              # Imágenes generadas y CSVs
```

## Requisitos

- Python 3.7+
- Pillow (PIL)

Instala las dependencias con:

```bash
pip install pillow
```

## Paso a paso para generar tus imágenes

1. **Prepara tus frases**

   - Crea un archivo de texto en `sources/text_data/` con tus frases motivacionales, una por línea. Puedes añadir el autor separando con `:::` (ejemplo: `La vida es bella ::: Autor`).
2. **Prepara tus imágenes**

   - Coloca tus imágenes en `sources/images/{tema}` (por ejemplo, `sources/images/quotes`).
3. **Crea las carpetas necesarias**

   - Ejecuta en el script principal:
     ```python
     import image_utils as helper
     helper.create_new_topic_dirs("quotes", project_dir)
     ```
   - Esto creará las carpetas para imágenes recortadas y oscurecidas.
4. **Recorta y oscurece las imágenes**

   - Recorta las imágenes:
     ```python
     helper.cut_images("sources/images/quotes", "sources/images/quotes/cropped")
     ```
   - Oscurece las imágenes recortadas:
     ```python
     helper.darken_images("sources/images/quotes/cropped", "sources/images/quotes/cropped/darken")
     ```
5. **Configura el archivo `main.py`**

   - Ajusta los parámetros principales:
     - `TOPIC`: nombre del tema (debe coincidir con el archivo de frases y carpeta de imágenes)
     - `SHOW_AUTHOR`: `True` para mostrar el autor, `False` para ocultarlo
     - `CUSTOMER_NAME`: nombre del cliente o marca
     - `NUM_OF_POSTS`: cuántas imágenes generar (-1 para todas)
     - Rutas de fuentes y logo si quieres personalizar
6. **Ejecuta el generador**

   - Simplemente ejecuta:
     ```bash
     python main.py
     ```
   - Las imágenes generadas aparecerán en `generated/{TOPIC}/{CUSTOMER_NAME}/` junto con un archivo CSV con el detalle de cada post.

## Personalización avanzada

- Puedes cambiar las fuentes en la carpeta `sources/fonts/` y ajustar las rutas en `main.py`.
- El logotipo se superpone en la parte inferior de la imagen si lo configuras.
- Puedes crear nuevos temas repitiendo el proceso para diferentes archivos de frases e imágenes.

## Ejemplos de frases en el archivo de texto

```
La vida es como una bicicleta, para mantener el equilibrio debes seguir adelante. ::: Albert Einstein

Cree en ti mismo y todo será posible.
```

## Licencia

<p align="center">
	Repositorio generado por <a href="https://github.com/sabiopobre" target="_blank">virtu 🎣</a>
</p>

<p align="center">
	<img src="https://open.soniditos.com/cat_footer.svg" />
</p>

<p align="center">
	Copyright © 2025
</p>

<p align="center">
	<a href="/LICENSE"><img src="https://img.shields.io/static/v1.svg?style=for-the-badge&label=License&message=MIT&logoColor=d9e0ee&colorA=363a4f&colorB=b7bdf8"/></a>
</p>
