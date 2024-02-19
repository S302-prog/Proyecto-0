from parser import validar

if __name__ == "__main__":
    autores = ["Juan David Guevara - 202116875", "Sebastian Palma Mogollon - 202222498"]

    print("="*60)
    print(f"{'-'*10} PARSER LENGUAJES Y MAQUINAS PROYECTO 0 {'-'*10}")
    print("_"*60)
    for autor in autores:
        l = (60 - len(autor)) // 2
        print(f"{' '*(l-1)} {autor} {' '*(l-1)}")
    print("="*60+"\n\n")

    # Para imprimir el proceso de validación en consola, agregar True como parametro a la función validar()

    v = validar("tests/pruebas.txt")
    print(f"El archivo 'tests/pruebas.txt' es {'in' if not v[0] else ''}correcto")
    v = validar("tests/ejemploPDFcorregido.txt")
    print(f"El archivo 'tests/ejemploPDFcorregido.txt' es {'in' if not v[0] else ''}correcto")
