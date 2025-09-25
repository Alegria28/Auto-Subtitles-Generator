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
SHARED_FOLDER_PATH = "/autoSubtitlesGenerator/sharedFolder"
JSON_NAME = "videoFeatures.json"

# Diccionario para mapear posiciones de GUI a valores de moviepy
POSITIONS = {"Bottom": "bottom", "Middle": "center", "Top": "top"}
# Diccionario para mapear los modelos de AI
AI_MODELS = {
    "Tiny": "tiny",
    "Base": "base",
    "Small": "small",
    "Medium": "medium",
    "Large": "large",
    "Turbo": "turbo",
}


# Diccionario para mapear nombres de fuentes a archivos .ttf
FONTS = {
    "Arial": "arial.ttf",
    "Arial Black": "ariblk.ttf",
    "Arial Bold": "arialbd.ttf",
    "Arial Italic": "ariali.ttf",
    "Arial Bold Italic": "arialbi.ttf",
    "Comic Sans MS": "comic.ttf",
    "Comic Sans MS Bold": "comicbd.ttf",
    "Courier New": "cour.ttf",
    "Courier New Bold": "courbd.ttf",
    "Courier New Italic": "couri.ttf",
    "Courier New Bold Italic": "courbi.ttf",
    "Georgia": "georgia.ttf",
    "Georgia Bold": "georgiab.ttf",
    "Georgia Italic": "georgiai.ttf",
    "Georgia Bold Italic": "georgiaz.ttf",
    "Impact": "impact.ttf",
    "Times New Roman": "times.ttf",
    "Times New Roman Bold": "timesbd.ttf",
    "Times New Roman Italic": "timesi.ttf",
    "Times New Roman Bold Italic": "timesbi.ttf",
    "Trebuchet MS": "trebuc.ttf",
    "Trebuchet MS Bold": "trebucbd.ttf",
    "Trebuchet MS Italic": "trebucit.ttf",
    "Trebuchet MS Bold Italic": "trebucbi.ttf",
    "Verdana": "verdana.ttf",
    "Verdana Bold": "verdanab.ttf",
    "Verdana Italic": "verdanai.ttf",
    "Verdana Bold Italic": "verdanaz.ttf",
    "Webdings": "webdings.ttf",
}


def convert_rgb(hex_color):
    # Quitamos el # del string
    hex_color = hex_color.lstrip("#")

    # Extraemos cada componente r, g, b de la cadena pasándolo a decimal, le decimos que ese numero estaba en hexadecimal
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    # Lo regresamos como tupla
    return (r, g, b)


def create_text_clip(word, duration, color, font_size, font_name):

    # Cargamos una fuente con tamaño en especifico
    try:
        # Obtenemos la llave de la fuente segun el nombre que nos llego
        font_file = FONTS.get(font_name)
        # Cargamos la fuente
        font = ImageFont.truetype(font_file, font_size)
    # En caso de que esta no se haya podido cargar
    except Exception as e:
        print(
            "The specified font was not found, the default font will be used " + str(e)
        )
        font = ImageFont.load_default()

    # Obtenemos el ancho y alto del texto, getbbox nos da (left, top, right, bottom) del texto
    _, top, right, bottom = font.getbbox(word)
    # Guardamos el ancho
    text_width = right
    # Guardamos la altura real
    text_height = bottom - top

    # Aumentamos el margen para evitar cortes, especialmente en vertical
    horizontal_margin = 20
    vertical_margin = 20

    # Crea la imagen final con el tamaño correcto y un margen más generoso
    img = Image.new(
        "RGBA",
        (text_width + horizontal_margin, text_height + vertical_margin),
        (0, 0, 0, 0),
    )
    # Hacemos un dibujo a partir de la imagen
    draw = ImageDraw.Draw(img)

    # Dibujamos el texto, ajustando la posición para centrarlo dentro del nuevo margen
    # La posición Y es (margen_vertical / 2) - top para compensar las letras que empiezan por encima de la línea base
    draw.text(
        xy=(horizontal_margin / 2, (vertical_margin / 2) - top),
        text=word,
        font=font,
        fill=color,
    )

    # Hacemos la conversion para poder usar la imagen de la librería Pillow y moviepy, dado que ambos conocen
    # los array de numpy, asi que una imagen se puede representar como un array de numpy
    image_array = numpy.array(img)
    # A partir de este array hacemos un ImageClip a quien después le especificamos la duración que va a tener
    clip = ImageClip(image_array).set_duration(duration)

    # Regresamos el TextClip
    return clip


# Entrada principal al programa
if __name__ == "__main__":

    # --- Lectura de Json ---

    # Leemos el archivo JSON para obtener las características del video
    with open(os.path.join(SHARED_FOLDER_PATH, JSON_NAME), "r") as f:
        features_json = json.load(f)

    # Obtenemos los valores con los que vamos a trabajar
    font_size = features_json["size"]  # El tamaño lo trabajamos asi
    font_position = POSITIONS[
        features_json["position"]
    ]  # Hacemos la conversion necesaria para poder utilizar el valor correcto
    font_color = convert_rgb(features_json["color"])
    # Obtenemos el nombre de la fuente
    font_name = features_json["font"]
    ai_model = AI_MODELS[features_json["ai_model"]]
    video_path_in_folder = features_json["video_path"]
    audio_path_in_folder = features_json["audio_path"]
    video_name, video_extension = features_json["video_name"]

    # --- Procesamiento ---

    # Creamos la ruta del video, juntando el nombre de la carpeta compartida y el nombre del video
    video_path = os.path.join(
        SHARED_FOLDER_PATH, os.path.basename(video_path_in_folder)
    )

    print("🎥 Loading video")

    # Cargamos el video
    video = VideoFileClip(video_path)

    print("🧠 Downloading and/or loading AI model")

    # Especificamos el modelo de Whisper
    # model = whisper.load_model("large-v3")
    model = whisper.load_model(ai_model)

    # Mostramos mensaje y después esperamos antes de realizar la transcripción
    print("📝 Generating transcription")

    # Obtenemos la transcripción, utilizando el audio que esta en la carpeta compartida
    result = model.transcribe(
        audio_path_in_folder,
        word_timestamps=True,  # Tiempo para cada palabra
    )

    print("📝 Generating text clips")

    # Lista que va a guardar los clip de textos del subtitulo
    subtitles = []

    # Mostramos la information
    for segment in result["segments"]:
        if "words" in segment:
            for word_data in segment["words"]:
                print(
                    f"Word: \"{word_data['word']}\" (Start: {word_data['start']:.2f}s, End: {word_data['end']:.2f}s)"
                )

                # Obtenemos la information sobre la palabra
                word = word_data[
                    "word"
                ].strip()  # Quitamos los espacios en blanco de la palabra
                start = word_data["start"]
                end = word_data["end"]
                duration = end - start

                # Creamos el clip de texto a partir de la información
                text_clip = create_text_clip(
                    word=word,
                    duration=duration,
                    color=font_color,
                    font_size=font_size,
                    font_name=font_name,
                )

                # Establecemos la posición, inicio y duración del clip
                text_clip = text_clip.set_position(font_position)
                text_clip = text_clip.set_start(start)

                # Agregamos este clip a nuestra lista
                subtitles.append(text_clip)

    # Superponemos los clips de texto sobre el video
    final_video = CompositeVideoClip([video] + subtitles)

    # We use the original video name adding "-subtitled" just before the file extension
    output_video_path = os.path.join(SHARED_FOLDER_PATH, video_name + "-subtitled" + video_extension)

    # Creamos el video, especificando la ruta de la carpeta compartida
    final_video.write_videofile(output_video_path, codec="libx264")

    print("🎥 Video generated")
