import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class BaseIntentHandler(AbstractRequestHandler):
    """Clase base con Template Method para handlers de intents."""

    def can_handle(self, handler_input):
        """Este método debe implementar la condición del intent específico"""
        raise NotImplementedError("Subclase debe implementar can_handle()")

    def handle(self, handler_input):
        """Template Method: flujo genérico de manejo de un intent"""
        try:
            # Obtener atributos persistentes
            attr = handler_input.attributes_manager.persistent_attributes

            # Preparar datos del intent específico
            datos = self.preparar_datos(handler_input, attr)

            # Ejecutar acción específica del intent
            speak_output = self.ejecutar_accion(handler_input, attr, datos)

            # Guardar cambios persistentes si aplica
            handler_input.attributes_manager.save_persistent_attributes()

            # Responder al usuario
            return handler_input.response_builder.speak(speak_output).ask(self.reprompt()).response

        except Exception as e:
            logger.error(f"Error en {self.__class__.__name__}: {e}", exc_info=True)
            return handler_input.response_builder.speak(self.error_message()).ask(self.reprompt()).response

    # --- Métodos abstractos que cada handler concreto debe implementar ---
    def preparar_datos(self, handler_input, attr):
        """Extraer datos específicos del intent"""
        raise NotImplementedError("Subclase debe implementar preparar_datos()")

    def ejecutar_accion(self, handler_input, attr, datos):
        """Realizar la acción específica del intent"""
        raise NotImplementedError("Subclase debe implementar ejecutar_accion()")

    def reprompt(self):
        """Texto genérico, puede sobreescribirse"""
        return "¿Deseas hacer otra cosa?"

    def error_message(self):
        """Mensaje de error"""
        return "Hubo un error procesando tu solicitud. Intenta de nuevo."
