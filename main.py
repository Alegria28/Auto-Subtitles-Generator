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
import json  # Para trabajar con archivos JSON
import subprocess  # Para ejecutar comandos en terminal

# ------ Constantes ------
FOLDER_NAME = "sharedFolder"
VIDEO_TXT_NAME = "pathVideo.txt"
AUDIO_TXT_NAME = "pathAudio.txt"
JSON_NAME = "videoFeatures.json"

# Obtenemos la ruta absoluta de la carpeta donde está este archivo (main.py).
# - __file__ es el nombre del archivo actual (puede ser una ruta relativa o absoluta, según cómo se ejecute el script).
# - os.path.dirname(__file__) obtiene solo la carpeta que contiene este archivo, quitando el nombre del archivo.
# - os.path.abspath(...) convierte esa ruta (relativa o absoluta) en una ruta absoluta.
# Así, PATH_BASE siempre apunta a la carpeta raíz de tu proyecto, sin importar desde dónde ejecutes el script.
BASE_PATH = os.path.abspath(os.path.dirname(__file__))
SHARED_FOLDER_PATH = os.path.join(BASE_PATH, "sharedFolder")
CACHE_PATH = os.path.join(BASE_PATH, ".cache")

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 900


def center_screen(root):
    # Obtenemos el ancho y altura de la pantalla
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculamos la posición para la ventana
    x = (screen_width - WINDOW_WIDTH) // 2  # Valor redondeado
    y = (screen_height - WINDOW_HEIGHT) // 2

    # Establecemos la posición de la ventana
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")


# Punto de entrada al proyecto (dado que este programa se corre directamente y no es importado como modulo)
if __name__ == "__main__":

    # Limpiamos la terminal
    os.system("clear")

    # Al iniciar el programa abrimos el explorador de archivos para obtener el nombre del video con que trabajar
    # (filedialog es un sub-modulo de tkinter)
    host_video_path = filedialog.askopenfilename(
        title="Select the video",
        # Tipo de archivos de video soportados
        filetypes=[("Video files", "*.mp4"), ("Video files", "*.mov")],
    )

    # Verificamos si se obtuvo el nombre del video
    if host_video_path:
        print(f"📂 The video path on the host is: {host_video_path}\n")

        # Se crea la carpeta compartida entre el host y el contenedor si este no existe
        os.makedirs(
            name=FOLDER_NAME, exist_ok=True
        )  # En caso de que ya exista, se ignora el error

        # Copiamos el video a la carpeta compartida
        shutil.copy(src=host_video_path, dst=SHARED_FOLDER_PATH)

    else:
        # Se cierra la aplicación si no se pudo encontrar el video
        sys.exit("⚠️ Could not get the video name")

    # ------ Ventana principal ------

    # Creamos nuestra ventana
    root = tkinter.Tk()
    # Le cambiamos el nombre a nuestra ventana
    root.title("Automatic Subtitles Generator")
    # LLamamos a la función para centrar nuestra ventana
    center_screen(root=root)

    # ------ Estructura de la interfaz ------

    # Frame para los controles (derecha)
    controls_frame = tkinter.Frame(root, width=300, background="")
    controls_frame.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    controls_frame.pack_propagate(False)  # Para que no cambie de tamaño el frame

    # Frame para el video (izquierda)
    video_frame = tkinter.Frame(root, background="black")
    video_frame.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    # ------ Lógica VLC ------

    # Creamos una instancia de VLC
    instance = vlc.Instance(
        "--quiet"
    )  # Para que no se vean los errores de VLC en la terminal
    # Creamos un reproductor
    player = instance.media_player_new()

    # Variables de control
    is_slider_active = False

    # ------ Lógica VLC ------

    player.video_set_marquee_string(vlc.VideoMarqueeOption.Text, "Prueba")
    player.video_set_marquee_int(vlc.VideoMarqueeOption.Enable, 1)

    # ------ Conjunto de funciones anidadas para el manejo de widgets del programa ------

    def pause_video():
        player.pause()

    def change_volume(volume):
        player.audio_set_volume(int(volume))

    def set_position(position):
        # Si el reproductor tiene un video cargado
        if player.get_media():
            # Convertimos el valor de entrada (que esta entre 0 y 1000) a un valor entre 0 y 1
            pos = int(position) / 1000.0
            # Establecemos la posición
            player.set_position(pos)
            # Si no se está reproduciendo, le damos a play
            if not player.is_playing():
                player.play()
                # Aseguramos que el botón muestre "Pausa"
                pause_button.config(text="Pause")

    def update_slider():
        # Si el usuario no esta arrastrando el slider
        if not is_slider_active:
            # Obtenemos el estado del video, para ver si se esta reproduciendo
            is_playing = player.is_playing()
            # Si no se esta reproduciendo, entonces el botón va a decir pausa
            pause_button.config(text="Play" if not is_playing else "Pause")

            # Si se esta reproduciendo
            if is_playing:
                # Obtenemos la posición en el video (obtenemos un valor entre 0 y 1)
                current_position = player.get_position()
                # Si el video ya termino, lo reiniciamos llamando a nuestra función
                if current_position > 0.99:
                    set_position(0)
                # Si se sigue reproduciendo entonces actualizamos el slider
                else:
                    position_slider.set(int(current_position * 1000))

        # Programamos a la ventana para que se ejecute la función cada 200ms
        root.after(200, update_slider)

    def on_slider_press(event):
        # Cuando el usuario hace click en el slider, cambiamos la bandera para que la función
        # actualizarSlider no actualice el slider
        global is_slider_active  # Accedemos a la bandera anteriormente declarada ya que la queremos modificar
        is_slider_active = True

    def on_slider_release(event):
        global is_slider_active
        is_slider_active = False
        # Cambiamos la posición del video al mandarle la posición en la que se dejo el slider
        set_position(position_slider.get())

    def choose_color():
        # Abrimos una ventana para que el usuario pueda elegir un color, color_code
        # va a ser una tupla que tiene la representación RGB y hexadecimal del color
        color_code = colorchooser.askcolor(title="Choose a color")

        # Si se selecciono un color
        if color_code:
            # Obtenemos el color hexadecimal elegido
            color_variable.set(color_code[1])
            # Cambiamos el color seleccionado en GUI
            color_display.config(background=color_code[1])

    def on_select(event):
        # Obtenemos el indice del valor seleccionado
        selected_index = listbox.curselection()

        # Si hay un font seleccionado
        if selected_index:
            # Obtenemos el indice
            index = selected_index[0]
            # Guardamos el valor del indice
            font_variable.set(listbox.get(index))

    # ------ Widgets ------

    # Se crea un contenedor que dibuja un borde al rededor, el cual estará dentro del controls_frame
    playback_lf = tkinter.LabelFrame(
        controls_frame, text="Playback", padx=10, pady=10, bg="lightgrey"
    )
    # Se posiciona este LabelFrame dentro de su contenedor (controls_frame)
    playback_lf.pack(pady=10, padx=10, fill=tkinter.X)

    # Se crea un button especificándole que va a estar dentro del LabelFrame antes creado
    pause_button = tkinter.Button(playback_lf, text="Pause", command=pause_video)
    # Se posiciona dentro del contenedor (playback_lf)
    pause_button.pack(fill=tkinter.X)

    # Creamos un slider
    position_slider = tkinter.Scale(
        playback_lf,  # Especificando que va a estar dentro del LabelFrame antes creado
        from_=0,
        to=1000,
        orient=tkinter.HORIZONTAL,
        showvalue=0,  # No se va a mostrar el valor numero del slider
        bg="lightgrey",
        highlightthickness=0,
    )

    # Se posiciona dentro del contenedor
    position_slider.pack(fill=tkinter.X, pady=(5, 0))
    # Asociamos los eventos del ratón con las funciones antes creadas
    position_slider.bind("<ButtonPress-1>", on_slider_press)
    position_slider.bind("<ButtonRelease-1>", on_slider_release)

    # Creamos otro slider
    volume_slider = tkinter.Scale(
        playback_lf,
        from_=0,
        to=100,
        orient=tkinter.HORIZONTAL,
        command=change_volume,  # Le decimos que función va a ejecutar cuando el slider se utiliza
        bg="lightgrey",
        highlightthickness=0,
        label="Volume",
    )
    # Inicia el valor en 50
    volume_slider.set(50)
    # Se posiciona dentro del contenedor
    volume_slider.pack(fill=tkinter.X, pady=(5, 0))

    # --- Variables y widgets de subtítulos

    font_variable = tkinter.StringVar(root, "Arial")
    size_variable = tkinter.IntVar(root, 30)
    position_variable = tkinter.StringVar(root, "Bottom")
    color_variable = tkinter.StringVar(root, "#FFFFFF")
    ai_model = tkinter.StringVar(root, "Medium")

    # Creamos otra sección de opciones de subtítulos dentro del frame de controles
    subs_lf = tkinter.LabelFrame(
        controls_frame, text="Subtitle Options", padx=10, pady=10, bg="lightgrey"
    )
    # Lo posicionamos en el contenedor
    subs_lf.pack(pady=10, padx=10, fill=tkinter.X)

    # Fuente
    tkinter.Label(subs_lf, text="Font:", bg="lightgrey").pack(anchor="w")
    # Lista de python con las fuentes disponibles
    fonts = [
        "Arial",
        "Arial Black",
        "Arial Bold",
        "Arial Italic",
        "Arial Bold Italic",
        "Comic Sans MS",
        "Comic Sans MS Bold",
        "Courier New",
        "Courier New Bold",
        "Courier New Italic",
        "Courier New Bold Italic",
        "Georgia",
        "Georgia Bold",
        "Georgia Italic",
        "Georgia Bold Italic",
        "Impact",
        "Times New Roman",
        "Times New Roman Bold",
        "Times New Roman Italic",
        "Times New Roman Bold Italic",
        "Trebuchet MS",
        "Trebuchet MS Bold",
        "Trebuchet MS Italic",
        "Trebuchet MS Bold Italic",
        "Verdana",
        "Verdana Bold",
        "Verdana Italic",
        "Verdana Bold Italic",
        "Webdings",
    ]

    # Frame para la lista
    list_frame = tkinter.Frame(subs_lf, background="lightgrey")

    # Creamos un ListBox
    listbox = tkinter.Listbox(
        list_frame, height=10, selectmode="single"
    )  # Solo se puede seleccionar un item

    # Creamos un scrollbar
    scrollbar = tkinter.Scrollbar(
        list_frame, orient=tkinter.VERTICAL, command=listbox.yview
    )
    # Lo agregamos del lado derecho y que tome todo el espacio de Y
    scrollbar.pack(side="right", fill="y")
    # Conectamos la lista con el scroll que creamos
    listbox.config(yscrollcommand=scrollbar.set)
    # Conectamos el evento de que un elemento sea seleccionado con la funcion
    listbox.bind("<<ListboxSelect>>", on_select)
    # Ahora si empaquetamos este widget
    listbox.pack(fill="both", expand=True)

    # Agregamos las fuentes a la lista
    for font in fonts:
        listbox.insert(tkinter.END, font)

    # Buscamos en la lista el indice en el que esta nuestra variable
    selection_index = fonts.index(font_variable.get())

    # Seleccionamos en la lista lo que tiene la variable
    listbox.selection_set(selection_index)

    # Tras insertar valores ahora si empaquetamos el widget
    list_frame.pack(fill="both", expand=True)

    # Tamaño
    tkinter.Label(subs_lf, text="Size:", bg="lightgrey").pack(anchor="w", pady=(10, 0))
    # Creamos un SpinBox que es un campo de entrada de números con flechas, diciéndole que va a estar dentro
    # de la sección, con un rango de valores y vinculando el valor con la variable anteriormente creada
    size_spinbox = tkinter.Spinbox(
        subs_lf, from_=10, to=100, textvariable=size_variable
    )
    size_spinbox.pack(fill=tkinter.X)

    # Color
    tkinter.Label(subs_lf, text="Color:", bg="lightgrey").pack(anchor="w", pady=(10, 0))
    # Un pequeño frame para acomodar los widgets del color
    color_frame = tkinter.Frame(subs_lf, bg="lightgrey")
    color_frame.pack(fill=tkinter.X)
    # Se crea un botón que va a ejecutar la función antes declarada elegirColor
    color_button = tkinter.Button(color_frame, text="Select", command=choose_color)
    color_button.pack(side=tkinter.LEFT, expand=True, fill=tkinter.X, padx=(0, 5))
    # Este funcionara como un cuadro para la vista previa del color
    color_display = tkinter.Label(
        color_frame,
        bg=color_variable.get(),  # Utilizamos su color de fondo como cuadro de la vista previa
        width=4,
        relief="sunken",  # Estilo pra que parezca un recuadro
    )
    color_display.pack(side=tkinter.RIGHT)

    # Posición
    tkinter.Label(subs_lf, text="Position:", bg="lightgrey").pack(
        anchor="w", pady=(10, 0)
    )
    # Lista de python para almacenar las opciones
    positions = ["Top", "Middle", "Bottom"]
    # Recorremos la lista
    for pos in positions:
        # Se crea un radio button para cada una de las opciones
        rb = tkinter.Radiobutton(
            subs_lf,
            text=pos,  # El texto que esta en la lista
            variable=position_variable,  # Se asocia con la variable antes creada
            value=pos,
            bg="lightgrey",
            activebackground="lightgrey",
        )
        rb.pack(anchor="w")

    # Botón de Generar

    def generate_subtitles():
        print("--- GENERATING SUBTITLES WITH THE FOLLOWING OPTIONS ---")
        print(f"Font: {font_variable.get()}")
        print(f"Size: {size_variable.get()}")
        print(f"Color: {color_variable.get()}")
        print(f"Position: {position_variable.get()}")
        print(f"AI Model: {ai_model.get()}")

        # Creamos un diccionario con los valores obtenidos
        dictionary = {
            "font": font_variable.get(),
            "size": size_variable.get(),
            "color": color_variable.get(),
            "position": position_variable.get(),
            "ai_model": ai_model.get(),
            "video_path": os.path.join(FOLDER_NAME, os.path.basename(host_video_path)),
            "audio_path": os.path.join(
                FOLDER_NAME, os.path.basename(created_audio_path)
            ),
            "video_name": os.path.splitext(os.path.basename(host_video_path)),
        }

        # A partir del diccionario, lo convertimos en JSON
        json_format = json.dumps(dictionary, indent=4)  # Para que sea mas fácil leerlo

        # Dentro de la carpeta compartida escribimos el JSON, ya que sera leído por el contenedor
        with open(file=os.path.join(FOLDER_NAME, JSON_NAME), mode="w") as f:
            f.write(json_format)

        # Creamos el comando completo a ejecutar en la nueva terminal
        full_command = f"""
        echo '--- Starting subtitle generation process in Docker ---' && \\
        docker build -f Dockerfile -t auto-subtitles-generator . && \\
        docker image prune -f && \\
        echo '--- Creating container to generate subtitles ---' && \\
        docker run --rm -it \\
        -v "{SHARED_FOLDER_PATH}:/autoSubtitlesGenerator/{FOLDER_NAME}" \\
        -v "{CACHE_PATH}:/root/.cache" \\
        auto-subtitles-generator && \\
        echo '--- Process finished, the video with subtitles is in the folder: {FOLDER_NAME} ---' && \\
        echo '--- You can close this terminal ---' && \\
        exec bash
        """

        # Abrimos la nueva terminal que ejecutara los comandos, añadiendo el argumento --geometry para centrar la terminal
        subprocess.Popen(
            [
                "gnome-terminal",
                "--maximize",
                "--",
                "bash",
                "-c",
                full_command,
            ]
        )

        # Cerramos la ventana de la GUI
        root.destroy()

    generate_button = tkinter.Button(
        controls_frame,
        text="Generate Subtitles",
        command=generate_subtitles,
        bg="#4CAF50",
        fg="white",
        font=("Arial", 10, "bold"),
    )
    generate_button.pack(side=tkinter.BOTTOM, fill=tkinter.X, padx=10, pady=10)

    # Creamos una sección para los ajustes de la aplicación
    settings_lf = tkinter.LabelFrame(
        controls_frame, text="Settings", padx=10, pady=10, bg="lightgrey"
    )
    # Lo posicionamos en el contenedor
    settings_lf.pack(pady=10, padx=10, fill=tkinter.X)

    # Modelo de IA
    tkinter.Label(settings_lf, text="AI Model:", bg="lightgrey").pack(anchor="w")
    # Lista de python con los modelos disponibles
    ai_models = ["Tiny", "Base", "Small", "Medium", "Large", "Turbo"]
    # Se crea un menu dentro de la nueva sección, vinculando la variable fontVariable y desempaquetando
    # la lista al momento de pasarlo como parámetro
    ai_menu = tkinter.OptionMenu(settings_lf, ai_model, *ai_models)
    ai_menu.pack(fill=tkinter.X)

    # ------ Procesamiento archivos ------

    # Obtenemos el nombre del video
    base_name = os.path.basename(p=host_video_path)
    # Obtenemos una tupla separando el nombre y la extension, el nombre se queda en nombre_sin_extension y
    # la extension en _
    name_without_extension, _ = os.path.splitext(p=base_name)
    # Al nombre del video, le agregamos la extension correspondiente
    audio_name = name_without_extension + ".mp3"

    # Cargamos el video utilizando el constructor de la clase
    video = VideoFileClip(filename=host_video_path, audio=True)

    # Cargamos el video para el reproductor
    player_video = instance.media_new(host_video_path)
    # Le cargamos el video al reproductor
    player.set_media(player_video)

    # Extraemos el audio
    audio = video.audio
    # Creamos el audio
    audio.write_audiofile(os.path.basename(audio_name), codec="mp3")

    # Creamos la ruta en donde esta el audio que acabamos de crear
    created_audio_path = os.path.join(BASE_PATH, audio_name)

    # Copiamos el audio a la carpeta compartida
    shutil.copy(src=created_audio_path, dst=SHARED_FOLDER_PATH)

    # ------ Reproducción ------

    def play_video():
        # Identificamos que sistema de gestión de ventanas se esta usando

        # Para Linux
        if sys.platform.startswith("linux"):
            player.set_xwindow(video_frame.winfo_id())
        # Para windows
        elif sys.platform.startswith("win32"):
            player.set_hwnd(video_frame.winfo_id())

        # Reproducimos el video (se escucha con audio gracias a que utiliza vlc)
        player.play()
        pause_button.config(text="Pause")

        # Actualizamos nuestra variable y llamamos a nuestra funcion
        global is_playing
        is_playing = True
        update_slider()

    # Para asegurarnos que la ventana este lista antes de reproducir, le mandamos el objeto de
    # reproducirVideo para que este pueda ejecutarlo mas tarde (1ms mas tarde) cuando se inicie el main loop
    root.after(1, play_video)

    # Iniciamos el loop principal de la ventana
    root.mainloop()

    # ------ Limpieza ------

    # Borramos el .mp3 creado
    os.remove(audio_name)
    player.stop()
