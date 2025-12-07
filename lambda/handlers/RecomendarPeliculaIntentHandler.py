import logging
import ask_sdk_core.utils as ask_utils
from handlers.BaseIntentHandler import BaseIntentHandler
from helpers.api import get_movie_list

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RecomendarPeliculaIntentHandler(BaseIntentHandler):
    """Handler para recomendar películas basadas en géneros del usuario."""

    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RecomendarPeliculaIntent")(handler_input)

    def preparar_datos(self, handler_input, attr):
        """Obtiene la lista de películas de la API"""
        result = get_movie_list(handler_input)
        return {"result": result}

    def ejecutar_accion(self, handler_input, attr, datos):
        """Procesa las películas y guarda en sesión"""
        result = datos["result"]
        session_attr = handler_input.attributes_manager.session_attributes

        if isinstance(result, str):
            msgs = {
                "first_time": "No tienes géneros guardados. Dime qué te gusta primero.",
                "no_valid_ids_found": "No encontré coincidencias para tus géneros.",
                "no_movies_found": "No encontré películas con esos criterios.",
                "api_error": "Hubo un error de conexión con la base de datos."
            }
            return msgs.get(result, "Error desconocido.")

        movies_clean = [
            {"title": m.get("title"), "overview": m.get("overview")}
            for m in result
        ]

        session_attr["movie_queue"] = movies_clean
        session_attr["movie_index"] = 0

        logger.info(f"Guardada cola de películas. Tamaño: {len(movies_clean)}")

        first_movie = movies_clean[0]
        title = first_movie['title']
        overview = first_movie['overview']

        return f"Te recomiendo: {title}. {overview}. ¿Quieres ver la siguiente?"

    def reprompt(self):
        return "¿Quieres ver la siguiente opción?"

    def error_message(self):
        return "Hubo un problema obteniendo recomendaciones."

    def handle(self, handler_input):
        """Override para no guardar persistent_attributes y manejar should_end_session"""
        try:
            attr = handler_input.attributes_manager.persistent_attributes
            datos = self.preparar_datos(handler_input, attr)
            speak_output = self.ejecutar_accion(handler_input, attr, datos)

            return (
                handler_input.response_builder
                .speak(speak_output)
                .ask(self.reprompt())
                .set_should_end_session(False)
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