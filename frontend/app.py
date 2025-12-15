import gradio as gr
import requests

API_BASE_URL = "http://localhost:7000"


# ======================
# NLP
# ======================

def analizar_sentimiento(user_id, texto):
    payload = {
        "user_id": user_id,
        "texto_usuario": texto
    }

    r = requests.post(
        f"{API_BASE_URL}/api/nlp/sentimiento_analisis",
        json=payload
    )

    if r.status_code != 200:
        return f"Error: {r.text}"

    return r.json()["resultado"]


def tokenizar_texto(user_id, texto, model):
    payload = {
        "user_id": user_id,
        "texto_usuario": texto,
        "model": model
    }

    r = requests.post(
        f"{API_BASE_URL}/api/nlp/tokenizar_texto",
        json=payload
    )

    if r.status_code != 200:
        return f"Error: {r.text}"

    return r.json()["resultado"]


# ======================
# IMÁGENES
# ======================

def procesar_imagen_local(user_id, path_imagen):
    payload = {
        "user_id": user_id,
        "path_imagen": path_imagen
    }

    r = requests.post(
        f"{API_BASE_URL}/api/imagenes/procesar-local",
        json=payload
    )

    if r.status_code != 200:
        return f"Error: {r.text}"

    data = r.json()
    return data["imagenes"]


# ======================
# INTERFAZ
# ======================

with gr.Blocks(title="API ML Frontend") as demo:
    gr.Markdown("# 🚀 Frontend ML (FastAPI + Gradio)")
    gr.Markdown("Interfaz visual para consumir servicios NLP e Imagenes")

    with gr.Tabs():

        # ---------- NLP ----------
        with gr.Tab("🧠 Análisis de Sentimiento"):
            user_id_1 = gr.Textbox(label="User ID", value="wilson")
            texto_1 = gr.Textbox(
                label="Texto",
                placeholder="Escribe un texto...",
                lines=4
            )
            salida_1 = gr.Textbox(label="Resultado")

            gr.Button("Analizar").click(
                analizar_sentimiento,
                inputs=[user_id_1, texto_1],
                outputs=salida_1
            )

        with gr.Tab("🧠 Tokenización"):
            user_id_2 = gr.Textbox(label="User ID", value="wilson")
            texto_2 = gr.Textbox(label="Texto", lines=4)

            model_2 = gr.Textbox(
                label="Modelo",
                value="default",
                placeholder="Ej: spacy, nltk, bert"
            )

            salida_2 = gr.Textbox(label="Resultado")

            gr.Button("Tokenizar").click(
                tokenizar_texto,
                inputs=[user_id_2, texto_2, model_2],
                outputs=salida_2
            )

        # ---------- IMÁGENES ----------
        with gr.Tab("🖼️ Procesar Imagen (ruta local)"):
            user_id_3 = gr.Textbox(label="User ID", value="wilson")
            path_img = gr.Textbox(
                label="Ruta local de la imagen",
                placeholder="C:/imagenes/foto.jpg o /data/img.png"
            )

            salida_3 = gr.JSON(label="Resultado")

            gr.Button("Procesar imagen").click(
                procesar_imagen_local,
                inputs=[user_id_3, path_img],
                outputs=salida_3
            )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
