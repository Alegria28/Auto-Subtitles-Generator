# cspell:disable

# Información sobre los módulos: https://shorturl.at/slHUh

# Importamos los módulos
import tkinter  # Para trabajar con UI
import vlc  # Para reproducir el video

# Del modulo tkinter, importamos la clase
from tkinter import filedialog
from tkinter import colorchooser

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

ANCHOVENTANA = 1200
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

    # ---- Ventana principal ----

    # Creamos nuestra ventana
    root = tkinter.Tk()
    # Le cambiamos el nombre a nuestra ventana
    root.title("Generador de subtítulos automáticos")
    # LLamamos a la función para centrar nuestra ventana
    centrarPantalla(root=root)

    # ---- Estructura de la interfaz ----

    # Frame para los controles (derecha)
    controls_frame = tkinter.Frame(root, width=300, bg="lightgrey")
    controls_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    controls_frame.pack_propagate(False)  # Para que no cambie de tamaño el frame

    # Frame para el video (izquierda)
    video_frame = tkinter.Frame(root, background="black")
    video_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    # ---- Lógica VLC ----

    # Creamos una instancia de VLC y del reproductor
    instance = vlc.Instance(
        "--avcodec-hw=none --quiet"
    )  # Desactivamos la aceleracion por hardware para evitar errores de "deadlock"
    reproductor = instance.media_player_new()

    # Variables de control
    isSliderActive = False

    # ---- Funciones de control del reproductor ----
    def pausar():
        reproductor.pause()

    def cambiarVolumen(volumen):
        reproductor.audio_set_volume(int(volumen))

    def setPosition(posicion):
        if reproductor.get_media():
            pos = int(posicion) / 1000.0
            reproductor.set_position(pos)
            # Si no se está reproduciendo, le damos a play
            if not reproductor.is_playing():
                reproductor.play()
                # Aseguramos que el botón muestre "Pausa"
                pause_button.config(text="Pausa")

    def actualizar_slider():
        if not isSliderActive:
            is_playing = reproductor.is_playing()
            pause_button.config(text="Reproducir" if not is_playing else "Pausa")

            if is_playing:
                posicion_actual = reproductor.get_position()
                if posicion_actual > 0.99:
                    # Cuando el video termina, lo reinicia llamando a setPosition(0)
                    setPosition(0)
                else:
                    position_slider.set(int(posicion_actual * 1000))

        root.after(200, actualizar_slider)

    def on_slider_press(event):
        global isSliderActive
        isSliderActive = True

    def on_slider_release(event):
        global isSliderActive
        isSliderActive = False
        setPosition(position_slider.get())

    def elegirColor():
        codigoColor = colorchooser.askcolor(title="Elige un color")

        if codigoColor:
            colorVariable.set(codigoColor[1])
            color_display.config(bg=codigoColor[1])

    def generate_subtitles():
        print("--- GENERANDO SUBTÍTULOS CON LAS SIGUIENTES OPCIONES ---")
        print(f"Fuente: {fontVariable.get()}")
        print(f"Tamaño: {sizeVariable.get()}")
        print(f"Color: {colorVariable.get()}")
        print(f"Posición: {positionVariable.get()}")

        # -------- Lógica para procesamiento de subtítulos -----------

    # --- Widgets de control ---

    playback_lf = tkinter.LabelFrame(
        controls_frame, text="Reproducción", padx=10, pady=10, bg="lightgrey"
    )
    playback_lf.pack(pady=10, padx=10, fill=tkinter.X)

    pause_button = tkinter.Button(playback_lf, text="Pausa", command=pausar)
    pause_button.pack(fill=tkinter.X)

    position_slider = tkinter.Scale(
        playback_lf,
        from_=0,
        to=1000,
        orient=tkinter.HORIZONTAL,
        showvalue=0,
        bg="lightgrey",
        highlightthickness=0,
    )
    position_slider.pack(fill=tkinter.X, pady=(5, 0))
    position_slider.bind("<ButtonPress-1>", on_slider_press)
    position_slider.bind("<ButtonRelease-1>", on_slider_release)

    volume_slider = tkinter.Scale(
        playback_lf,
        from_=0,
        to=100,
        orient=tkinter.HORIZONTAL,
        command=cambiarVolumen,
        bg="lightgrey",
        highlightthickness=0,
        label="Volumen",
    )
    volume_slider.set(50)
    volume_slider.pack(fill=tkinter.X, pady=(5, 0))

    # --- Variables y widgets de subtitulos

    fontVariable = tkinter.StringVar(root, "Arial")
    sizeVariable = tkinter.IntVar(root, 30)
    positionVariable = tkinter.StringVar(root, "Abajo")
    colorVariable = tkinter.StringVar(root, "#FFFFFF")

    # Sección de opciones de subtítulos
    subs_lf = tkinter.LabelFrame(
        controls_frame, text="Opciones de Subtítulos", padx=10, pady=10, bg="lightgrey"
    )
    subs_lf.pack(pady=10, padx=10, fill=tkinter.X)

    # Fuente
    tkinter.Label(subs_lf, text="Fuente:", bg="lightgrey").pack(anchor="w")
    fonts = ["Arial", "Courier New", "Times New Roman", "Verdana"]
    font_menu = tkinter.OptionMenu(subs_lf, fontVariable, *fonts)
    font_menu.pack(fill=tkinter.X)

    # Tamaño
    tkinter.Label(subs_lf, text="Tamaño:", bg="lightgrey").pack(
        anchor="w", pady=(10, 0)
    )
    size_spinbox = tkinter.Spinbox(subs_lf, from_=10, to=100, textvariable=sizeVariable)
    size_spinbox.pack(fill=tkinter.X)

    # Color
    tkinter.Label(subs_lf, text="Color:", bg="lightgrey").pack(anchor="w", pady=(10, 0))
    color_frame = tkinter.Frame(subs_lf, bg="lightgrey")
    color_frame.pack(fill=tkinter.X)
    color_button = tkinter.Button(color_frame, text="Seleccionar", command=elegirColor)
    color_button.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X, padx=(0, 5))
    color_display = tkinter.Label(
        color_frame, bg=colorVariable.get(), width=4, relief="sunken"
    )
    color_display.pack(side=tkinter.RIGHT)

    # Posición
    tkinter.Label(subs_lf, text="Posición:", bg="lightgrey").pack(
        anchor="w", pady=(10, 0)
    )
    positions = ["Abajo", "Medio", "Arriba"]
    for pos in positions:
        rb = tkinter.Radiobutton(
            subs_lf,
            text=pos,
            variable=positionVariable,
            value=pos,
            bg="lightgrey",
            activebackground="lightgrey",
        )
        rb.pack(anchor="w")

    # Botón de Generar
    generate_button = tkinter.Button(
        controls_frame,
        text="Generar Subtítulos",
        command=generate_subtitles,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
    )
    generate_button.pack(side=tkinter.BOTTOM, fill=tkinter.X, padx=10, pady=10)

    # ---- Procesamiento archivos ----

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

    # ---- Reproducción ----

    def reproducirVideo():
        # Identificamos que sistema de gestión de ventanas se esta usando

        # Para Linux
        if sys.platform.startswith("linux"):
            reproductor.set_xwindow(video_frame.winfo_id())
        # Para windows
        elif sys.platform.startswith("win32"):
            reproductor.set_hwnd(video_frame.winfo_id())

        # Reproducimos el video (se escucha con audio gracias a que utiliza vlc)
        reproductor.play()
        pause_button.config(text="Pausa")

        # Actualizamos nuestra variable y llamamos a nuestra funcion
        global isPlaying
        isPlaying = True
        actualizar_slider()

    # Para asegurarnos que la ventana este lista antes de reproducir, le mandamos el objeto de
    # reproducirVideo para que este pueda ejecutarlo mas tarde (1ms mas tarde) cuando se inicie el main loop
    root.after(1, reproducirVideo)

    # Iniciamos el loop principal de la ventana
    root.mainloop()

    # ---- Limpieza ----
    # Borramos el .mp3 creado
    os.remove(nombreAudio)
    reproductor.stop()
