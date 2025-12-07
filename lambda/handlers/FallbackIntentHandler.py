import logging

import ask_sdk_core.utils as ask_utils
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, no estoy seguirita. Puedes decir ayuda para conocer las opciones. ¿Qué te gustaría hacer?"
        reprompt = "Oyoyoi no capté eso. ¿Con que te puedo ayudar?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response
