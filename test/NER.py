from ipymarkup import show_span_ascii_markup, show_span_line_markup
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import traceback
import logging
from helpers import _to_python

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("NER")

tarea = "ner"
MODELO_NER = "Clinical-AI-Apollo/Medical-NER"


tokenizador = AutoTokenizer.from_pretrained(MODELO_NER)
modelo_ner = AutoModelForTokenClassification.from_pretrained(MODELO_NER)
ner_pipe = pipeline(
    task=tarea,
    model=modelo_ner,
    tokenizer=tokenizador,
    aggregation_strategy="simple"
)



def ner_shows(texto: str):
    """
    Ejecuta NER sobre el texto.
    Devuelve siempre un dict con éxito o error.
    """
    if ner_pipe is None:
        return {
            "ok": False,
            "error": "El modelo no está inicializado correctamente.",
            "trace": "Revisa los logs para más detalle"
        }

    if not isinstance(texto, str) or not texto.strip():
        return {
            "ok": False,
            "error": "El parámetro 'texto' debe ser un string no vacío."
        }

    try:
        result = ner_pipe(texto)
        raw = ner_pipe(texto)
        return {
            "ok": True,
            "result": _to_python(raw)
        }
    except Exception as e:
        logger.error("❌ Error ejecutando NER")
        logger.error(traceback.format_exc())
        return {
            "ok": False,
            "error": str(e),
            "trace": traceback.format_exc()
        }
