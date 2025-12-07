from ask_sdk_core.utils import is_intent_name
from handlers.base_intent_handler import BaseIntentHandler
from helpers.frases import ALGO_MAS
from helpers.utils import get_random_phrase
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class AgregarGenerosIntentHandler(BaseIntentHandler):

    def can_handle(self, handler_input):
        return is_intent_name("AgregarGenerosIntent")(handler_input)

    def preparar_datos(self, handler_input, attr):
        # Obtenemos el slot 'genero'
        genero = handler_input.request_envelope.request.intent.slots.get("genero")
        if genero:
            genero = genero.value
        return {"genero": genero}

    def ejecutar_accion(self, handler_input, attr, datos):
        genero = datos["genero"]

        if not genero:
            return "¡Perfecto! Vamos a agregar un género. ¿Cuál sería?"

        if "lista_generos" not in attr:
            attr["lista_generos"] = []

        if genero not in attr["lista_generos"]:
            attr["lista_generos"].append(genero)
            speak_output = f"¡Listo! He agregado {genero} a tu lista. {ALGO_MAS}"
        else:
            speak_output = f"El género {genero} ya estaba en tu lista. {ALGO_MAS}"

        return speak_output

    def reprompt(self):
        return get_random_phrase(ALGO_MAS)
