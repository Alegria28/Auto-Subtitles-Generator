# Modulo de OpenAi para la transcripcion del video
import whisper

# Modulo para poder trabajar con video
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

# Para borrar el archivo de audio
import os

# Librería pillow para el manejo y procesamiento de imágenes, se utiliza en lugar de
# ImageMagick para mayor facilidad
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Para ver si hay una GPU disponible
import torch

# Para utilizar el sleep
import time

# ------ Constantes ------
NOMBREAUDIO = "audioExtraido.mp3"
FONTSIZE = 20
NOMBREARCHIVO = "carpetaCompartida/pathVideo.txt"
CARPETACOMPARTIDA = "carpetaCompartida"
VIDEOSALIDA = os.path.join(CARPETACOMPARTIDA, "videoConSubtitulos.mp4")


def crearTextClip(palabra, duracion, color):

    # Cargamos una fuente con tamaño en especifico
    try:
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", FONTSIZE
        )
    # En caso de que esta no se haya podido cargar
    except Exception as e:
        print(
            "La fuente especificada no fue encontrada, se usara la fuente por defecto "
            + str(e)
        )
        font = ImageFont.load_default()

    # Creamos una imagen 1px x 1px solamente para después ver cuanto espacio ocupa en realidad el texto, RGB
    # es simplemente el modo de color
    imagenTemporal = ImageDraw.Draw(Image.new("RGBA", (1, 1)))

    # textbbox() calcula el tamaño que ocuparía el texto si este se dibujara. Este regresa una tupla de 4
    # números representando las coordenadas (x0, y0, x1, y1) de la caja invisible que rodea a la palabra.
    # El (0,0) es la coordenada de anclaje o el punto hipotético donde se empezaría a dibujar el texto
    cajaTemporal = imagenTemporal.textbbox((0, 0), palabra, font)
    # Calculamos el ancho
    textAncho = cajaTemporal[2] - cajaTemporal[0]
    # Calculamos la altura
    textAltura = cajaTemporal[3] - cajaTemporal[1]

    # Crea la imagen final con el tamaño correcto y un pequeño margen (10), ademas de no tener ningún color de
    # fondo (0,0,0,0)
    img = Image.new("RGBA", (textAncho + 10, textAltura + 10), (0, 0, 0, 0))
    # Hacemos un dibujo a partir de la imagen, de esta manera podemos dibujar sobre la imagen
    draw = ImageDraw.Draw(img)
    # A esa imagen por medio del draw le agregamos el texto con esa posición dentro de la imagen creada
    draw.text((5, 5), palabra, font, color)

    # Hacemos la conversion para poder usar la imagen de la librería Pillow y moviepy, dado que ambos conocen
    # los array de numpy, asi que una imagen se puede representar como un array de numpy
    imagenArray = np.array(img)
    # A partir de este array hacemos un ImageClip a quien después le especificamos la duración que va a tener
    clip = ImageClip(imagenArray).set_duration(duracion)

    # Regresamos el TextClip
    return clip


if __name__ == "__main__":

    # Leemos la ruta en donde se encuentra el video a partir del .txt
    with open(NOMBREARCHIVO, "r") as f:
        pathVideo = f.read().strip()

    # Cargamos el video
    video = VideoFileClip(pathVideo)
    # Le sacamos el audio
    audio = video.audio

    # Creamos el audio
    audio.write_audiofile(NOMBREAUDIO, codec="mp3")

    # Especificamos el modelo de Whisper
    model = whisper.load_model("large-v3")

    # Verificamos si se está usando GPU o CPU
    if torch.cuda.is_available():
        print("✅ GPU detectada: Esta se utilizara para el procesamiento")
    else:
        print("⚠️ No se detectó GPU: Esta utilizara el CPU en su lugar")

    # Mostramos mensaje y después esperamos antes de realizar la transcripcion
    print(" Generando transcripcion")
    time.sleep(3)

    # Obtenemos la transcripcion
    resultado = model.transcribe(
        "audioExtraido.mp3", word_timestamps=True  # Tiempo para cada palabra
    )

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

                # Obtenemos la information sobre la palabra
                palabra = word["word"]
                inicio = word["start"]
                fin = word["end"]
                duracion = fin - inicio

                # Creamos el clip de texto a partir de la informacion 
                clipTexto = crearTextClip(palabra, duracion, (255, 255, 255)) # Color blanco

                # Establecemos la posición, inicio y duración del clip
                clipTexto = clipTexto.set_position("bottom")
                clipTexto = clipTexto.set_start(inicio)

                # Agregamos este clip a nuestra lista
                subtitulos.append(clipTexto)

    # Superponemos los clips de texto sobre el video
    videoFinal = CompositeVideoClip([video] + subtitulos)

    # Creamos el video, especificando la ruta de la carpeta compartida
    videoFinal.write_videofile(VIDEOSALIDA, codec="libx264")
