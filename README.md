# Movie Picker - Skill de Alexa

**Movie Picker** es una skill de Alexa diseñada para ayudar a los usuarios a elegir películas de forma rápida, imparcial y divertida, basándose en sus géneros favoritos o mediante recomendaciones especiales como "Recomendación del día" o aleatoria. Su objetivo es reducir el tiempo de búsqueda y facilitar la decisión sin debates ni dudas.

## Tabla de Contenidos
1. [Características](#características)
2. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
3. [Patrones de Diseño Implementados](#patrones-de-diseño-implementados)
4. [Instalación](#instalación)
5. [Uso](#uso)
6. [Handlers](#handlers)
7. [Estructura de Archivos](#estructura-de-archivos)
8. [Dependencias](#dependencias)
9. [Autores](#autores)

## Características

- Agregar, listar y eliminar géneros favoritos.
- Obtener recomendaciones de películas basadas en los géneros del usuario.
- Recomendaciones del día o aleatorias si no hay géneros seleccionados.
- Manejo de errores con mensajes amigables.
- Persistencia de datos usando **DynamoDB**.
- Interacción natural mediante reprompts y confirmaciones.

## Arquitectura del Proyecto

El proyecto se organiza en tres capas principales:

1. **Lambda Function (`lambda_function.py`)**: Punto de entrada de la skill que configura los handlers y la persistencia con DynamoDB.
2. **Handlers (`/handlers`)**: Controladores de intents de Alexa, cada uno encargado de manejar una acción específica.
3. **Helpers (`/helpers`)**: Funciones auxiliares y estrategias de recomendación, incluyendo la comunicación con la API de películas y gestión de frases.

## Patrones de Diseño Implementados

1. **Template Method**: Cada handler sigue un flujo base de ejecución (validar, procesar, responder), garantizando consistencia en la interacción.
2. **Strategy**: La recomendación de películas se abstrae en estrategias:
    - `PorGeneroStrategy`: Recomienda según los géneros del usuario.
    - `AleatoriaStrategy`: Recomendación aleatoria si no hay géneros.
    - `DelDiaStrategy`: Recomendación del día.
   Esto permite cambiar el comportamiento sin modificar el handler principal.
3. **Singleton**: Se aplica en la configuración de DynamoDB para asegurar una única instancia de persistencia durante toda la ejecución de la skill.

## Diagramas C4's

Existe una carpeta llamada **DiagramsC4** en el que se encuentran los diagramas pertinentes que detallan el contexto del proyecto y a continuación una breve explicación de que hacen
1. **Movie Picker Context**: Este el el primer diagrama, aquí explicamos los actores que interactuan en la ejecución para el proyecto
2. **Movie Picker Containers Alexa Skill**: El segundo diagrama se muestran los sistemas que actúan en una interacción básica en la que nuestra Alexa Skill es llamada (esto por medio de contenedores)
3. **Movie Picker Components Alexa Skill**: Finalmente en archivo de MermaidChart se explica una comunicación interna de los componentes del sistema en la Skill Movie-Picker


## Instalación

1. Clonar el repositorio:
```bash
git clone <URL_DEL_REPOSITORIO>
cd Cinema
