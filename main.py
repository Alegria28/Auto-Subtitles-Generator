# Información sobre los módulos: https://shorturl.at/slHUh

# Importamos los módulos
import tkinter  # Para trabajar con UI
import vlc  # Para reproducir el video

# Del modulo tkinter, importamos la clase
from tkinter import filedialog

# Del modulo moviepy en el sub-modulo editor, importamos la clase
from moviepy.editor import VideoFileClip

# Módulos de la biblioteca estándar
import sys  # Para poder salir del programa
import os  # Para trabajar con rutas
import shutil  # Para copiar archivos

# Constantes
NOMBRE_CARPETA = "carpetaCompartida"
NOMBRE_TXT_VIDEO = "pathVideo.txt"
NOMBRE_TXT_AUDIO = "pathAudio.txt"

PATH_ACTUAL = os.getcwd()  # Directorio actual de trabajo
PATH_CARPETA_COMPARTIDA = os.path.join(PATH_ACTUAL, "carpetaCompartida")
PATH_TXT_VIDEO = os.path.join(PATH_ACTUAL, "pathVideo.txt")
PATH_TXT_AUDIO = os.path.join(PATH_CARPETA_COMPARTIDA, "pathAudio.txt")

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

    os.system("clear")

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
            name=NOMBRE_CARPETA, exist_ok=True
        )  # En caso de que ya exista, se ignora el error

        # Copiamos el video a la carpeta compartida
        shutil.copy(src=pathVideoHost, dst=PATH_CARPETA_COMPARTIDA)

        # Dentro de la carpeta compartida escribimos en un .txt la ruta del video, ya que sera leído por el contenedor
        with open(file=os.path.join(NOMBRE_CARPETA, NOMBRE_TXT_VIDEO), mode="w") as f:
            f.write(os.path.join(NOMBRE_CARPETA, os.path.basename(pathVideoHost)))

    else:
        # Se cierra la aplicación si no se pudo encontrar el video
        sys.exit("⚠️ No se pudo obtener el nombre del video")

    # Creamos nuestra ventana
    root = tkinter.Tk()
    # Le cambiamos el nombre a nuestra ventana
    root.title("Dashboard")
    # LLamamos a la función para centrar nuestra ventana
    centrarPantalla(root=root)

    # Creamos un frame a partir de la ventana para que este nos sirva como
    # salida de video
    frame = tkinter.Frame(root, background="black")
    frame.pack(fill=tkinter.BOTH, expand=1)

    # Creamos una instancia de VLC y del reproductor
    instance = vlc.Instance()
    reproductor = instance.media_player_new()

    # Obtenemos el nombre del video
    nombre_base = os.path.basename(p=pathVideoHost)
    # Obtenemos una tupla separando el nombre y la extension, el nombre se queda en nombre_sin_extension y
    # la extension en _
    nombre_sin_extension, _ = os.path.splitext(p=nombre_base)
    # Al nombre del video, le agregamos la extension correspondiente
    nombreAudio = nombre_sin_extension + ".mp3"

    # Cargamos el video utilizando el constructor de la clase
    video = VideoFileClip(filename=pathVideoHost, audio=True)

    # Cargamos el video para el reproductor
    videoReproductor = instance.media_new(pathVideoHost)
    # Le cargamos el video al reproductor
    reproductor.set_media(videoReproductor)

    # Extraemos el audio
    audio = video.audio
    # Creamos el audio
    audio.write_audiofile(os.path.basename(nombreAudio), codec="mp3")

    # Creamos la ruta en donde esta el audio que acabamos de crear
    pathAudioCreado = os.path.join(PATH_ACTUAL, nombreAudio)

    # Copiamos el audio a la carpeta compartida
    shutil.copy(src=pathAudioCreado, dst=PATH_CARPETA_COMPARTIDA)

    # Dentro de la carpeta compartida escribimos en un .txt la ruta del audio, ya que sera leído por el contenedor
    with open(file=os.path.join(NOMBRE_CARPETA, NOMBRE_TXT_AUDIO), mode="w") as f:
        f.write(os.path.join(NOMBRE_CARPETA, os.path.basename(pathAudioCreado)))

    def reproducirVideo():
        # Identificamos que sistema de gestión de ventanas se esta usando

        # Para Linux
        if sys.platform.startswith("linux"):
            reproductor.set_xwindow(frame.winfo_id())
        # Para windows
        elif sys.platform.startswith("win32"):
            reproductor.set_hwnd(frame.winfo_id())

        # Reproducimos el video (se escucha con audio gracias a que utiliza vlc)
        reproductor.play()

    # Para asegurarnos que la ventana este lista antes de reproducir, le mandamos el objeto de 
    # reproducirVideo para que este pueda ejecutarlo mas tarde (1ms mas tarde) cuando se inicie el main loop
    root.after(1, reproducirVideo)

    # Iniciamos el loop principal de la ventana
    root.mainloop()

    # Borramos el .mp3 creado
    os.remove(nombreAudio)
