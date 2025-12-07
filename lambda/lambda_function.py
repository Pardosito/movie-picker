import logging
import os
import boto3
import ask_sdk_core.utils as ask_utils
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler, AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

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
from handlers.SiguientePaginaIntentHandler import SiguientePeliculaIntentHandler
from handlers.SiguientePaginaIntentHandler import YesIntentHandler
from handlers.SiguientePaginaIntentHandler import NoIntentHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
dynamodb_adapter = DynamoDbAdapter(table_name=ddb_table_name, create_table=False, dynamodb_resource=ddb_resource)

sb = CustomSkillBuilder(persistence_adapter=dynamodb_adapter)

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(AgregarGenerosIntentHandler())
sb.add_request_handler(EliminarGenerosIntentHandler())
sb.add_request_handler(ListarGenerosIntentHandler())
sb.add_request_handler(MostrarOpcionesIntentHandler())
sb.add_request_handler(RecomendarPeliculaIntentHandler())
sb.add_request_handler(SiguientePeliculaIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())

sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()