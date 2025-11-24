from transformers import AutoTokenizer, AutoModelForSequenceClassification
from variables import MODELO_BASE

tokenizador = AutoTokenizer.from_pretrained(MODELO_BASE)

#frase = 'me gusta el aprendizaje'
#vector = tokenizador(frase, return_tensors='pt')

def tokenizar_texto(texto):
    return tokenizador(texto,  return_tensors='pt')
