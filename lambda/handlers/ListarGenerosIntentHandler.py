import logging

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from helpers.frases import ALGO_MAS
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ListarGenerosIntentHandler(AbstractRequestHandler):
    """Handler para ListarGenerosIntent (aún no implementado)."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ListarGenerosIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        try:
            attr = handler_input.attributes_manager.persistent_attributes

            if "lista_generos" not in attr:
                speak_output = "¡Ajá! ¿No será esta la primera vez que nos visitas? Añade un género primero antes de listarlos"
                logger.info("Usuario nuevo intentó listar géneros con lista vacía")
                return (
                    handler_input.response_builder.speak(speak_output)
                    .ask(get_random_phrase(ALGO_MAS))
                    .response
                )

            elif attr["lista_generos"] is None:
                speak_output = "Hmmm, de momento no tienes géneros añadidos, agrega uno para poder listarlos."
                logger.info("Usuario recurrente intentó listar géneros con lista vacía")

            else:
                speak_output = (
                    f"Mira, estos son tus géneros guardados: {attr['lista_generos']}"
                )
                return (
                    handler_input.response_builder.speak(speak_output)
                    .ask(get_random_phrase(ALGO_MAS))
                    .response
                )

            return (
                handler_input.response_builder.speak(speak_output)
                .ask("¿Qué otra cosa puedo hacer?")
                .response
            )

        except Exception as e:
            logger.error(f"Error en ListarGenerosIntent: {e}", exc_info=True)
            return (
                handler_input.response_builder.speak(
                    "Hubo un problema listando los géneros."
                )
                .ask("¿Qué deseas hacer?")
                .response
            )
