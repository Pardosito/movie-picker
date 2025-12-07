import logging

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from helpers.frases import OPCIONES_MENU, PREGUNTAS_QUE_HACER, SALUDO_INICIAL, SALUDOS
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        try:
            # type: (HandlerInput) -> Response
            attr = handler_input.attributes_manager.persistent_attributes
            if attr["lista_generos"]:
                saludo_inicial = SALUDO_INICIAL
                speak_output = saludo_inicial
            else:
                saludo = get_random_phrase(SALUDOS)
                speak_output = saludo

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
