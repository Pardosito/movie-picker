from ask_sdk_core.dispatch_components import AbstractRequestHandler
import ask_sdk_core.utils as ask_utils
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ListarGenerosIntentHandler(AbstractRequestHandler):
    """Handler encargado de listar los géneros registrados en la base de datos.
    Para que funcione como se está planeado, solamente se tendrán registrados dos
    usuarios y tres géneros por cada uno.
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