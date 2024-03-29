import re

from lenguaje import DIRECCIONES
from lenguaje import ORIENTACIONES
from lenguaje import ROTACIONES
from lenguaje import CONSTANTES
from lenguaje import OBJETOS


def dividir_comandos(text: str) -> list[str]:
    """
    Divide el texto dado en una lista de comandos separados.
    El texto debe ser un bloque de profundidad 1

    Parameters:
        text (str): El texto a dividir.

    Returns:
        list: Una lista de comandos separados.
    """

    lista = re.split(r"[,()\s]", text)

    prev = [elem for elem in lista if elem]

    if ":" in prev:
        existe = prev.index(":")

        if existe < len(prev) - 1:
            siguiente = prev[existe + 1]
            prev.pop(existe)
            prev.pop(existe)
            prev.insert(existe, f":{siguiente}")

    
    if "?" not in prev:
        return prev

    existe = prev.index("?")

    if existe != 0:
        anterior = prev[existe - 1]
        prev.pop(existe - 1)
        prev.pop(existe - 1)
        prev.insert(existe - 1, f"{anterior}?")

    return prev

# ======================================
# Chequeo de todos los posibles comandos
# ======================================

def chequeo_defvar(text: str, variables: list) -> str | None:
    """
    Verifica si el comando de declaración de variable es válido.

    :param text: El comando a verificar.
    :param variables: La lista de variables existentes.
    :return: El nombre de la variable si el comando es válido, de lo contrario None.
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 3 or tokens[0] != "defvar":
        return None

    # El nombre no puede iniciar con un número
    if tokens[1][0].isnumeric() or not tokens[1].isalnum():
        return None

    # Ya existe una variable con ese nombre
    if tokens[1] in variables or tokens[1] in CONSTANTES:
        return None

    if tokens[2].isnumeric() or tokens[2] in CONSTANTES or tokens[2] in variables:
        return tokens[1]

    return None


def chequeo_asignacion(text: str, variables: list) -> bool:
    """
    Verifica si el comando de asignación es válido.

    :param text: El comando a verificar.
    :param variables: La lista de variables existentes.
    :return: Verdadero si el comando es válido, de lo contrario Falso.
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 3 or tokens[0] != "=":
        return False

    if tokens[1] not in variables:
        return False

    return tokens[2].isnumeric() or tokens[2] in CONSTANTES or tokens[2] in variables


def chequeo_move_skip(text: str, variables: list) -> bool:
    """
    Verifica si el comando es "move" o "skip", además verifica si es válido.

    :param text: El comando a verificar.
    :param variables: La lista de variables existentes.
    :return: Verdadero si el comando es válido, de lo contrario Falso.
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 2 or tokens[0] not in ["move", "skip"]:
        return False

    return tokens[1].isnumeric() or tokens[1] in variables


def chequeo_rotacion(text: str) -> bool:
    """
    Verifica si el comando de rotación ("face" o "turn") es válido.

    :param text: El comando a verificar.
    :return: Verdadero si el comando es válido, de lo contrario Falso.
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 2 or tokens[0] not in ["turn", "face"]:
        return False

    opciones = ROTACIONES if tokens[0] == "turn" else ORIENTACIONES

    return tokens[1] in opciones


def chequeo_pick_put(text: str, variables: list[str]):
    """
    Verifica si el comando de interacción dado es válido.
    Args:
       text:El comando de interacción a ser verificado.
    Returns:
       bool:Verdadero si el comando de interacción es válido, Falso en caso contrario.
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 3 or tokens[0] not in ["put", "pick"] or tokens[1] not in OBJETOS:
        return False

    return tokens[2].isnumeric() or tokens[2] in CONSTANTES or tokens[2] in variables


def chequeo_movimiento_direccion(text: str, variables: list) -> bool:
    """
    Verifica si el comando de movimiento es válido.

    :param text: El comando a verificar.
    :param variables: La lista de variables existentes.
    :return: Verdadero si el comando es válido, de lo contrario Falso.
    """
    tokens = dividir_comandos(text)
    if len(tokens) != 3 or tokens[0] != "move-dir":
        return False

    if (not tokens[1].isnumeric()) and (tokens[1] not in variables):
        return False

    return tokens[2] in DIRECCIONES


def chequeo_lista_direcciones(text: str) -> bool:
    """
    Verifica si el comando de movimiento es válido.

    :param text: El comando a verificar.
    :return: Verdadero si el comando es válido, de lo contrario Falso.
    """
    tokens = dividir_comandos(text)
    if len(tokens) < 2 or tokens[0] != "run-dirs":
        return False

    return all(map(lambda _dir: _dir in DIRECCIONES, tokens[1:]))


def chequeo_encarar_mover(text: str, variables: list) -> bool:
    """
    Verifica si el comando de encarar y mover es válido.

    :param text: El comando a verificar.
    :param variables: La lista de variables existentes.
    :return: Verdadero si el comando es válido, de lo contrario Falso.
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 3 or tokens[0] != "move-face":
        return False

    if tokens[1] not in variables and not tokens[1].isnumeric():
        return False

    return tokens[2] in ORIENTACIONES


def rev_null(text: str):
    """
    Verifica si el comando nulo sea válido.

    :param text: El comando a verificar.
    :return: Verdadero si el comando es válido, de lo contrario Falso.
    """
    tokens = dividir_comandos(text)

    return len(tokens) == 1 and tokens[0] == "null"


def chequeo_ejecucion_funcion(text: str, variables: list[str], funciones: list[tuple[str, int]]) -> bool:
    tokens = dividir_comandos(text)

    disponibles = dict(funciones)

    if len(tokens) == 0 or tokens[0] not in disponibles:
        return False

    return len(tokens) == disponibles[tokens[0]] + 1


# No se verifica defvar por su condicion especial
def es_comando_valido(texto: str, variables: list, funciones: list) -> bool:
    return (chequeo_asignacion(texto, variables) or 
            chequeo_move_skip(texto, variables) or 
            chequeo_rotacion(texto) or 
            chequeo_pick_put(texto, variables) or 
            chequeo_movimiento_direccion(texto, variables) or 
            chequeo_lista_direcciones(texto) or 
            chequeo_encarar_mover(texto, variables) or 
            rev_null(texto) or 
            chequeo_ejecucion_funcion(texto, variables, funciones))
