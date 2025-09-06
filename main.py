# cspell: disable

# Modulo de OpenAi para la transcripcion del video
import whisper

# Modulo para poder trabajar con GUI (graphical user interface)
import tkinter
from tkinter import filedialog

# Modulo para extraer audio del video
import moviepy

# Para poder trabajar con video
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# Para poder terminar el programa
import sys

# Para borrar el archivo de audio
import os

# Para poder crear los TextClip sin tener el problema de ImageMagick
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Constante
NOMBREAUDIO = "audioExtraido.mp3"
FONT = 20


def crearTextClip(palabra, duracion, color):

    # Cargamos una fuente basica
    try:
        font = ImageFont.truetype("Ubuntu-M.ttf", FONT)
    except Exception as e:
        print(
            "La fuenta especificada no fue encontrada, se usara la fuente por defecto"
        )
        font = ImageFont.load_default()

    # Crea un objeto de dibujo para medir el texto
    draw_temp = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    

    bbox = draw_temp.textbbox((0, 0), palabra, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Crea la imagen final con el tamaño correcto y un pequeño margen
    img = Image.new('RGBA', (text_width + 10, text_height + 10), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), palabra, font=font, fill=color)
    
    # Convierte la imagen de Pillow a un array de numpy y crea un ImageClip
    np_image = np.array(img)
    clip = ImageClip(np_image).set_duration(duracion)
    
    return clip


# Punto de entrada al proyecto (dado que este programa se corre directamente y no es importado como modulo)
if __name__ == "__main__":

    # Al iniciar el programa abrimos el explorador de archivos para obtener el nombre del video con que trabajar
    pathVideo = filedialog.askopenfilename(
        title="Selecciona el video",
        # Tipo de archivos de video soportados
        filetypes=[("Video files", "*.mp4"), ("Video files", "*.mov")],
    )

    # Verificamos si se obtuvo el nombre del video
    if pathVideo:
        print("El nombre del video es: " + pathVideo)
    else:
        sys.exit("No se pudo obtener el nombre del video")

    # Cargamos el video
    video = VideoFileClip(pathVideo)
    # Le sacamos el audio
    audio = video.audio

    # Creamos el audio
    audio.write_audiofile(NOMBREAUDIO, codec="mp3")

    # Especificamos el modelo de Whisper
    model = whisper.load_model("large-v3")

    print("Generando transcripcion")

    # Obtenemos la transcripcion
    resultado = model.transcribe(
        "audioExtraido.mp3", word_timestamps=True
    )  # Tiempo para cada palabra

    print("Transcripcion terminada")

    # Borramos el audio creado ya que ya no sera utilizado
    os.remove(NOMBREAUDIO)

    # Lista que va a guardar los clip de textos del subtitulo
    subtitulos = []

    # Mostramos la information
    for segment in resultado["segments"]:
        if "words" in segment:
            for word in segment["words"]:
                print(
                    f"Word: \"{word['word']}\" (Start: {word['start']:.2f}s, End: {word['end']:.2f}s)"
                )

                # Obtenemos la informacion sobre la palabra
                palabra = word["word"]
                inicio = word["start"]
                fin = word["end"]
                duracion = fin - inicio

                # Creamos el clip de texto a partir de la informacion
                clipTexto = crearTextClip(
                    palabra,
                    duracion,
                    "white"
                )

                # Establecemos la posicion, inicio y duracion del clip
                clipTexto = clipTexto.set_position("bottom")
                clipTexto = clipTexto.set_start(inicio)

                # Agregamos este clip a nuestra lista
                subtitulos.append(clipTexto)

    # Superponemos los clips de texto sobre el video
    videoFinal = CompositeVideoClip([video] + subtitulos)

    # Creamos el video
    videoFinal.write_videofile("video-con-subtitulos.mp4", codec="libx264")
