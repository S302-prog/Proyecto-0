from comandos import dividir_comandos
from bloques import obtener_bloques, validar_estructura_bloque
from lenguaje import CONDICIONES, CONSTANTES, ORIENTACIONES, OBJETOS

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

    if partes[0] == "facing":
        if len(partes) != 3:
            return False
        return partes[2] in ORIENTACIONES

    if partes[0] == "blocked":
        return len(partes) == 2

    if partes[0] in ["can-put", "can-pick"]:
        if len(partes) != 4:
            return False

        if partes[2] not in OBJETOS:
            return False

        return partes[3].isnumeric() or partes[3] in CONSTANTES or partes[3] in variables

    if partes[0] == "can-move":
        if len(partes) != 3:
            return False

        return partes[2] in ORIENTACIONES

    if partes[0] == "isZero":
        if len(partes) != 3:
            return False

        return partes[2].isnumeric() or partes[2] in CONSTANTES or partes[2] in variables


    return False


def chequeo_if(text: str, variables: list) -> bool:
    comandos = dividir_comandos(text)

    if len(comandos) < 1 or comandos[0] != "if":
        return False

    bloques = obtener_bloques(text.strip())
    if bloques is None:
        return False

    if len(bloques) != 3:
        return False

    condicion_valida = chequeo_condicion(bloques[0], variables)
    then = validar_estructura_bloque(bloques[1])
    otherwise = validar_estructura_bloque(bloques[2])

    return condicion_valida and then and otherwise



def chequeo_ciclo(text: str, variables: list) -> bool:
    return False


def chequeo_repetir(text: str, variables: list) -> bool:
    return False


def chequeo_funcion(text: str, variables: list) -> str | None:
    return None


def es_estructura_valida(text: str, variables: list, funciones: list) -> bool:
    return True
