import logging
import ask_sdk_core.utils as ask_utils
from handlers.BaseIntentHandler import BaseIntentHandler
from helpers.frases import ALGO_MAS, OPCIONES_MENU
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class EliminarGenerosIntentHandler(BaseIntentHandler):
    """Handler para eliminar géneros de la lista del usuario."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("EliminarGenerosIntent")(handler_input)

    def preparar_datos(self, handler_input, attr):
        """Extrae el slot 'genero' del intent"""
        genero = ask_utils.get_slot_value(handler_input, "genero")
        return {"genero": genero}

    def ejecutar_accion(self, handler_input, attr, datos):
        """Elimina el género de la lista si existe"""
        genero = datos["genero"]

        if not genero:
            return "Perfecto, ¿Qué género quieres eliminar?"

        if "lista_generos" not in attr or not attr["lista_generos"]:
            return f"Oops! Parece que tu lista está vacía o es la primera vez que vienes. Intenta añadir un género primero. {get_random_phrase(ALGO_MAS)}"

        if genero not in attr["lista_generos"]:
            return f"¡Vaya! El género {genero} no aparece en tu lista de favoritos, así que no puedo borrarlo. {get_random_phrase(ALGO_MAS)}"

        attr["lista_generos"].remove(genero)
        return f"Listones de colores, el género {genero} ha sido eliminado. {get_random_phrase(ALGO_MAS)}"

    def reprompt(self):
        return get_random_phrase(ALGO_MAS)

    def error_message(self):
        return "Hubo un problema eliminando el género."

    def handle(self, handler_input):
        """Override para asegurar guardado de persistent attributes"""
        try:
            attr = handler_input.attributes_manager.persistent_attributes

            logger.info(f"ANTES de eliminar - Atributos: {attr}")

            datos = self.preparar_datos(handler_input, attr)
            speak_output = self.ejecutar_accion(handler_input, attr, datos)

            logger.info(f"DESPUÉS de eliminar - Atributos: {attr}")

            handler_input.attributes_manager.persistent_attributes = attr
            handler_input.attributes_manager.save_persistent_attributes()

            logger.info("Atributos guardados exitosamente")

            return (
                handler_input.response_builder
                .speak(speak_output)
                .ask(self.reprompt())
                .response
            )

        except Exception as e:
            logger.error(f"Error en {self.__class__.__name__}: {e}", exc_info=True)
            return (
                handler_input.response_builder
                .speak(self.error_message())
                .ask(self.reprompt())
                .response
            )