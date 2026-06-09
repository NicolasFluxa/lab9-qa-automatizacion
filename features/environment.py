# features/environment.py
# Asegura que el directorio raíz del proyecto esté en sys.path
# para que Behave pueda importar los módulos de app/
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
