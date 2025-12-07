import logging

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from helpers.frases import ALGO_MAS
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AgregarGenerosIntentHandler(AbstractRequestHandler):
    """Handler encargado de agregar los géneros..."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AgregarGenerosIntent")(handler_input)

    def handle(self, handler_input):
        try:
            genero = ask_utils.get_slot_value(handler_input, "genero")
            attr = handler_input.attributes_manager.persistent_attributes

            if not genero:
                return (
                    handler_input.response_builder.speak(
                        "¡Perfecto! Vamos a agregar un género. ¿Cuál sería?"
                    )
                    .ask("Perfecto ¿Qué género quieres agregar?")
                    .response
                )

            if "lista_generos" not in attr:
                attr["lista_generos"] = []

            if genero not in attr["lista_generos"]:
                attr["lista_generos"].append(genero)
                speak_output = f"¡Listo! He agregado {genero} a tu lista. {get_random_phrase(ALGO_MAS)}"
            else:
                speak_output = f"El género {genero} ya estaba en tu lista. {get_random_phrase(ALGO_MAS)}"

            handler_input.attributes_manager.save_persistent_attributes()

            return (
                handler_input.response_builder.speak(speak_output)
                .ask(get_random_phrase(ALGO_MAS))
                .response
            )

        except Exception as e:
            logger.error(f"Error en AgregarGenerosIntent: {e}", exc_info=True)
            return (
                handler_input.response_builder.speak(
                    "Hubo un problema agregando el género. Intentemos de nuevo."
                )
                .ask("¿Qué género quieres agregar?")
                .response
            )
