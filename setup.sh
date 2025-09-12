#!/bin/bash

# Se instala lo necesario en el sistema para poder ejecutar el programa

echo "🎯 Preparando sistema..."

# Verificamos si no hay un entorno virtual
if [ ! -n "$VIRTUAL_ENV" ]; then
    echo "📦 Creando entorno virtual"
    python3 -m venv venv
fi

# Activamos el entorno virtual
echo "🔧 Activando el entorno virtual"
source venv/bin/activate

# Instalamos los módulos necesarios
echo "📥 Instalando módulos necesarios"
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Sistema listo"