# Utilizamos la ultima y mas ligera version para el contenedor (utiliza Debian)
FROM python:3.13-slim

# Se actualiza el sistema
RUN apt update && apt upgrade -y

# La librería openai-whisper utiliza ffmpeg, lo instalamos
RUN apt install ffmpeg -y

# Instalamos las fuentes
RUN apt-get update && apt-get install -y fonts-dejavu && \
    # Habilitamos el componente 'contrib' para poder instalar las fuentes de Microsoft
    echo "deb http://deb.debian.org/debian bookworm contrib" >> /etc/apt/sources.list && \
    apt-get update && \
    # Pre-aceptamos la licencia de EULA para la instalación no interactiva
    echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
    # Instalamos el paquete de fuentes
    apt-get install -y ttf-mscorefonts-installer && \
    # Limpiamos la cache de apt para reducir el tamaño de la imagen
    rm -rf /var/lib/apt/lists/*

# Instalamos las librerías necesarias de python
RUN pip install --no-cache-dir \
    openai-whisper \ 
    moviepy==1.0.3 \
    pillow 

# Entramos o creamos (si es la primera vez) nuestro directorio de trabajo
WORKDIR /autoSubtitlesGenerator
# Copiamos el código de python a este directorio
COPY procesamiento.py /autoSubtitlesGenerator

# Comando que se ejecutara al crear el contenedor
CMD ["python", "procesamiento.py"]