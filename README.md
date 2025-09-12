# Generador Automático de Subtítulos

Este proyecto es una herramienta para generar subtítulos automáticamente para un archivo de video y luego incrustarlos en el mismo. Utiliza `openai-whisper` para la transcripción de audio a texto y `MoviePy` para la manipulación de video.

## Requisitos

*   **Python 3:** Para ejecutar el script de la interfaz.
*   **Docker:** Para ejecutar el contenedor de procesamiento.

### Dependencias del Sistema

Antes de ejecutar el script local (`main.py`), asegúrate de tener instaladas las siguientes herramientas en tu sistema:

*   **FFmpeg:** La librería `moviepy` lo necesita para procesar archivos de video y audio.
    *   En Debian/Ubuntu: `sudo apt-get install ffmpeg`
    *   En macOS (con Homebrew): `brew install ffmpeg`
    *   En Windows: Descárgalo desde el [sitio oficial](https://ffmpeg.org/download.html) y añade el ejecutable a tu PATH.

*   **Tkinter:** Es la librería para la interfaz gráfica. En muchas instalaciones de Python ya viene incluida, pero en algunas distribuciones de Linux podría necesitarse instalar por separado.
    *   En Debian/Ubuntu: `sudo apt-get install python3-tk`

## Configuración del Entorno Local

Para configurar el entorno y las dependencias del proyecto, se ha proporcionado un script de instalación automatizado.

### Instalación Automática (Linux/macOS)

Para usuarios de Linux y macOS, simplemente ejecuta el siguiente comando desde la raíz del proyecto. Este script creará un entorno virtual, lo activará e instalará todas las librerías necesarias.

**Importante:** Debes ejecutar el script usando el comando `source` para que el entorno virtual se active correctamente en tu terminal.

```bash
source setup.sh
```

> **¿Por qué `source`?**
> Es crucial usar `source setup.sh` (o su atajo `. setup.sh`) en lugar de `./setup.sh`. Al usar `source`, el script modifica tu sesión de terminal actual, activando el entorno virtual en ella. Si lo ejecutas como `./setup.sh`, el entorno solo se activará en un proceso temporal que se cierra al terminar el script, y no tendrá efecto en tu terminal.

Una vez ejecutado, verás que el nombre del entorno (`venv`) aparece al inicio de la línea de tu terminal, indicando que está activo y listo para usarse.

## Pasos para Generar un Video

Sigue estos pasos en orden para generar un video con subtítulos:

### 1. Construir la Imagen de Docker

Primero, necesitas construir la imagen de Docker que contiene el entorno de procesamiento. Desde la raíz del proyecto, ejecuta:

```bash
docker build -t auto-subtitles-generator .
```

*(Puedes cambiar `auto-subtitles-generator` por el nombre que prefieras)*.

### 2. Preparar el Video

A continuación, ejecuta el script de la interfaz para seleccionar tu video y preparar los archivos.

```bash
python main.py
```

Se abrirá una ventana para que selecciones el archivo de video. El script copiará el video y extraerá su audio en la carpeta `carpetaCompartida/`.

### 3. Ejecutar el Procesamiento

Una vez que el paso anterior haya finalizado, ejecuta el contenedor de Docker para que comience la generación de subtítulos. El siguiente comando "monta" la `carpetaCompartida` de tu máquina dentro del contenedor, permitiendo que el script acceda a los archivos.

```bash
docker run --rm -v "$(pwd)/carpetaCompartida:/autoSubtitlesGenerator/carpetaCompartida" auto-subtitles-generator
```

*   `--rm`: Elimina el contenedor automáticamente cuando termina el proceso.
*   `-v`: Vincula la carpeta local con la carpeta dentro del contenedor.

El proceso de transcripción puede tardar varios minutos, dependiendo de la duración del video y la potencia de tu máquina. Verás el progreso en la terminal.

### 4. Obtener el Resultado

¡Listo! Cuando el contenedor termine su ejecución, encontrarás el video final con los subtítulos incrustados en `carpetaCompartida/videoConSubtitulos.mp4`.
