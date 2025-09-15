# cspell: disable

# Importamos los módulos
import whisper

# Del modulo editor de moviepy importamos las clases
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# Del modulo pillow importamos los módulos
from PIL import Image, ImageDraw, ImageFont

# Módulos biblioteca estándar
import numpy
import os
import json

# ------ Constantes ------
NOMBRE_CARPETA_COMPARTIDA = "/autoSubtitlesGenerator/carpetaCompartida"
NOMBRE_TXT_VIDEO = "pathVideo.txt"
NOMBRE_TXT_AUDIO = "pathAudio.txt"
NOMBRE_JSON = "caracteristicasVideo.json"

PATH_VIDEO_SALIDA = os.path.join(NOMBRE_CARPETA_COMPARTIDA, "videoConSubtitulos.mp4")

# Diccionario para mapear posiciones de GUI a valores de moviepy
POSICIONES = {"Abajo": "bottom", "Medio": "center", "Arriba": "top"}


def convertirRGB(colorHexadecimal):
    # Quitamos el # del string
    colorHexadecimal = colorHexadecimal.lstrip("#")

    # Extraemos cada componente r, g, b de la cadena pasándolo a decimal, le decimos que ese numero estaba en hexadecimal
    r = int(colorHexadecimal[0:2], 16)
    g = int(colorHexadecimal[2:4], 16)
    b = int(colorHexadecimal[4:6], 16)

    # Lo regresamos como tupla
    return (r, g, b)


def crearTextClip(palabra, duracion, color, tamanoFuente):

    # Cargamos una fuente con tamaño en especifico
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", tamanoFuente
        )
    # En caso de que esta no se haya podido cargar
    except Exception as e:
        print(
            "La fuente especificada no fue encontrada, se usara la fuente por defecto "
            + str(e)
        )
        font = ImageFont.load_default()

    # Obtenemos el ancho y alto del texto, getbbox nos da (left, top, right, bottom) del texto
    _, top, right, bottom = font.getbbox(palabra)
    # Guardamos el ancho
    textAncho = right
    # Guardamos la altura real
    textAltura = bottom - top

    # Aumentamos el margen para evitar cortes, especialmente en vertical
    margenHorizontal = 20
    margenVertical = 20

    # Crea la imagen final con el tamaño correcto y un margen más generoso
    img = Image.new(
        "RGBA",
        (textAncho + margenHorizontal, textAltura + margenVertical),
        (0, 0, 0, 0),
    )
    # Hacemos un dibujo a partir de la imagen
    draw = ImageDraw.Draw(img)

    # Dibujamos el texto, ajustando la posición para centrarlo dentro del nuevo margen
    # La posición Y es (margen_vertical / 2) - top para compensar las letras que empiezan por encima de la línea base
    draw.text(
        xy=(margenHorizontal / 2, (margenVertical / 2) - top),
        text=palabra,
        font=font,
        fill=color,
    )

    # Hacemos la conversion para poder usar la imagen de la librería Pillow y moviepy, dado que ambos conocen
    # los array de numpy, asi que una imagen se puede representar como un array de numpy
    imagenArray = numpy.array(img)
    # A partir de este array hacemos un ImageClip a quien después le especificamos la duración que va a tener
    clip = ImageClip(imagenArray).set_duration(duracion)

    # Regresamos el TextClip
    return clip


# Entrada principal al programa
if __name__ == "__main__":

    # --- Lectura de archivos ---

    # Leemos el archivo .txt de la carpeta compartida para obtener el nombre del video
    with open(os.path.join(NOMBRE_CARPETA_COMPARTIDA, NOMBRE_TXT_VIDEO), "r") as f:
        pathVideoEnCarpeta = f.read().strip()

    # Leemos el archivo .txt de la carpeta compartida para obtener el nombre del video
    with open(os.path.join(NOMBRE_CARPETA_COMPARTIDA, NOMBRE_TXT_AUDIO), "r") as f:
        pathAudioEnCarpeta = f.read().strip()

    # Leemos el archivo JSON para obtener las características del video
    with open(os.path.join(NOMBRE_CARPETA_COMPARTIDA, NOMBRE_JSON), "r") as f:
        caracteristicasVideo = json.load(f)

    # Obtenemos los valores con los que vamos a trabajar
    tamanoFuente = caracteristicasVideo["size"]  # El tamaño lo trabajamos asi
    posicionFuente = POSICIONES[
        caracteristicasVideo["position"]
    ]  # Hacemos la conversion necesaria para poder utilizar el valor correcto
    colorFuente = convertirRGB(caracteristicasVideo["color"])

    # --- Procesamiento ---

    # Creamos la ruta del video, juntando el nombre de la carpeta compartida y el nombre del video
    pathVideo = os.path.join(
        NOMBRE_CARPETA_COMPARTIDA, os.path.basename(pathVideoEnCarpeta)
    )

    print("🎥 Cargando video")

    # Cargamos el video
    video = VideoFileClip(pathVideo)

    print("🧠 Cargando modelo IA")

    # Especificamos el modelo de Whisper
    # model = whisper.load_model("large-v3")
    model = whisper.load_model("medium")

    # Mostramos mensaje y después esperamos antes de realizar la transcripción
    print("📝 Generando transcripción")

    # Obtenemos la transcripción, utilizando el audio que esta en la carpeta compartida
    resultado = model.transcribe(
        pathAudioEnCarpeta,
        word_timestamps=True,  # Tiempo para cada palabra
    )

    print("📝 Generando text clips")

    # Lista que va a guardar los clip de textos del subtitulo
    subtitulos = []

    # Mostramos la information
    for segment in resultado["segments"]:
        if "words" in segment:
            for word in segment["words"]:
                print(
                    f"Word: \"{word['word']}\" (Start: {word['start']:.2f}s, End: {word['end']:.2f}s)"
                )

                # Obtenemos la information sobre la palabra
                palabra = word[
                    "word"
                ].strip()  # Quitamos los espacios en blanco de la palabra
                inicio = word["start"]
                fin = word["end"]
                duracion = fin - inicio

                # Creamos el clip de texto a partir de la información
                clipTexto = crearTextClip(
                    palabra=palabra,
                    duracion=duracion,
                    color=colorFuente,
                    tamanoFuente=tamanoFuente,
                )

                # Establecemos la posición, inicio y duración del clip
                clipTexto = clipTexto.set_position(posicionFuente)
                clipTexto = clipTexto.set_start(inicio)

                # Agregamos este clip a nuestra lista
                subtitulos.append(clipTexto)

    # Superponemos los clips de texto sobre el video
    videoFinal = CompositeVideoClip([video] + subtitulos)

    # Creamos el video, especificando la ruta de la carpeta compartida
    videoFinal.write_videofile(PATH_VIDEO_SALIDA, codec="libx264")

    print("🎥 Video generado")
