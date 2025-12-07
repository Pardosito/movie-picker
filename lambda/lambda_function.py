import logging
import os
import boto3
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_dynamodb.adapter import DynamoDbAdapter

# Importar handlers
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
from handlers.SiguientePeliculaIntentHandler import (
    SiguientePeliculaIntentHandler,
    YesIntentHandler,
    NoIntentHandler
)
from handlers.SpinTheWheelIntentHandler import SpinTheWheelIntentHandler
from handlers.PeliculaDiaIntentHandler import PeliculaDiaIntentHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# =========================
# Singleton para DynamoDB
# =========================
class DynamoDBSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            logger.info("Creando la instancia única de DynamoDbAdapter...")
            ddb_region = os.environ.get('DYNAMODB_PERSISTENCE_REGION')
            ddb_table_name = os.environ.get('DYNAMODB_PERSISTENCE_TABLE_NAME')
            ddb_resource = boto3.resource('dynamodb', region_name=ddb_region)
            cls._instance = DynamoDbAdapter(
                table_name=ddb_table_name,
                create_table=False,
                dynamodb_resource=ddb_resource
            )
        return cls._instance


dynamodb_adapter = DynamoDBSingleton()


# =========================
# Skill Builder
# =========================
sb = CustomSkillBuilder(persistence_adapter=dynamodb_adapter)

# Handlers principales
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(FallbackIntentHandler())

# Handlers de géneros
sb.add_request_handler(AgregarGenerosIntentHandler())
sb.add_request_handler(EliminarGenerosIntentHandler())
sb.add_request_handler(ListarGenerosIntentHandler())

# Handlers de películas
sb.add_request_handler(RecomendarPeliculaIntentHandler())
sb.add_request_handler(PeliculaDiaIntentHandler())
sb.add_request_handler(SpinTheWheelIntentHandler())
sb.add_request_handler(SiguientePeliculaIntentHandler())

# Handlers de navegación
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())

# Handler de opciones
sb.add_request_handler(MostrarOpcionesIntentHandler())

# Handlers de último recurso
sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()