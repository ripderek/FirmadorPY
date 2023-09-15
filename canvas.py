from PIL import Image, ImageDraw, ImageFont

def crear_canvas(nombre_usuario, qr_imagen_path):
    # Crear una nueva imagen (canvas) con un tamaño adecuado
    canvas = Image.new('RGB', (1000, 500), 'white')

    # Dibujar un rectángulo alrededor del canvas (contorno)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, canvas.width - 1, canvas.height - 1], outline="black")

    # Dibujar el QR en el canvas
    qr_imagen = Image.open(qr_imagen_path)
    canvas.paste(qr_imagen, (1, 1))

    # Crear un objeto de dibujo en la imagen
    draw = ImageDraw.Draw(canvas)

    # Configurar la fuente y el tamaño del texto
    font1 = ImageFont.truetype("arial.ttf", 38)
    font2 = ImageFont.truetype("arial.ttf", 60)

    # Dividir el nombre en palabras
    palabras = nombre_usuario.split()

    # Inicializar líneas para el nombre y apellidos
    lineas_nombre = []
    lineas_apellidos = []

    # Valor aproximado del ancho máximo permitido
    ancho_maximo = 300

    # Separar el nombre y apellidos en líneas según el ancho del canvas
    for palabra in palabras:
        nombre_actual = " ".join(lineas_nombre + [palabra])
        apellidos_actual = " ".join(lineas_apellidos + [palabra])

        # Estimar el ancho del texto
        ancho_nombre = len(nombre_actual) * 20  # Valor aproximado basado en la fuente y tamaño
        ancho_apellidos = len(apellidos_actual) * 20  # Valor aproximado basado en la fuente y tamaño

        if ancho_nombre <= ancho_maximo:
            lineas_nombre.append(palabra)
        elif ancho_apellidos <= ancho_maximo:
            lineas_apellidos.append(palabra)

    # Truncar el nombre y apellidos si son muy largos
    for i in range(len(lineas_nombre)):
        if len(" ".join(lineas_nombre)) * 20 > ancho_maximo:
            lineas_nombre[-1] = lineas_nombre[-1][:len(lineas_nombre[-1])-1] + "..."
    
    for i in range(len(lineas_apellidos)):
        if len(" ".join(lineas_apellidos)) * 20 > ancho_maximo:
            lineas_apellidos[-1] = lineas_apellidos[-1][:len(lineas_apellidos[-1])-1] + "..."

    # Agregar el texto "firmado electrónicamente por:"
    draw.text((465, 150), "Firmado electrónicamente por:", fill="black", font=font1)

    # Agregar el nombre del usuario (parte superior)
    nombre_completo = " ".join(lineas_nombre)
    draw.text((465, 220), nombre_completo, fill="black", font=font2)

    # Agregar los apellidos (parte inferior)
    apellidos_completos = " ".join(lineas_apellidos)
    draw.text((465, 300), apellidos_completos, fill="black", font=font2)

    return canvas
