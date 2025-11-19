from transformers import pipeline
from variables import TOKEN_HUGFACE, MODELO_BASE

tarea = 'text-classification'

MODELO_BASE='distilbert/distilbert-base-uncased-finetuned-sst-2-english'

clasificador = pipeline(task=tarea, model=MODELO_BASE)

def analisis_sentimiento(texto):
    return clasificador(texto)
