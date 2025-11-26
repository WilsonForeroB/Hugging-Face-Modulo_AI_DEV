import cv2
from PIL import Image, ImageEnhance, ImageOps, ImageFilter

def cargar_imagen_local(path: str):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen en el path → {path}")
    return img

# 3. Voltear verticalmente
def voltear_vertical(imagen):
    return imagen.transpose(Image.FLIP_TOP_BOTTOM)

# ======================
# Convertir imagen a base64
# ======================
def to_b64(img):
    ok, buffer = cv2.imencode(".png", img)
    if not ok:
        raise ValueError("No se pudo convertir a base64")
    return base64.b64encode(buffer).decode("utf-8")


# ======================
# Procesador principal
# ======================
def procesar_imagen_local(path: str):
    img = cargar_imagen_local(path)

def procesar_imagen_servicio_pillow():
    print('ENTRA A SERVICIO PROCESAR IMAGEN')

    print('1 cargar imagen ') 
    imagen = 'aqui  iria la imagen carga en local'
    #debo usar la función cargar_imagen_local
    print('2 procesar la imagen')
    # usar la funcion voltear_vertical
    print('3 convertir en base 64')
    imagen_64 = 'qwerer' # la funcion de to_b64
    return {"imagen_grises": imagen_64}