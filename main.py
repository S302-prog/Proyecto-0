from parser import validar


if __name__ == "__main__":
    v = validar("tests/pruebas.txt")
    print(v)
    v = validar("tests/ejemploPDFcorregido.txt")
    print(v)
