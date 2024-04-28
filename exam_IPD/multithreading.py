#EJECUCIÓN DEL APLICATIVO CON MÚLTIPLES HILOS (MULTITHREADING)

# Los números de hilos se especifican utilizando el parámetro max_workers al crear los objetos ThreadPoolExecutor.
# llevandose a cabo con 4,8 y 16 unidades de procesamiento basado en el documento del examen. 
import os
import json
import datetime
import subprocess
from concurrent.futures import ThreadPoolExecutor

# Cargar el archivo JSON
with open('Channels.json', 'r') as f:
    data = json.load(f)

# Crear la carpeta para los audios extraídos
output_folder = 'extracted_audios'
os.makedirs(output_folder, exist_ok=True)

# Función para descargar el video y extraer su audio correspondiente
def download_and_extract_audio(video_url, channel_name):
    # Obtener el ID del video
    video_id = video_url.split('/')[-1].split('?')[0]
    
    # Definir la ruta de salida para el archivo de video descargado y el audio en formato mp3
    video_file = os.path.join(output_folder, f'{video_id}.mp4')
    audio_folder = os.path.join(output_folder, f'audio_channel_{channel_name}')
    os.makedirs(audio_folder, exist_ok=True)
    audio_file = os.path.join(audio_folder, f'{video_id}.mp3')
    
    try:
        # Descargar el video usando la herramienta yt-dlp
        subprocess.run(['yt-dlp', '--format', 'bestaudio', '-o', video_file, video_url], check=True)
        
        # Verificar si el archivo de video se descargó correctamente
        if os.path.isfile(video_file):
            # Extraer el audio del video usando la herramienta ffmpeg y guardarlo en formato mp3
            subprocess.run(['ffmpeg', '-i', video_file, '-vn', '-acodec', 'libmp3lame', '-q:a', '2', audio_file])
            
            # Eliminar el video descargado
            os.remove(video_file)
            print(f"Audio de '{video_url}' extraído y video eliminado.")
        else:
            print(f"Error al descargar el video de '{video_url}'.")
    except subprocess.CalledProcessError as e:
        print(f"Error al descargar el video de '{video_url}': {e}")

# Función para procesar los videos de un canal
def process_channel_videos(channel):
    channel_name = channel['nombre_canal']
    videos = channel['videos']
    
    print(f"Descargando y extrayendo audios del canal '{channel_name}'...")
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Descargar y extraer audios en múltiples hilos
        executor.map(lambda video_url: download_and_extract_audio(video_url, channel_name), videos)

    # Registro de la fecha de descarga
    fecha_descarga = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Guardar registro de los videos descargados en un archivo de texto
    with open('registro.txt', 'a') as registro_file:
        for video_url in videos:
            registro_file.write(f"Video: {video_url}\nFecha de descarga: {fecha_descarga}\n\n")

# Iterar sobre los canales y procesar sus videos en hilos
with ThreadPoolExecutor(max_workers=4) as executor:
    executor.map(process_channel_videos, data['canales'])

print("Proceso completado.")