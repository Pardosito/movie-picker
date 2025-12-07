import logging
import ask_sdk_core.utils as ask_utils
from handlers.BaseIntentHandler import BaseIntentHandler
from helpers.api import spin_the_wheel

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SpinTheWheelIntentHandler(BaseIntentHandler):
    """Handler para la ruleta de películas."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SpinTheWheelIntent")(handler_input)

    def preparar_datos(self, handler_input, attr):
        """Obtiene una película aleatoria de la ruleta"""
        result = spin_the_wheel(handler_input)
        return {"movie": result}

    def ejecutar_accion(self, handler_input, attr, datos):
        """Procesa el resultado de la ruleta"""
        movie = datos["movie"]

        if isinstance(movie, str):
            msgs = {
                "first_time": "No tienes géneros guardados. Agrega algunos primero.",
                "no_valid_ids_found": "No encontré coincidencias para tus géneros.",
                "no_movies_found": "No encontré películas con esos criterios.",
                "api_error": "Hubo un error de conexión."
            }
            return msgs.get(movie, "Error desconocido.")

        title = movie.get('title', 'Sin título')
        overview = movie.get('overview', 'Sin descripción')

        logger.info(f"Película de la ruleta: {title}")

        return f"Redoble de tambores por favor, la película que salió fue... {title}. {overview}"

    def reprompt(self):
        return "¿Qué más puedo hacer por ti?"

    def error_message(self):
        return "Hubo un problema con la ruleta de películas."

    def handle(self, handler_input):
        """Override para no guardar persistent_attributes"""
        try:
            attr = handler_input.attributes_manager.persistent_attributes
            datos = self.preparar_datos(handler_input, attr)
            speak_output = self.ejecutar_accion(handler_input, attr, datos)

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