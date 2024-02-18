from comandos import chequeo_pick_put
from bloques import obtener_bloques
from estructura_control import chequeo_if
from parser import validar


if __name__ == "__main__":
    v = validar("tests/pruebas.txt")
    print(v)
    v = validar("tests/ejemploPDFcorregido.txt")
    print(v)

