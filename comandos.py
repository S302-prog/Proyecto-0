import re

from lenguaje import DIRECCIONES
from lenguaje import ORIENTACIONES
from lenguaje import ROTACIONES
from lenguaje import CONSTANTES
from lenguaje import OBJETOS

"""
Toca crear lista que guarde las variables que se creen con defvar ya que estas también pueden ser n y con esa 
lista creada seria poner un or en lo try-except en
"""


def dividir_comandos(text: str) -> list:
    """
    Divide el texto dado en una lista de comandos separados.
    El texto debe ser un bloque de profundidad 1

    Parameters:
        text (str): El texto a dividir.

    Returns:
        list: Una lista de comandos separados.
    """

    lista = re.split(r"[,()\s]", text)

    return [elem for elem in lista if elem]


# ======================================
# Chequeo de todos los posibles comandos
# ======================================

def chequeo_defvar(text: str, variables: list) -> bool:
    """
    Verifica si el comando de declaración de variable es válido.

    :param text: El comando a verificar.
    :param variables: La lista de variables existentes.
    :return: Verdadero si el comando es válido, de lo contrario Falso.
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 3 or tokens[0] != "defvar":
        return False

    # El nombre no puede iniciar con un número
    if tokens[1][0].isnumeric():
        return False

    # Ya existe una variable con ese nombre
    if tokens[1] in variables or tokens[1] in CONSTANTES:
        return False

    return tokens[2].isnumeric() or tokens[2] in CONSTANTES or tokens[2] in variables


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


def chequeo_pick_put(text: str):
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

    return tokens[2].isnumeric() or tokens[2] in CONSTANTES


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

    if not tokens[1].isnumeric() or tokens[1] not in variables:
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

    if tokens[1] not in variables or not tokens[1].isnumeric():
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
