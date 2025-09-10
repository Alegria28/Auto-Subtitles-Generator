# Información sobre los módulos: https://shorturl.at/slHUh

# Importamos los módulos
import tkinter # Para trabajar con UI
import tkvideoaudio # Para poder reproducir el sonido del video
import pygame # Sirve como motor de audio para el modulo pygame

# Del modulo tkinter, importamos la clase
from tkinter import filedialog
# Del modulo moviepy en el sub-modulo editor, importamos la clase
from moviepy.editor import VideoFileClip

# Módulos de la biblioteca estándar
import sys # Para poder salir del programa
import os # Para trabajar con rutas
import shutil # Para copiar archivos

# Constantes
NOMBRECARPETA = "carpetaCompartida"
NOMBREARCHIVO = os.path.join(NOMBRECARPETA, "pathVideo.txt")
ANCHOVENTANA = 1000
ALTURAVENTANA = 900


def centrarPantalla(root):

    # Obtenemos el ancho y altura de la pantalla
    anchoPantalla = root.winfo_screenwidth()
    alturaPantalla = root.winfo_screenheight()

    # Calculamos la posición para la ventana
    x = (anchoPantalla - ANCHOVENTANA) // 2  # Valor redondeado
    y = (alturaPantalla - ALTURAVENTANA) // 2

    # Establecemos la posición de la ventana
    root.geometry(f"{ANCHOVENTANA}x{ALTURAVENTANA}+{x}+{y}")


# Punto de entrada al proyecto (dado que este programa se corre directamente y no es importado como modulo)
if __name__ == "__main__":

    # Al iniciar el programa abrimos el explorador de archivos para obtener el nombre del video con que trabajar
    # (filedialog es un sub-modulo de tkinter)
    pathVideoHost = filedialog.askopenfilename(
        title="Selecciona el video",
        # Tipo de archivos de video soportados
        filetypes=[("Video files", "*.mp4"), ("Video files", "*.mov")],
    )

    # Verificamos si se obtuvo el nombre del video
    if pathVideoHost:
        print(f"📂 La ruta del video en el host es: {pathVideoHost}\n")

        # Se crea la carpeta compartida entre el host y el contenedor si este no existe
        os.makedirs(
            name=NOMBRECARPETA, exist_ok=True
        )  # En caso de que ya exista, se ignora el error

        # Creamos la ruta relativa para esta carpeta NOMBRECARPETA/pathVideo (solo nombre del video, el basename)
        pathCarpetaCompartidaConVideo = os.path.join(
            NOMBRECARPETA, os.path.basename(pathVideoHost)
        )
        print(f"📂 Ruta creada para video: {pathCarpetaCompartidaConVideo}\n")

        # Copiamos el video a la carpeta compartida
        shutil.copy(src=pathVideoHost, dst=pathCarpetaCompartidaConVideo)

        print(f"📂 Ruta creada para .txt: {NOMBREARCHIVO}\n")

        # Creamos un archivo .txt (cuya ruta esta en la carpeta compartida) donde escribimos la ruta que creamos para la carpeta compartida
        with open(file=NOMBREARCHIVO, mode="w") as f:
            f.write(pathCarpetaCompartidaConVideo)

    else:
        sys.exit("⚠️ No se pudo obtener el nombre del video")

    # Creamos nuestra ventana
    root = tkinter.Tk()

    # Le cambiamos el nombre a nuestra ventana
    root.title("Dashboard")

    # LLamamos a la función para centrar nuestra ventana
    centrarPantalla(root=root)

    """Label widget which can display text and bitmaps."""
    label = tkinter.Label(root)

    """Geometry manager Pack.
    Base class to use the methods pack_* in every widget."""
    label.pack()

    # Declaramos nuestro reproductor (accedemos a la clase tkvideo del modulo)
    reproductor = tkvideoaudio.tkvideo(
        path=pathVideoHost, label=label, size=(640, 360)
    )

    # Obtenemos el nombre del video
    nombre_base = os.path.basename(p=pathVideoHost)
    # Obtenemos una tupla separando el nombre y la extension, el nombre se queda en nombre_sin_extension y
    # la extension en _
    nombre_sin_extension, _ = os.path.splitext(p=nombre_base)
    # Al nombre del video, le agregamos la extension correspondiente
    nombreAudio = nombre_sin_extension + ".mp3"
    print(f"🔊 Nombre del audio generado: {nombreAudio}\n")

    # Cargamos el video utilizando el constructor de la clase
    video = VideoFileClip(filename=pathVideoHost, audio=True)

    # Extraemos el audio
    audio = video.audio
    # Creamos el audio
    audio.write_audiofile(os.path.basename(nombreAudio), codec="mp3")

    # Reproducimos el video (se escucha con audio gracias a que utiliza pygame)
    reproductor.play()

    # Iniciamos el loop principal de la ventana
    root.mainloop()

    # Limpiamos módulos de pygame que se iniciaron 
    pygame.quit()
