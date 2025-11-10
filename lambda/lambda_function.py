# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


from handlers.AgregarGenerosIntentHandler import AgregarGenerosIntentHandler
from handlers.CancelOrStopIntentHandler import CancelOrStopIntentHandler
from handlers.CatchAllExceptionHandler import CatchAllExceptionHandler
from handlers.EliminarGenerosIntentHandler import EliminarGenerosIntentHandler
from handlers.FallbackIntentHandler import FallbackIntentHandler
from handlers.HelpIntentHandler import HelpIntentHandler
from handlers.IntentReflectorHandler import IntentReflectorHandler
from handlers.LaunchRequestHandler import LaunchRequestHandler
from handlers.ListarGenerosIntentHandler import ListarGenerosIntentHandler
from handlers.MostrarOpcionesIntentHandler import MostrarOpcionesIntentHandler
from handlers.RecomendarPeliculaIntentHandler import RecomendarPeliculaIntentHandler
from handlers.SessionEndedRequestHandler import SessionEndedRequestHandler
from handlers.SiguientePaginaIntentHandler import SiguientePaginaIntentHandler

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(AgregarGenerosIntentHandler())
sb.add_request_handler(EliminarGenerosIntentHandler())
sb.add_request_handler(ListarGenerosIntentHandler())
sb.add_request_handler(MostrarOpcionesIntentHandler())
sb.add_request_handler(RecomendarPeliculaIntentHandler())
sb.add_request_handler(SiguientePaginaIntentHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()