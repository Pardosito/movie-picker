import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

from helpers.frases import OPCIONES_MENU
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MostrarOpcionesIntentHandler(AbstractRequestHandler):
    """Handler para MostrarOpcionesIntent (aún no implementado)."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MostrarOpcionesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        try:
            menu = get_random_phrase(OPCIONES_MENU)
            speak_output = menu
            logger.info("Se llamó a MostrarOpcionesIntentHandler")

            return (
                handler_input.response_builder.speak(speak_output)
                .ask("¿Qué otra cosa puedo hacer?")
                .response
            )

        except Exception as e:
            logger.error(f"Error en MostrarOpcionesIntent: {e}", exc_info=True)
            return (
                handler_input.response_builder.speak(
                    "Hubo un problema mostrando el menú."
                )
                .ask("¿Qué deseas hacer?")
                .response
            )