# *-* coding: utf-8 *-*
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12
import qrcode
import io
from endesive.pdf import cms

#python server.py 
def firmar(contraseña, certificado, pdf):
    #datos para el qr:
    nombre = "Raul Steven Coello Castillo"
    fecha = "2023-09-05"
    aplicacion ="SGD"
    empresa = "Xtintor"
    datos = f"Firmado por: {nombre}, Fecha: {fecha}, Razon: {empresa}"
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
    img.save('qrtelecapp.png')

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
        "signaturebox": (194, 510, 254, 570), 
        #"signature": nombre,
        "signature_img": "qrtelecapp.png",
        "contact": "hola@ejemplo.com",
        "location": "Ubicación",
        "signingdate": date,
        "reason": "Razón",
        "password": contraseña,
    }
    # with open("cert.p12", "rb") as fp:
    p12 = pkcs12.load_key_and_certificates(
        certificado.read(), contraseña.encode("ascii"), backends.default_backend()
    )
    #p12[1].
    

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
