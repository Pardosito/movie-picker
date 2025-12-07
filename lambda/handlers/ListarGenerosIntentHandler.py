import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from helpers.frases import PREGUNTAS_QUE_HACER, SALUDO_INICIAL, SALUDOS
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        try:
            attr = handler_input.attributes_manager.persistent_attributes

            logger.info(f"DEBUG - CONTENIDO DB: {attr}")

            saved_genres = attr.get("lista_generos")

            if saved_genres:
                logger.info(f"Usuario recurrente. Generos: {saved_genres}")
                saludo = get_random_phrase(SALUDOS)
                speak_output = saludo
            else:
                logger.info("Usuario nuevo (sin géneros guardados).")
                speak_output = SALUDO_INICIAL

            return (
                handler_input.response_builder.speak(speak_output)
                .ask(get_random_phrase(PREGUNTAS_QUE_HACER))
                .response
            )
        except Exception as e:
            logger.error(f"Error en LaunchRequest: {e}", exc_info=True)
            return (
                handler_input.response_builder.speak("Hubo un error cargando la skill")
                .ask("¿Qué deseas hacer?")
                .response
            )