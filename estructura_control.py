from comandos import dividir_comandos
from bloques import obtener_bloques, validar_estructura_bloque

def chequeo_condicion(text: str, variables: list) -> bool:    
    return True


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
