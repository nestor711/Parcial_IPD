# Implementación de un Descargador de Videos y Extractor de Audio de YouTube en Python

Este proyecto tiene como objetivo principal evaluar el speedup de una aplicación intensiva en operaciones de entrada y salida al utilizar hilos (threading) y procesos (processing) en Python. La aplicación automatiza la descarga de vídeos de YouTube y la extracción de sus audios correspondientes, utilizando las herramientas yt-dlp y ffmpeg disponibles para Linux. La aplicación permite elegir entre diferentes configuraciones de ejecución: un solo hilo, multithreading y multiprocessing con 4, 8 y 16 unidades de procesamiento.

## Integrantes del Grupo
- Brayan Camilo Urrea Jurado - 2410023 (urrea.brayan@correounivalle.edu.co)
- Kevin Alejandro Velez Agudelo - 2123281 (kevin.alejandro.velez@correounivalle.edu.co)
- Néstor David Heredia Gutierrez - 2058558 (nestor.heredia@correounivalle.edu.co)

## Descripción de Requerimientos
La aplicación debe cumplir con los siguientes requerimientos:
- Automatizar la descarga de vídeos de YouTube.
- Extraer los audios correspondientes a los vídeos descargados.
- Utilizar yt-dlp y ffmpeg para la descarga y extracción de audio.
- Implementar tres versiones de la aplicación: un solo hilo, múltiples hilos y múltiples procesos.
- Conservar solo los audios, eliminando los vídeos descargados.
- Llevar un registro de los vídeos descargados, incluyendo la fecha de publicación en YouTube y la fecha de descarga.

## Requisitos
- Python 3.x
- yt-dlp
- ffmpeg

## Forma de Uso o Ejecución
Para ejecutar la aplicación, sigue estos pasos:
1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias (yt-dlp y ffmpeg).
3. Ejecuta el script de Python correspondiente a la versión que deseas probar.

## Descripción de la Lógica del Aplicativo
El aplicativo se divide en tres versiones, cada una implementando un enfoque diferente para la concurrencia:
1. **Un Solo Hilo:** Todas las tareas se ejecutan secuencialmente en un solo hilo.
2. **Múltiples Hilos:** Se utiliza el módulo threading para ejecutar múltiples tareas en paralelo dentro del mismo proceso.
3. **Múltiples Procesos:** Se utiliza el módulo multiprocessing para ejecutar múltiples procesos independientes, cada uno con su propio hilo de ejecución.

## Diagrama
