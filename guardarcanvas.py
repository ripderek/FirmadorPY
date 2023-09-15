import os
import datetime

def guardacanvasruta():

# Obtener la ruta del directorio actual donde se encuentra el script

    #Fecha Actual
    fecha_a = datetime.datetime.now()

    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    # Nombre de la carpeta que deseas crear
    nombre_carpeta = "canvas_generados"

    # Ruta completa de la carpeta que se creará
    carpeta_destino = os.path.join(directorio_actual, nombre_carpeta)

    # Crear la carpeta si no existe
    if not os.path.exists(carpeta_destino):
        os.makedirs(carpeta_destino)

    fecha_hora = fecha_a.strftime("%Y%m%d%H%M%S") + str(fecha_a.microsecond)
    #Poner nombre y fecha al qr unicos
    nombreqr = 'qrtelecapp'+fecha_hora+'.png'

    # Ruta completa del archivo QR, incluyendo la carpeta de destino
    ruta_completa = os.path.join(carpeta_destino, nombreqr)

    return ruta_completa