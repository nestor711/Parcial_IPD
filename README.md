# Parcial_IPD

# Grupo de Trabajo
Néstor David Heredia Gutierrez - 2058558
Brayan Camilo Urrea Jurado - 2410023
Kevin Alejandro Velez Agudelo - 2123281

## Automatizador de Descarga y Extracción de Audio de YouTube

Esta aplicación automatiza la descarga de vídeos de cinco canales de YouTube y extrae sus respectivos audios. Utiliza las herramientas yt-dlp y ffmpeg en un entorno Linux para realizar estas tareas. En total, se descargarán 25 vídeos y se obtendrán 25 audios correspondientes a estos vídeos.

### Informe de Desempeño de la Aplicación

Este informe proporciona un análisis exhaustivo del desempeño de la aplicación de descarga y extracción de audio de YouTube, incluyendo la especificación de los elementos clave, los tiempos de ejecución y el cálculo de métricas de rendimiento.

### Especificaciones de Entrada:
- Se define un archivo YAML para especificar los canales de YouTube de los cuales se descargarán los vídeos.
- La estructura de almacenamiento para los registros de vídeos descargados se define en un formato específico.
### Especificaciones del Sistema:
- Se detalla el equipo de cómputo utilizado, incluyendo RAM y unidades de procesamiento.
- Se describe el ancho de banda disponible para la descarga de vídeos.
### Procesamiento Paralelo:
- Se investiga si las aplicaciones yt-dlp y ffmpeg admiten procesamiento paralelo.
- Se realiza un análisis sobre el número de unidades de procesamiento utilizadas y la justificación detrás de esta elección.
### Tiempo de Ejecución:
- Se lleva a cabo la ejecución de la aplicación en varios escenarios de procesamiento: con un solo hilo, multithreading y multiprocessing.
- Se registra el tiempo de ejecución en cada configuración y se calcula el promedio de cada ejecución.
### Métricas de Rendimiento:
- Se calcula el speedup y la eficiencia para cada configuración de procesamiento paralelo.
- Se determina el porcentaje de la aplicación que es paralelizable (f) a partir de los tiempos observados.
### Resultados y Conclusiones:
- Se presentan los resultados obtenidos y se analiza la consistencia del rendimiento en los diferentes escenarios.
- Se discuten las implicaciones de los hallazgos y se proporcionan recomendaciones para futuras mejoras de la aplicación.
- Este informe ofrece una visión completa del desempeño de la aplicación, desde la definición de entrada hasta el análisis de métricas de rendimiento, proporcionando una base sólida para la evaluación y optimización continua del sistema.
