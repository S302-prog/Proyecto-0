from comandos import chequeo_pick_put
import re


def procesar_bloque(bloque: str) -> bool:
    if len(bloque) < 2:
        return False
    bloques = re.findall(r"(.*)", bloque)

    print(bloques)

    return True


if __name__ == "__main__":
    print(chequeo_pick_put("put :balloons 3"))
    print(chequeo_pick_put("pick :balloons 3"))

    bloque = open("tests/pruebas.txt").read()
    print(procesar_bloque(bloque.strip()))

    bloque = open("tests/ejemploPDFcorregido.txt").read()
    print(procesar_bloque(bloque.strip()))
