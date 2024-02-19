from typing import Callable
from comandos import dividir_comandos
from bloques import Resultado, obtener_bloques, solo_un_bloque, validar_estructura_bloque
from lenguaje import CONDICIONES, CONSTANTES, ORIENTACIONES, OBJETOS, COMANDOS, RESERVADAS

def chequeo_condicion(text: str, variables: list) -> bool:
    partes = dividir_comandos(text.strip())

    if len(partes) == 0:
        return False

    if partes[0] not in CONDICIONES:
        return False

    if partes[0] == "not":
        bloques = obtener_bloques(text)
        if bloques is None or len(bloques) != 1:
            return False
        return chequeo_condicion(bloques[0], variables)

    if partes[0] == "facing?":
        if len(partes) != 2:
            return False
        return partes[1] in ORIENTACIONES

    if partes[0] == "blocked?":
        return len(partes) == 1

    if partes[0] in ["can-put?", "can-pick?"]:
        if len(partes) != 3:
            return False

        if partes[2] not in OBJETOS:
            return False

        return partes[2].isnumeric() or partes[2] in CONSTANTES or partes[2] in variables

    if partes[0] == "can-move?":
        if len(partes) != 2:
            return False

        return partes[1] in ORIENTACIONES

    if partes[0] == "iszero?":
        if len(partes) != 2:
            return False

        return partes[1].isnumeric() or partes[1] in CONSTANTES or partes[1] in variables

    return False


def chequeo_if(text: str, variables: list, funciones: list, func_validar_bloque: Callable[[str, list[str], list[tuple[str, int]], bool], Resultado], es_funcion = False) -> bool:
    comandos = dividir_comandos(text)

    if len(comandos) < 1 or comandos[0] != "if":
        return False

    bloques = obtener_bloques(text.strip())
    if bloques is None:
        return False

    if len(bloques) != 3 and len(bloques) != 2:
        return False

    condicion_valida = chequeo_condicion(bloques[0], variables)
    then = func_validar_bloque(bloques[1], variables, funciones, es_funcion).valido
    if len(bloques) == 3:
        otherwise = func_validar_bloque(bloques[2], variables, funciones, es_funcion).valido
    else:
        otherwise = True

    return condicion_valida and then and otherwise


def chequeo_ciclo(text: str, variables: list, funciones: list, func_validar_bloque: Callable[[str, list[str], list[tuple[str, int]], bool], Resultado], es_funcion = False) -> bool:
    comandos = dividir_comandos(text)

    if len(comandos) < 1 or comandos[0] != "loop":
        return False
    
    bloques = obtener_bloques(text.strip())

    if bloques is None:
        return False

    if len(bloques) != 2:
        return False

    condicion_valida = chequeo_condicion(bloques[0], variables)
    then = func_validar_bloque(bloques[1], variables, funciones, es_funcion).valido

    return condicion_valida and then


def chequeo_repetir(text: str, variables: list, funciones: list, func_validar_bloque: Callable[[str, list[str], list[tuple[str, int]], bool], Resultado], es_funcion = False) -> bool:
    comandos = dividir_comandos(text)

    if len(comandos) < 1 or comandos[0] != "repeat":
        return False
    
    bloques = obtener_bloques(text.strip())
    if bloques is None:
        return False

    if len(bloques) != 1:
        return False
    
    cantidad_valida = comandos[1] in CONSTANTES or comandos[1] in variables or comandos[1].isnumeric()
    otherwise = func_validar_bloque(bloques[0], variables, funciones, es_funcion).valido

    return cantidad_valida and otherwise


def chequeo_funcion(
            text: str,
            variables: list,
            funciones: list[tuple[str, int]],
            func_validar_bloque: Callable[[str, list[str], list[tuple[str, int]], bool], Resultado],
        ) -> tuple[str, int] | None:
    comandos = dividir_comandos(text)

    if len(comandos) < 1 or comandos[0] != "defun":
        return None
    
    bloques = obtener_bloques(text.strip())

    if bloques is None or len(bloques) < 2:
        return None

    if any(map(lambda x: x[0] == comandos[1] or comandos[1] in RESERVADAS or comandos[1] in variables, funciones)):
        return None

    nombre = comandos[1]

    parametros = dividir_comandos(bloques[0])

    if any(map(lambda x: x in variables or x in RESERVADAS or x in map(lambda f: f[0], funciones), parametros)):
        return None

    funciones_disponibles = funciones + [(nombre, len(parametros))]
    variables_disponibles = variables + parametros

    a_ejecutar = map(lambda bloque: func_validar_bloque(bloque, variables_disponibles, funciones_disponibles, True).valido, bloques[1:])

    if not all(a_ejecutar):
        return None

    return (nombre, len(parametros))



def es_estructura_valida(text: str, variables: list, funciones: list, func_validar_bloque: Callable[[str, list[str], list[tuple[str, int]], bool], Resultado], es_funcion = False) -> bool:
    return (chequeo_if(text, variables, funciones, func_validar_bloque, es_funcion) or
        chequeo_ciclo(text, variables, funciones, func_validar_bloque, es_funcion) or
        chequeo_repetir(text, variables, funciones, func_validar_bloque, es_funcion))

