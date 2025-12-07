import logging
import ask_sdk_core.utils as ask_utils
from handlers.BaseIntentHandler import BaseIntentHandler
from helpers.frases import ALGO_MAS
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ListarGenerosIntentHandler(BaseIntentHandler):
    """Handler para listar los géneros favoritos del usuario."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ListarGenerosIntent")(handler_input)

    def preparar_datos(self, handler_input, attr):
        """No necesita datos del intent, solo de los atributos"""
        return {}

    def ejecutar_accion(self, handler_input, attr, datos):
        """Lista todos los géneros guardados del usuario"""
        saved_genres = attr.get("lista_generos", [])

        if not saved_genres:
            return f"Aún no tienes géneros favoritos guardados. ¿Quieres agregar algunos? {get_random_phrase(ALGO_MAS)}"

        if len(saved_genres) == 1:
            generos_texto = saved_genres[0]
        elif len(saved_genres) == 2:
            generos_texto = f"{saved_genres[0]} y {saved_genres[1]}"
        else:
            generos_texto = ", ".join(saved_genres[:-1]) + f" y {saved_genres[-1]}"

        return f"Tus géneros favoritos son: {generos_texto}. {get_random_phrase(ALGO_MAS)}"

    def reprompt(self):
        return get_random_phrase(ALGO_MAS)

    def error_message(self):
        return "Hubo un problema mostrando tus géneros."