# *-* coding: utf-8 *-*
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
import qrcode
import io
from endesive.pdf import cms
import re
from canvas import crear_canvas
import os
from guardarqr import guardaqrruta
from guardarcanvas import guardacanvasruta

#python server.py 
def firmar(contraseña, certificado, pdf):

    #Movi----------------------------------------------------------------------
    # with open("cert.p12", "rb") as fp:
    p12 = pkcs12.load_key_and_certificates(
        certificado.read(), contraseña.encode("ascii"), backends.default_backend()
    )
    #p12[1].
    
    #sacar la cadena que tiene el nombre
    subject = p12[1].subject.rfc4514_string()

    # Usamos una expresión regular para buscar el valor del atributo CN el cual tiene el nombre
    match = re.search(r'CN=([^,]+)', subject)
    nombre = match.group(1)
    
    print("Emisor del certificado:", nombre)

    #Fecha Actual
    fecha_a = datetime.datetime.now()
    fecha_actual = fecha_a.date()
    print("Fecha :", fecha_actual)

    #Movi----------------------

    ruta_completa = guardaqrruta()

    #----------------------------

    #datos para el qr:
    #nombre = "JuanJosejarabarrra Klindesr Arve saciases"
    fecha = fecha_actual
    empresa = "Xtintor"
    localiza = "UTEQ"
    validar =  "www.firmadigital.gob.ec"
    datos = f"Firmado por: {nombre},\nRazon: {empresa},\nLocalizacion: {localiza},\nFecha: {fecha},\nValidar con: {validar}"
    #construir el qr 
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
    )
    qr.add_data(datos)
    qr.make(fit=True)
    img = qr.make_image(fill='black',back_color='white')
    img.save(ruta_completa)

    #Generar el canvas----------------------------------
    # Utilizar la función para crear el canvas
    qr_imagen_path = ruta_completa  #ubicación real de la imagen QR
    canvas = crear_canvas(nombre, qr_imagen_path)

    # Guardar el canvas en un archivo o mostrarlo en pantalla
    canvas.save(guardacanvasruta())

    #--------------------------------------------

    #coordenadas
    

    #firmador
    date = datetime.datetime.utcnow() - datetime.timedelta(hours=12)
    date = date.strftime("D:%Y%m%d%H%M%S+00'00'")

    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 120,
        "sigpage": 1,
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        # A=izquierda  B=arriba  C=A+60   D=B+60  
        #        "signaturebox": (194, 510, 254, 570), 
        #"signaturebox": (194, 120, 254, 180),
        "signaturebox": (194, 120, 320, 180),  
        #"signature": nombre,
        "signature_img": "canvas.png",
        "contact": "hola@ejemplo.com",
        "location": "Ubicación",
        "signingdate": date,
        "reason": "Razón",
        "password": contraseña,
    }


    #datau = open(fname, "rb").read()
    datau = pdf.read()
    datas = cms.sign(datau, dct, p12[0], p12[1], p12[2], "sha256")
    return datau, datas

    """
    fname = "test.pdf"
    with open(fname, "wb") as fp:
        fp.write(datau)
        fp.write(datas)
    """
