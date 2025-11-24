# services/imagenes_opencv.py
import cv2
import base64

# ---- Lee imagen desde un path físico ----
def cargar_imagen_local(path: str):
    img = cv2.imread(path)
    if img is None:
        raise ValueError(f"No se pudo leer la imagen en el path → {path}")
    return img


# ======================
# Funciones de OpenCV
# ======================
def escala_grises(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def redimensionar(img, w=200, h=200):
    return cv2.resize(img, (w, h))

def rotar(img, grados=90):
    alto, ancho = img.shape[:2]
    centro = (ancho // 2, alto // 2)
    matriz = cv2.getRotationMatrix2D(centro, grados, 1.0)
    return cv2.warpAffine(img, matriz, (ancho, alto))

def invertir(img):
    return cv2.bitwise_not(img)

def desenfoque(img, k=15):
    return cv2.GaussianBlur(img, (k, k), 0)

def bordes(img):
    gris = escala_grises(img)
    return cv2.Canny(gris, 100, 200)


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

    return {
        #"original": to_b64(img),
        "gris": to_b64(escala_grises(img)),
        "invertida": to_b64(invertir(img)),
        "bordes": to_b64(bordes(img)),
        "rotada": to_b64(rotar(img, 30)),
        "redimensionada": to_b64(redimensionar(img, 200, 200))
    }
