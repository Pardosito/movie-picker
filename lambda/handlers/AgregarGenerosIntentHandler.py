import logging
import ask_sdk_core.utils as ask_utils
from handlers.BaseIntentHandler import BaseIntentHandler
from helpers.frases import ALGO_MAS
from helpers.utils import get_random_phrase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class AgregarGenerosIntentHandler(BaseIntentHandler):
    """Handler encargado de agregar géneros a la lista del usuario."""

    def can_handle(self, handler_input):
        resultado = ask_utils.is_intent_name("AgregarGenerosIntent")(handler_input)
        logger.info(f"AgregarGenerosIntentHandler.can_handle() = {resultado}")
        return resultado

    def preparar_datos(self, handler_input, attr):
        """Extrae el slot 'genero' del intent"""
        genero = ask_utils.get_slot_value(handler_input, "genero")
        logger.info(f"Slot 'genero' capturado: {genero}")
        return {"genero": genero}

    def ejecutar_accion(self, handler_input, attr, datos):
        """Agrega el género a la lista de géneros del usuario"""
        genero = datos["genero"]
        logger.info(f"Ejecutando acción con género: {genero}")

        if not genero:
            return "¡Perfecto! Vamos a agregar un género. ¿Cuál sería?"

        if "lista_generos" not in attr:
            attr["lista_generos"] = []

        if genero not in attr["lista_generos"]:
            attr["lista_generos"].append(genero)
            return f"¡Listo! He agregado {genero} a tu lista. {get_random_phrase(ALGO_MAS)}"
        else:
            return f"El género {genero} ya estaba en tu lista. {get_random_phrase(ALGO_MAS)}"

    def reprompt(self):
        return get_random_phrase(ALGO_MAS)

    def error_message(self):
        return "Hubo un problema agregando el género. Intentemos de nuevo."

    def handle(self, handler_input):
        """Override para asegurar guardado de persistent attributes"""
        logger.info("===== ENTRANDO A AgregarGenerosIntentHandler.handle() =====")
        try:
            attr = handler_input.attributes_manager.persistent_attributes

            logger.info(f"ANTES de agregar - Atributos: {attr}")

            datos = self.preparar_datos(handler_input, attr)

            speak_output = self.ejecutar_accion(handler_input, attr, datos)

            logger.info(f"DESPUÉS de agregar - Atributos: {attr}")

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