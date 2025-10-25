import subprocess
import os

try:
    print("Instalando dependencias...")
    subprocess.check_call(["pip", "install", "-r", "requirements.txt"])
    print("Paquetes instalados correctamente.")
except subprocess.CalledProcessError as e:
    print(f"Error al instalar paquetes: {e}")
    exit()

try:
    print("Iniciando ChuyiBot...")
    os.system("python ChuyiBot.py")
except Exception as e:
    print(f"Error al ejecutar el bot: {e}")
