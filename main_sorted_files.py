
import os
import shutil
import hashlib
import re
import time
from pathlib import Path
from datetime import datetime

# By: Carlos Tivan
def get_file_extension(file_path):
    """Obtiene la extensión de un archivo."""
    return Path(file_path).suffix.lower()


def get_file_checksum(file_path):
    """Calcula el checksum (hash) de un archivo."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def move_file_to_directory(file_path, destination_directory):
    """Mueve un archivo a un directorio destino, moviendo el archivo existente a otra carpeta si es necesario."""
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    destination_path = os.path.join(destination_directory, os.path.basename(file_path))

    if os.path.exists(destination_path):
        # Si el archivo destino ya existe, moverlo a una carpeta de respaldo antes de mover el nuevo archivo
        backup_directory = os.path.join(destination_directory, "backup")
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)

        # Generar un nombre único para el archivo de respaldo (basado en la fecha y hora actual)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file_name = f"backup_{os.path.basename(destination_path)}_{timestamp}"
        backup_file_path = os.path.join(backup_directory, backup_file_name)

        # Mover el archivo existente a la carpeta de respaldo
        shutil.move(destination_path, backup_file_path)
        print(f"Archivo existente movido a la carpeta de respaldo: {backup_file_path}")

    try:
        shutil.move(file_path, destination_path)
    except Exception as e:
        print(f"Error al mover el archivo a '{destination_directory}': {e}")


def remove_numbered_files(directory_path):
    """Elimina archivos con nombres que contienen números entre paréntesis."""
    try:
        files = os.listdir(directory_path)
        pattern = re.compile(r'\(\d+\)')

        for file_name in files:
            file_path = os.path.join(directory_path, file_name)

            if os.path.isfile(file_path) and pattern.search(file_name):
                os.remove(file_path)
                print(f"Archivo eliminado: {file_path}")

    except Exception as e:
        print(f"Error al eliminar archivos numerados en '{directory_path}': {e}")

def organize_and_remove_duplicates(dir_path):
    """Clasifica archivos por extensión, elimina duplicados y mueve a nuevas carpetas."""
    try:
        extension_files = {}

        for file_name in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file_name)

            if os.path.isfile(file_path):
                file_extension = get_file_extension(file_path)

                if file_extension not in extension_files:
                    extension_files[file_extension] = []

                extension_files[file_extension].append(file_path)

        for extension, file_list in extension_files.items():
            extension_directory = os.path.join(dir_path, extension.strip('.').upper())

            if not os.path.exists(extension_directory):
                os.makedirs(extension_directory)

            for file_path in file_list:
                move_file_to_directory(file_path, extension_directory)

            remove_numbered_files(extension_directory)

    except Exception as e:
        print(f"Error al organizar y eliminar archivos numerados en '{dir_path}': {e}")


def watch_for_new_files(dir_path, max_runtime=10):
    """Observa el directorio en busca de nuevos archivos durante un tiempo limitado."""
    start_time = time.time()
    processed_files = set()

    while time.time() - start_time < max_runtime:
        try:
            files = [os.path.join(dir_path, f) for f in os.listdir(dir_path)
                     if os.path.isfile(os.path.join(dir_path, f))]

            new_files = [f for f in files if f not in processed_files]

            if new_files:
                organize_and_remove_duplicates(dir_path)
                processed_files.update(new_files)
                print("Procesamiento completado para nuevos archivos.")

        except Exception as e:
            print(f"Error inesperado al procesar archivos nuevos en '{dir_path}': {e}")

        time.sleep(1)  # Esperar 1 segundo antes de volver a verificar

    print(f"Tiempo máximo de ejecución ({max_runtime} segundos) alcanzado. El proceso ha terminado.")


if __name__ == "__main__":
    dir_path = 'C:/Users/Carlos/Downloads'
    watch_for_new_files(dir_path, max_runtime=10)  # Ejecutar durante un máximo de 10 segundos
