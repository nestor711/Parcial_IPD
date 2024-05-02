import os
import subprocess
import json

# Crear la carpeta para los audios extraídos
carpeta_descarga = 'download_videos'
os.makedirs(carpeta_descarga, exist_ok=True)

# Definir variables para los ejecutables
YT_DLP = "executables/yt-dlp.exe"  # Ruta al ejecutable de yt-dlp
FFMPEG = "executables/ffmpeg.exe"  # Ruta al ejecutable de ffmpeg

# Opciones de yt-dlp para especificar la plantilla de nombre de archivo
ydl_opts = {
    'outtmpl': '',  # Inicializar la plantilla de nombre de archivo vacía
}

# Cargar el archivo JSON con los canales
with open('channels.json') as f:
    canales_data = json.load(f)

# Recorrer los canales del archivo JSON
for canal in canales_data['canales']:
    # Crear la subcarpeta para el canal actual
    nombre_canal = canal['nombre']
    subcarpeta_canal = os.path.join(carpeta_descarga, nombre_canal)
    os.makedirs(subcarpeta_canal, exist_ok=True)

    # Modificar la plantilla de nombre de archivo
    ydl_opts['outtmpl'] = os.path.join(subcarpeta_canal, '%(title)s.%(ext)s')

    # Modificar el comando de descarga para el canal actual
    comando_descarga = [
        YT_DLP,
        '--format', 'worstvideo[ext=mp4]+bestaudio/webm',
        '--playlist-items', '1-5',  # Ajustar el rango de videos según se desee
        canal['url'],
        '--output', ydl_opts['outtmpl'],
    ]

    # Ejecutar el comando de descarga para el canal actual
    subprocess.call(comando_descarga)

    # Convertir cada video webm a audio mp3
    for archivo in os.listdir(subcarpeta_canal):
        if archivo.endswith('.webm'):
            nombre_sin_ext = os.path.splitext(archivo)[0]
            comando_conversion = [
                FFMPEG,
                '-i', os.path.join(subcarpeta_canal, archivo),
                '-vn',
                '-acodec', 'libmp3lame',
                '-ab', '128k',
                os.path.join(subcarpeta_canal, f'{nombre_sin_ext}.mp3'),
            ]
            subprocess.call(comando_conversion)

            # Eliminar el video webm original
            os.remove(os.path.join(subcarpeta_canal, archivo))

# Cambiar el nombre de la carpeta "download_videos" a "download_audios"
os.rename(carpeta_descarga, carpeta_descarga.replace('videos', 'audios'))






