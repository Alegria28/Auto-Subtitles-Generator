#!/bin/bash

# Se instala lo necesario en el sistema para poder ejecutar el programa

echo "🎯 Preparing system..."

# Verificamos si tenemos docker instalado
if ! command -v docker &> /dev/null
then
    echo "❌ Error: docker is not installed. Please install it and run this script again." >&2
    read -p "Press [Enter] to exit... 🚪"
    exit 1
else
    echo "🐳 docker is already installed."
fi

# Verificamos si tenemos pyenv instalado
if ! command -v pyenv &> /dev/null
then
    echo "❌ Error: pyenv is not installed. Please install it and run this script again." >&2
    read -p "Press [Enter] to exit... 🚪"
    exit 1
else
    echo "🐍 pyenv is already installed."
fi

# Verificamos si tenemos el modulo venv instalado
if ! python3 -c 'import venv' &> /dev/null
then
    echo "🔍 venv module not found, installing..."
    sudo apt install python3-venv
else
    echo "✅ venv module already installed"
fi

# Verificamos si no hay un entorno virtual
if [ ! -n "$VIRTUAL_ENV" ]; 
then
    echo "📦 Creating virtual environment"
    python3 -m venv venv
fi

# Activamos el entorno virtual
echo "🔧 Activating virtual environment"
source venv/bin/activate

# Verificamos si tenemos el modulo tkinter instalado
if ! python3 -c 'import tkinter' &> /dev/null
then
    echo "🔍 tkinter module not found, installing..."
    sudo apt install python3-tk
else
    echo "✅ tkinter module already installed"
fi

# Instalamos los módulos necesarios
echo "📥 Installing necessary modules"
pip install --upgrade pip
pip install -r requirements.txt

# Instalamos paquetes necesarios
echo "📥 Installing necessary packages" 
if ! command -v vlc &> /dev/null
then
    echo "🔍 vlc not found, installing..."
    sudo apt install vlc -y
else
    echo "✅ vlc is already installed."
fi

echo "✅ System ready"
read -p "Press [Enter] to exit... 👋"