# cspell: disable

# Modulo para poder trabajar con GUI (graphical user interface)
from tkinter import filedialog

# Para poder terminar el programa
import sys

# Para poder trabajar con las carpetas
import os

#
import shutil

NOMBRECARPETA = "carpetaCompartida"
NOMBREARCHIVO = os.path.join(NOMBRECARPETA, "pathVideo.txt")

# Punto de entrada al proyecto (dado que este programa se corre directamente y no es importado como modulo)
if __name__ == "__main__":

    # Al iniciar el programa abrimos el explorador de archivos para obtener el nombre del video con que trabajar
    pathVideoHost = filedialog.askopenfilename(
        title="Selecciona el video",
        # Tipo de archivos de video soportados
        filetypes=[("Video files", "*.mp4"), ("Video files", "*.mov")],
    )

    # Verificamos si se obtuvo el nombre del video
    if pathVideoHost:
        print("📂 La ruta del video en el host es: " + pathVideoHost), print()

        # Se crea la carpeta compartida entre el host y el contenedor si este no existe
        os.makedirs(
            NOMBRECARPETA, exist_ok=True
        )  # En caso de que ya exista, se ignora el error

        # Creamos la ruta relativa para esta carpeta NOMBRECARPETA/pathVideo (solo nombre del video, el basename)
        pathCarpetaCompartidaConVideo = os.path.join(
            NOMBRECARPETA, os.path.basename(pathVideoHost)
        )
        print("📂 Ruta creada para video: " + pathCarpetaCompartidaConVideo), print()

        # Copiamos el video a la carpeta compartida
        shutil.copy(pathVideoHost, pathCarpetaCompartidaConVideo)

        print("📂 Ruta creada para .txt: " + NOMBREARCHIVO), print()

        # Creamos un archivo .txt (cuya ruta esta en la carpetea compartida) donde escribimos la ruta que creamos para la carpeta compartida
        with open(NOMBREARCHIVO, "w") as f:
            f.write(pathCarpetaCompartidaConVideo)

    else:
        sys.exit("⚠️ No se pudo obtener el nombre del video")
