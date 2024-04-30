#VERSIÓN DE UN SOLO HILO (SECUENCIAL)

import os
import json
import datetime
import subprocess

# Cargar el archivo JSON
with open('channels2.json', 'r') as f:
    data = json.load(f)

# Crear la carpeta para los audios extraídos
output_folder = 'extracted_audios'
os.makedirs(output_folder, exist_ok=True)

# Función para descargar el video y extraer su audio
def download_and_extract_audio(video_url, channel_name):
    # Obtener el ID del video
    video_id = video_url.split('/')[-1].split('?')[0]
    
    # Definir la ruta de salida para el archivo de video descargado y el audio en formato mp3
    video_file = os.path.join(output_folder, f'{video_id}.mp4')
    audio_folder = os.path.join(output_folder, f'audio_channel_{channel_name}')
    os.makedirs(audio_folder, exist_ok=True)
    audio_file = os.path.join(audio_folder, f'{video_id}.mp3')
    
    try:
        # Descargar el video usando yt-dlp
        subprocess.run(['yt-dlp', '--format', 'bestaudio', '-o', video_file, video_url], check=True)
        
        # Verificar si el archivo de video se descargó correctamente
        if os.path.isfile(video_file):
            # Extraer el audio del video usando ffmpeg y guardarlo en formato mp3
            subprocess.run(['ffmpeg', '-i', video_file, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', audio_file])
            
            # Eliminar el video descargado
            os.remove(video_file)
            print(f"Audio de '{video_url}' extraído y video eliminado.")
        else:
            print(f"Error al descargar el video de '{video_url}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error al descargar el video de '{video_url}': {e}")

# Iterar sobre los canales y sus videos
for canal in data['canales']:
    print(f"Descargando y extrayendo audios del video del canal '{canal['nombre_canal']}'...")
    for video in canal['videos']:
        download_and_extract_audio(video, canal['nombre_canal'])

        # Registro de la fecha de descarga
        fecha_descarga = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Guardar registro en un archivo de texto
        with open('registro.txt', 'a') as registro_file:
            registro_file.write(f"Video: {video}\nFecha de descarga: {fecha_descarga}\n\n")

print("Proceso completado.")