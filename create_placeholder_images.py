import os
from PIL import Image, ImageDraw, ImageFont

def crear_imagen_placeholder(ancho, alto, texto, nombre_archivo, color_fondo=(81, 51, 64), color_texto=(255, 255, 255)):
    """Crea una imagen placeholder con texto"""
    
    # Crear directorio si no existe
    os.makedirs('static/images', exist_ok=True)
    
    # Crear imagen
    imagen = Image.new('RGB', (ancho, alto), color_fondo)
    draw = ImageDraw.Draw(imagen)
    
    # Intentar usar una fuente, si no está disponible usar la default
    try:
        # Para Windows
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        try:
            # Para Linux
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        except:
            try:
                # Para Mac
                font = ImageFont.truetype("/Library/Fonts/Arial.ttf", 24)
            except:
                # Fuente por defecto
                font = ImageFont.load_default()
    
    # Calcular posición del texto
    try:
        bbox = draw.textbbox((0, 0), texto, font=font)
        texto_ancho = bbox[2] - bbox[0]
        texto_alto = bbox[3] - bbox[1]
    except:
        # Método alternativo para versiones más antiguas de PIL
        texto_ancho = len(texto) * 12
        texto_alto = 24
    
    x = (ancho - texto_ancho) // 2
    y = (alto - texto_alto) // 2
    
    # Dibujar texto
    draw.text((x, y), texto, fill=color_texto, font=font)
    
    # Guardar imagen
    ruta_completa = os.path.join('static/images', nombre_archivo)
    imagen.save(ruta_completa)
    print(f"✅ Creada: {ruta_completa}")

def crear_todas_las_imagenes():
    """Crea todas las imágenes placeholder necesarias"""
    
    print("🎨 CREANDO IMÁGENES PLACEHOLDER...")
    print("=" * 50)
    
    # Imágenes de habitaciones (400x300)
    crear_imagen_placeholder(400, 300, "HABITACIÓN LUJO", "room-lujo.jpg", (81, 51, 64))
    crear_imagen_placeholder(400, 300, "HABITACIÓN ESTÁNDAR", "room-estandar.jpg", (125, 79, 101))
    crear_imagen_placeholder(400, 300, "HABITACIÓN ECONÓMICA", "room-economica.jpg", (169, 107, 138))
    crear_imagen_placeholder(400, 300, "HABITACIÓN DEFAULT", "room-default.jpg", (58, 36, 46))
    
    # Avatar por defecto (150x150)
    crear_imagen_placeholder(150, 150, "AVATAR", "avatar-default.jpg", (81, 51, 64))
    
    # Imágenes del carousel (800x400)
    crear_imagen_placeholder(800, 400, "HOTELES URBANOS", "ciudad.jpg", (44, 62, 80))
    crear_imagen_placeholder(800, 400, "RESORTS PLAYEROS", "playa.jpg", (23, 113, 153))
    crear_imagen_placeholder(800, 400, "LODGES DE MONTAÑA", "montañas.jpg", (56, 103, 65))
    crear_imagen_placeholder(800, 400, "ECO-HOTELES", "naturaleza.jpg", (76, 145, 65))
    
    # Testimonios (150x150)
    crear_imagen_placeholder(150, 150, "ESTUDIANTE 1", "testimonio1.jpg", (81, 51, 64))
    crear_imagen_placeholder(150, 150, "ESTUDIANTE 2", "testimonio2.jpg", (241, 8, 113))
    
    # Logos
    crear_imagen_placeholder(200, 80, "UTD", "logo_1.jpg", (255, 255, 255), (81, 51, 64))
    crear_imagen_placeholder(200, 100, "PNFI", "logo_2.jpg", (255, 255, 255), (241, 8, 113))
    
    # Favicon (32x32)
    crear_imagen_placeholder(32, 32, "TH", "favicon1.ico", (81, 51, 64))
    
    print("=" * 50)
    print("🎉 TODAS LAS IMÁGENES HAN SIDO CREADAS EXITOSAMENTE!")
    print("📍 Ubicación: static/images/")

if __name__ == '__main__':
    crear_todas_las_imagenes()