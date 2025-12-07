import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
import ask_sdk_core.utils as ask_utils
from helpers.api import get_next_movie_response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class SiguientePeliculaIntentHandler(AbstractRequestHandler):
    """Handler for 'Dame otra', 'Siguiente', etc."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("SiguientePeliculaIntent")(handler_input)

    def handle(self, handler_input):
        speak_output, reprompt = get_next_movie_response(handler_input)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(reprompt)
            .response
        )

class YesIntentHandler(AbstractRequestHandler):
    """Handler for 'Sí'."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        session_attr = handler_input.attributes_manager.session_attributes

        if session_attr.get("movie_queue"):
            speak_output, reprompt = get_next_movie_response(handler_input)

            return (
                handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
            )
        else:
            return (
                handler_input.response_builder
                .speak("¿En qué más te puedo ayudar?")
                .ask("Dime qué necesitas.")
                .response
            )

class NoIntentHandler(AbstractRequestHandler):
    """Handler for 'No'."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        speak_output = "Está bien. ¡Disfruta tu película!"

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_should_end_session(True)
            .response
        )