from ask_sdk_core.dispatch_components import AbstractRequestHandler
import ask_sdk_core.utils as ask_utils
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class MostrarOpcionesIntentHandler(AbstractRequestHandler):
    """Handler encargado de mostrar todas las recomendaciones que haya
    hecho el programa.
    """
    # BOILER PLATE CODE, FALTA EDITAR
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )