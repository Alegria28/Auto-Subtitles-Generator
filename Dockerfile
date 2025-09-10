# Utilizamos la ultima y mas ligera version para el contenedor (utiliza Debian)
FROM python:3.13-slim

# Se actualiza el sistema
RUN apt update && apt upgrade -y

# La librería openai-whisper utiliza ffmpeg, lo instalamos
RUN apt install ffmpeg -y

# Instalamos una fuente básica
RUN apt install fonts-dejavu -y

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