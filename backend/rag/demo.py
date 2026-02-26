import os
import tempfile
import whisper
import gradio as gr
from pytube import YouTube
from dotenv import load_dotenv

# LangChain imports
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Configuración Inicial
load_dotenv()
HUGGINGFACE_TOKEN = os.getenv('TOKEN_HUGFACE') # Usa el nombre exacto de tu .env

# Inicializar modelos de LLM
llm = HuggingFaceHub(
    repo_id='HuggingFaceH4/zephyr-7b-beta',
    task='text-generation',
    huggingfacehub_api_token=HUGGINGFACE_TOKEN,
    model_kwargs={
        'max_new_tokens': 512,
        'top_k': 30,
        'temperature': 0.1,
        'repetition_penalty': 1.03
    }
)
modelo_chat = ChatHuggingFace(llm=llm)
modelo_whisper = whisper.load_model('base')
vectorizador = HuggingFaceEmbeddings(model_name='sentence-transformers/all-roberta-large-v1')

# 2. Prompts y Parsers
def clean_parser(response: str) -> str:
    return response.split('<|assistant|>')[-1].strip()

plantilla = """Answer the question based on the context below. If you can't answer, reply "I don't know".
Context: {context}
Question: {question}"""

prompt = ChatPromptTemplate.from_template(plantilla)
prompt_traductor = ChatPromptTemplate.from_template("Translate the following text to {language}. Text: {answer}")
parser = StrOutputParser()

# 3. Funciones de Procesamiento
def procesar_video(url):
    try:
        # Descarga y Transcripción
        yt = YouTube(url)
        audio = yt.streams.filter(only_audio=True).first()
        
        with tempfile.TemporaryDirectory() as tmpdir:
            archivo_audio = audio.download(output_path=tmpdir)
            transcripcion = modelo_whisper.transcribe(archivo_audio, fp16=False)['text'].strip()
            
            txt_path = os.path.join("temp_transcription.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(transcripcion)
        
        # Segmentación e Indexación en Chroma
        loader = TextLoader(txt_path, encoding="utf-8")
        documento = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        docs = splitter.split_documents(documento)
        
        # Creamos la DB en memoria para esta sesión
        db = Chroma.from_documents(docs, vectorizador)
        return db, "Video procesado con éxito. ¡Ya puedes preguntar!"
    except Exception as e:
        return None, f"Error: {str(e)}"

def chat_func(pregunta, idioma, db_state):
    if db_state is None:
        return "Por favor, procesa un video de YouTube primero."
    
    # Recuperación
    contexto = db_state.similarity_search(pregunta, k=5)
    
    # Cadena de RAG
    cadena_rag = prompt | modelo_chat | parser
    
    # Cadena de Traducción
    cadena_completa = (
        {"answer": cadena_rag, "language": lambda x: idioma}
        | prompt_traductor
        | modelo_chat
        | parser
    )
    
    respuesta_sucia = cadena_completa.invoke({"context": contexto, "question": pregunta})
    return clean_parser(respuesta_sucia)

# 4. Interfaz Gradio
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📺 YouTube RAG Chat con Whisper y Zephyr")
    
    # Estado para guardar la base de datos de Chroma
    vector_db_state = gr.State()
    
    with gr.Row():
        with gr.Column():
            url_input = gr.Textbox(label="URL de YouTube", placeholder="https://www.youtube.com/watch?v=...")
            btn_procesar = gr.Button("Procesar Video", variant="primary")
            status_output = gr.Label(value="Esperando URL...")
        
        with gr.Column():
            idioma_input = gr.Dropdown(choices=["Spanish", "English", "French", "German"], value="Spanish", label="Idioma de respuesta")
            pregunta_input = gr.Textbox(label="Tu pregunta", placeholder="¿De qué trata el video?")
            btn_preguntar = gr.Button("Enviar Pregunta")
            respuesta_output = gr.Textbox(label="Respuesta", interactive=False)

    # Eventos
    btn_procesar.click(
        fn=procesar_video, 
        inputs=[url_input], 
        outputs=[vector_db_state, status_output]
    )
    
    btn_preguntar.click(
        fn=chat_func, 
        inputs=[pregunta_input, idioma_input, vector_db_state], 
        outputs=[respuesta_output]
    )

if __name__ == "__main__":
    demo.launch()