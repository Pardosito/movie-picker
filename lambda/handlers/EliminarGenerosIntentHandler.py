import logging

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.dialog import ElicitSlotDirective
from helpers.frases import ALGO_MAS, OPCIONES_MENU
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class EliminarGenerosIntentHandler(AbstractRequestHandler):
    """Handler para EliminarGenerosIntent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("EliminarGenerosIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        try:
            genero = ask_utils.get_slot_value(handler_input, "genero")
            attr = handler_input.attributes_manager.persistent_attributes

            if not genero:
                current_intent = handler_input.request_envelope.request.intent

                speak_output = "Perfecto, ¿Qué género quieres eliminar?"

                return (
                    handler_input.response_builder.speak(speak_output)
                    .ask(speak_output)
                    .add_directive(
                        ElicitSlotDirective(
                            updated_intent=current_intent, slot_to_elicit="genero"
                        )
                    )
                    .response
                )

            speak_output = ""

            if "lista_generos" not in attr or not attr["lista_generos"]:
                speak_output = f"Oops! Parece que tu lista está vacía o es la primera vez que vienes. Intenta añadir un género primero. {get_random_phrase(ALGO_MAS)}"
                return (
                    handler_input.response_builder.speak(speak_output)
                    .ask(get_random_phrase(OPCIONES_MENU))
                    .response
                )

            elif genero not in attr["lista_generos"]:
                speak_output = f"¡Vaya! El género {genero} no aparece en tu lista de favoritos, así que no puedo borrarlo. {get_random_phrase(ALGO_MAS)}"
                return (
                    handler_input.response_builder.speak(speak_output)
                    .ask(get_random_phrase(ALGO_MAS))
                    .response
                )

            else:
                attr["lista_generos"].remove(genero)
                handler_input.attributes_manager.save_persistent_attributes()

                speak_output = f"Listones de colores, el género {genero} ha sido eliminado. {get_random_phrase(ALGO_MAS)}"
                return (
                    handler_input.response_builder.speak(speak_output)
                    .ask(get_random_phrase(ALGO_MAS))
                    .response
                )

        except Exception as e:
            logger.error(f"Error en EliminarGeneroIntent: {e}", exc_info=True)
            return (
                handler_input.response_builder.speak(
                    "Hubo un problema eliminando el género."
                )
                .ask("¿Qué deseas hacer ahora?")
                .response
            )
