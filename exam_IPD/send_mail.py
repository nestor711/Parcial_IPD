import smtplib   #Libreria para enviar correos electrónicos a través de un servidor SMTP
from email.mime.multipart import MIMEMultipart   #Clase para representar un mensaje de correo electrónico multipartes
from email.mime.text import MIMEText   #Clase para el texto en un mensaje de correo electónico

def enviar_correo(destinatario, asunto, mensaje):
    # Configuración del servidor SMTP
    smtp_server = 'smtp.gmail.com'
    puerto = 587
    remitente = 'ExamIPD2024@gmail.com'
    contraseña = 'parcial_IPD'

    # Crear objeto mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto

    # Cuerpo del mensaje
    cuerpo_mensaje = mensaje
    msg.attach(MIMEText(cuerpo_mensaje, 'plain'))

    try:
        # Conectar al servidor SMTP y enviar correo
        server = smtplib.SMTP(smtp_server, puerto)
        server.starttls()
        server.login(remitente, contraseña)
        texto = msg.as_string()
        server.sendmail(remitente, destinatario, texto)
        print("Correo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        # Cerrar la conexión con el servidor SMTP
        server.quit()

if __name__ == "__main__":
    destinatario = 'urrea.brayan@correounivalle.edu.co' 
    asunto = 'Audio descargado correctamente'
    mensaje = '¡EL AUDIO SE HA DESCARGADO CORRECTAMENTE!. Puede encontrarlo en la siguiente ruta: /ruta/del/audio'

    enviar_correo(destinatario, asunto, mensaje)
