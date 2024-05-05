import os
import subprocess
import json
import yt_dlp
from datetime import datetime
import timeit
from multiprocessing import Process

# Función para descargar y convertir videos en un proceso
def procesar_canal(canal, carpeta_descarga, registro_path):
    nombre_canal = canal['nombre']
    subcarpeta_canal = os.path.join(carpeta_descarga, nombre_canal)
    os.makedirs(subcarpeta_canal, exist_ok=True)

    ydl_opts = {
        'format': 'worstvideo[ext=mp4]+bestaudio/webm',
        'playlist_items': '1-5',
        'outtmpl': os.path.join(subcarpeta_canal, '%(title)s.%(ext)s'),
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(canal['url'], download=True)
        videos = info.get('entries', [])
        if videos:
            for video in videos:
                title = video['title']
                upload_date = video.get('upload_date', 'Unknown')
                upload_date_str = datetime.strptime(upload_date, '%Y%m%d').strftime('%Y-%m-%d')
                current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Escribir información del video al registro con formato "Canal "nombre_canal" -> Video: ..."
                with open(registro_path, 'a') as registro_file:
                    registro_file.write(f"Canal \"{nombre_canal}\" -> Video: {title} - Fecha de publicación: {upload_date_str} - Fecha y hora de descarga: {current_date_time}\n")

    # Convertir videos a mp3
    for archivo in os.listdir(subcarpeta_canal):
        if archivo.endswith('.webm'):
            nombre_sin_ext = os.path.splitext(archivo)[0]
            archivo_webm = os.path.join(subcarpeta_canal, archivo)
            archivo_mp3 = os.path.join(subcarpeta_canal, f'{nombre_sin_ext}.mp3')
            subprocess.run(['ffmpeg', '-i', archivo_webm, '-vn', '-acodec', 'libmp3lame', '-ab', '128k', archivo_mp3])
            os.remove(archivo_webm)

def main(num_procesos):
    carpeta_descarga = 'download_videos'
    os.makedirs(carpeta_descarga, exist_ok=True)
    registro_path = 'registroMultiprocessing.txt'

    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(registro_path, 'a') as registro_file:
        registro_file.write(f"\nMultiprocessing - Fecha y hora de la ejecución: {current_date_time}\n\n")

    with open('channels.json') as f:
        canales_data = json.load(f)

    start_time = timeit.default_timer()
    procesos = []

    for canal in canales_data['canales']:
        proceso = Process(target=procesar_canal, args=(canal, carpeta_descarga, registro_path))
        procesos.append(proceso)
        proceso.start()

        # Limitar el número de procesos activos
        if len(procesos) >= num_procesos:
            for p in procesos:
                p.join()
            procesos = []

    for proceso in procesos:
        proceso.join()

    carpeta_audios = carpeta_descarga.replace('videos', 'audios')
    os.rename(carpeta_descarga, carpeta_audios)

    elapsed_time = timeit.default_timer() - start_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    print("\n\n\nLa ejecución ha terminado.")
    print(f"Tiempo de ejecución: {elapsed_minutes} minutos y {elapsed_seconds} segundos")

if __name__ == "__main__":
    num_procesos = 16  # Ajustar el número de procesos
    main(num_procesos)
