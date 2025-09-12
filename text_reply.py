from dotenv import load_dotenv      # carga variables de entorno 
import os                           # libreria de sistema
from transformers import pipeline   # importamos desde la librería transformers el pipeline
from transformers import TextIteratorStreamer
import threading

load_dotenv()


# importamos el token desde el archivo .env
TOKEN_HUGFACE = os.getenv('TOKEN_HUGFACE')



# definimos la tarea y el modelo 
TAREA = 'text-generation'  
MODELO = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'

# iniciamos el modelo de texto
PIPELINE = pipeline(task=TAREA, model=MODELO, token=TOKEN_HUGFACE)



# iniciamos la variable prompt con el mensaje del sistema
PROMPT = '<|im_start|>system \n You are a friendly chatbot.<|im_end|>\n'


def update_context(contexto: str, user: bool = True) -> None:
    
    """
    Función para actualizar la conversación.
    
    Params:
    + contexto: string de la pregunta del usuario o de la respuesta del modelo.
    + user: booleano que nos indica si el usuario o el modelo que habla
    
    Return:
    No devueve nada, solo actualiza la variable global PROMPT
    """
    
    global PROMPT
    
    if user:
        PROMPT += f'\n<|im_start|>user\n{contexto}<|im_end|>\n<|im_start|>assistant\n'
        
    else:
        PROMPT += f'{contexto}<|im_end|>\n'
        
    return None


def chatbot(pregunta: str) -> str:
    
    """
    Función para llamar al modelo, recibe la pregunta y actualiza la conversación.
    
    Params:
    + pregunta: string con la pregunta del usuario
    
    Return:
    String con la respuesta del modelo
    """
    
    global PIPELINE, PROMPT
    
    
    # prompt de la conversacion 
    update_context(pregunta, user=True)
    
    
    # generamos la respuesta del chat
    respuesta = PIPELINE(text_inputs=PROMPT,
                         max_new_tokens=256, 
                         do_sample=True, 
                         temperature=0.2, 
                         top_k=50, 
                         top_p=0.95)
    
    print("Respuesta sin tratar:", respuesta)
    # formato string de la respuesta
    respuesta = respuesta[0]['generated_text'].split('assistant\n')[-1].strip()
    
    
    # actualiza la conversacion con la respuesta
    update_context(respuesta, user=False)
    
    
    return respuesta


def chatbot_stream(pregunta: str) -> str:
    """
    Función para llamar al modelo en streaming, recibe la pregunta y actualiza la conversación.
    Imprime los tokens en tiempo real y devuelve la respuesta completa.
    """

    global PIPELINE, PROMPT

    # prompt de la conversacion 
    update_context(pregunta, user=True)

    # streamer para recibir tokens en vivo
    streamer = TextIteratorStreamer(
        PIPELINE.tokenizer,
        skip_prompt=True,
        skip_special_tokens=True
    )

    # preparamos inputs
    inputs = PIPELINE.tokenizer(PROMPT, return_tensors="pt").to(PIPELINE.model.device)
    gen_kwargs = dict(
        **inputs,
        max_new_tokens=256,
        do_sample=True,
        temperature=0.2,
        top_k=50,
        top_p=0.95,
        streamer=streamer
    )

    # lanzamos la generación en un hilo
    thread = threading.Thread(target=PIPELINE.model.generate, kwargs=gen_kwargs)
    thread.start()

    # tokens en tiempo real
    respuesta_tokens = []
    for token in streamer:
        print(token, end="", flush=True)  # imprime en vivo
        respuesta_tokens.append(token)

    # unimos todo el texto generado
    respuesta = "".join(respuesta_tokens).strip()

    # actualiza la conversacion con la respuesta final
    update_context(respuesta, user=False)

    return respuesta

#print(chatbot('Hola, como estas?'))

#print(chatbot_stream('Hola, en que me puedes ayudar?'))