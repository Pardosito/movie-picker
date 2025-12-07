import logging
import ask_sdk_core.utils as ask_utils
from handlers.BaseIntentHandler import BaseIntentHandler
from helpers.api import get_movie_of_the_day

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PeliculaDiaIntentHandler(BaseIntentHandler):
    """Handler para obtener la película del día."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PeliculaDiaIntent")(handler_input)

    def preparar_datos(self, handler_input, attr):
        """Obtiene la película del día desde la API"""
        movie = get_movie_of_the_day()
        return {"movie": movie}

    def ejecutar_accion(self, handler_input, attr, datos):
        """Procesa la película del día"""
        movie = datos["movie"]

        if isinstance(movie, str):
            msgs = {
                "no_movies_found": "No encontré la película del día.",
                "api_error": "Hubo un error de conexión con la base de datos."
            }
            return msgs.get(movie, "Error desconocido.")

        title = movie.get('title', 'Sin título')
        overview = movie.get('overview', 'Sin descripción')

        logger.info(f"Película del día: {title}")

        return f"La película del día es: {title}. {overview}."

    def reprompt(self):
        return "¿Qué más puedo hacer por ti?"

    def error_message(self):
        return "Hubo un problema obteniendo la película del día."

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