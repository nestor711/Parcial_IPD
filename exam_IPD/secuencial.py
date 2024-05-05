import os
import subprocess
import json
import yt_dlp
from datetime import datetime
import timeit

# Función principal
def main():
    # Carpeta principal para la descarga de videos
    carpeta_descarga = 'download_videos'
    os.makedirs(carpeta_descarga, exist_ok=True)

    # Crear el archivo de registro
    registro_path = 'registro.txt'

    # Obtener la fecha y hora actual del PC
    current_date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Escribir la fecha y hora al principio del archivo de registro
    with open(registro_path, 'a') as registro_file:
        registro_file.write(f"\nSecuencial - Fecha y hora de la ejecucion: {current_date_time}\n\n")

    # Cargar el archivo JSON con los canales
    with open('channels.json') as f:
        canales_data = json.load(f)

    # Iniciar el timer
    start_time = timeit.default_timer()

    # Variable para seguir el último canal procesado
    last_canal = None

    # Recorrer los canales del archivo JSON
    for canal in canales_data['canales']:
        # Crear la subcarpeta para el canal actual
        nombre_canal = canal['nombre']
        subcarpeta_canal = os.path.join(carpeta_descarga, nombre_canal)
        os.makedirs(subcarpeta_canal, exist_ok=True)

        # Modificar la plantilla de nombre de archivo para yt-dlp
        ydl_opts = {
            'format': 'worstvideo[ext=mp4]+bestaudio/webm',
            'playlist_items': '1-5',  # Ajustar el rango de videos según se desee
            'outtmpl': os.path.join(subcarpeta_canal, '%(title)s.%(ext)s'),  # Ruta de salida de los archivos
        }

        # Descargar los videos del canal actual
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
                        if nombre_canal != last_canal:
                            registro_file.write(f"Canal -> {nombre_canal}:\n")
                            last_canal = nombre_canal
                        registro_file.write(f"\t- Video: {title} - Fecha de publicacion: {upload_date_str} - Fecha y hora de descarga: {current_date_time}\n")

        # Convertir cada video webm a audio mp3
        for archivo in os.listdir(subcarpeta_canal):
            if archivo.endswith('.webm'):
                nombre_sin_ext = os.path.splitext(archivo)[0]
                archivo_webm = os.path.join(subcarpeta_canal, archivo)
                archivo_mp3 = os.path.join(subcarpeta_canal, f'{nombre_sin_ext}.mp3')
                subprocess.run(['ffmpeg', '-i', archivo_webm, '-vn', '-acodec', 'libmp3lame', '-ab', '128k', archivo_mp3])

                # Eliminar el video webm original
                os.remove(archivo_webm)

    # Cambiar el nombre de la carpeta "download_videos" a "download_audios"
    carpeta_audios = carpeta_descarga.replace('videos', 'audios')
    os.rename(carpeta_descarga, carpeta_audios)

    # Calcular el tiempo de ejecución
    elapsed_time = timeit.default_timer() - start_time
    elapsed_minutes = int(elapsed_time // 60)
    elapsed_seconds = int(elapsed_time % 60)

    # Indicar que la ejecución ha terminado y mostrar el tiempo de ejecución
    print("\n\n\nLa ejecucion ha terminado.")
    print(f"Tiempo de ejecucion: {elapsed_minutes} minutos y {elapsed_seconds} segundos")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
