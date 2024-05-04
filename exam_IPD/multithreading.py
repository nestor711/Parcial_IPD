#EJECUCIÓN DEL APLICATIVO CON MÚLTIPLES HILOS (MULTITHREADING)

import os
import subprocess
import json
import yt_dlp
from datetime import datetime
import timeit
import threading

# Función para descargar y convertir videos en un hilo
def procesar_canal(canal, carpeta_descarga, registro_path):
    # Extraer información del canal
    nombre_canal = canal['nombre']
    subcarpeta_canal = os.path.join(carpeta_descarga, nombre_canal)
    os.makedirs(subcarpeta_canal, exist_ok=True)

    # Opciones de descarga para yt-dlp
    ydl_opts = {
        'format': 'worstvideo[ext=mp4]+bestaudio/webm',
        'playlist_items': '1-5',  
        'outtmpl': os.path.join(subcarpeta_canal, '%(title)s.%(ext)s'), 
    }

    # Descargar los videos del canal
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(canal['url'], download=True)
        videos = info.get('entries', [])
        if videos:
            for video in videos:
                title = video['title']
                upload_date = video.get('upload_date', 'Unknown')
                upload_date_str = datetime.strptime(upload_date, '%Y%m%d').strftime('%Y-%m-%d')
                current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                with open(registro_path, 'a') as registro_file:
                    registro_file.write(f"\t- Video: {title} - Fecha de publicacion: {upload_date_str} - Fecha y hora de descarga: {current_date_time}\n")

    # Convertir los videos descargados a archivos de audio
    for archivo in os.listdir(subcarpeta_canal):
        if archivo.endswith('.webm'):
            nombre_sin_ext = os.path.splitext(archivo)[0]
            archivo_webm = os.path.join(subcarpeta_canal, archivo)
            archivo_mp3 = os.path.join(subcarpeta_canal, f'{nombre_sin_ext}.mp3')
            subprocess.run(['ffmpeg', '-i', archivo_webm, '-vn', '-acodec', 'libmp3lame', '-ab', '128k', archivo_mp3])
            os.remove(archivo_webm)

# Función principal
def main():
    # Carpeta principal para la descarga de videos
    carpeta_descarga = 'download_videos'
    os.makedirs(carpeta_descarga, exist_ok=True)
    registro_path = 'registroSecuencial.txt'
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Escribir la fecha y hora de inicio en el archivo de registro
    with open(registro_path, 'a') as registro_file:
        registro_file.write(f"\nFecha y hora de la ejecucion: {current_date_time}\n\n")

    # Cargar los datos de los canales desde el archivo JSON
    with open('channels.json') as f:
        canales_data = json.load(f)

    # Iniciar el cronómetro
    start_time = timeit.default_timer()

    # Crear una lista para almacenar los hilos
    threads = []

    # Procesar cada canal en un hilo separado
    for canal in canales_data['canales']:
        thread = threading.Thread(target=procesar_canal, args=(canal, carpeta_descarga, registro_path))
        threads.append(thread)
        thread.start()

    # Esperar a que todos los hilos terminen
    for thread in threads:
        thread.join()

    # Cambiar el nombre de la carpeta de videos a audios
    carpeta_audios = carpeta_descarga.replace('videos', 'audios')
    os.rename(carpeta_descarga, carpeta_audios)

    # Calcular el tiempo de ejecución
    elapsed_time = timeit.default_timer() - start_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    # Indicar que la ejecución ha terminado y mostrar el tiempo de ejecución
    print("\n\n\nLa ejecucion ha terminado.")
    print(f"Tiempo de ejecucion: {elapsed_minutes} minutos y {elapsed_seconds} segundos")

# Ejecutar la función principal si este script es el programa principal
if __name__ == "__main__":
    main()
