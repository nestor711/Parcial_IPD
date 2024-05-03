import os
import subprocess
import json
import yt_dlp

# Carpeta principal para la descarga de videos
carpeta_descarga = 'download_videos'
os.makedirs(carpeta_descarga, exist_ok=True)

# Cargar el archivo JSON con los canales
with open('channels.json') as f:
    canales_data = json.load(f)

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
        ydl.download([canal['url']])

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
