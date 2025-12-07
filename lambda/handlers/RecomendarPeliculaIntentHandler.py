import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_model import Response
from helpers.api import get_movie_list

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class RecomendarPeliculaIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("RecomendarPeliculaIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        result = get_movie_list(handler_input)

        if isinstance(result, str):
            msgs = {
                "first_time": "No tienes géneros guardados. Dime qué te gusta primero.",
                "no_valid_ids_found": "No encontré coincidencias para tus géneros.",
                "no_movies_found": "No encontré películas con esos criterios.",
                "api_error": "Hubo un error de conexión con la base de datos."
            }
            speak_output = msgs.get(result, "Error desconocido.")

            return handler_input.response_builder.speak(speak_output).response

        movies_clean = []
        for m in result:
            movies_clean.append({
                "title": m.get("title"),
                "overview": m.get("overview")
            })

        session_attr["movie_queue"] = movies_clean
        session_attr["movie_index"] = 0

        logger.info(f"Guardada cola de peliculas. Tamaño: {len(movies_clean)}")

        first_movie = movies_clean[0]
        title = first_movie['title']
        overview = first_movie['overview']

        speak_output = f"Te recomiendo: {title}. {overview}. ¿Quieres ver la siguiente?"
        reprompt_text = "¿Quieres ver la siguiente opción?"

        logger.info("PREPARANDO RESPUESTA...")
        logger.info(f"Speak Output: {speak_output}")
        logger.info(f"Reprompt: {reprompt_text}")

        response = (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt_text)
            .set_should_end_session(False)
            .response
        )

        logger.info(f"SESSION END FLAG: {response.should_end_session}")

        return response