import re 

lista_direcciones = [":front", ":right", ":left", ":back"] 
lista_orientaciones = [":north", ":south", ":west", ":east"]
lista_op = [":left", ":right", ":around"]
lista_constantes = ["Dim", "myXpos", "myYpos", "MyChips", "myBalloons", "balloonsHere", "ChipsHere", "Spaces"]
b_or_c = [":balloons", ":chips"]

"""toca crear lista que guarde las variables que se creen con defvar ya que estas tambien pueden ser n y con esa lista creada seria poner un or en lo try-except en """

def dividir_comandos(text: str):
    """
    Divide los caracteres de los comandos en una lista
    """

    lista = re.split(r"[,()\s]", text)

    nueva_lista = []
    palabra_actual = ""

    for elemento in lista:
        if ":" in elemento:
            if palabra_actual:
                nueva_lista.append(palabra_actual)
                palabra_actual = ""
            palabra_actual = elemento
        else:
            if palabra_actual:
                palabra_actual += elemento
            else:
                nueva_lista.append(elemento)

    if palabra_actual:
        nueva_lista.append(palabra_actual)

    nueva_lista = [x for x in nueva_lista if x]

    return nueva_lista

print(dividir_comandos("(put :chips myXpos)"))
print(dividir_comandos("(run-dirs :left :up :left :right)"))

"""Primera parte, revisar todos los comandos"""

def rev_defVar(text: str):
    """
    Revisa que los defVar estan bien escritos
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 3 or tokens[0] != "defvar":
        return False
    
    try:
        int(tokens[1])
        return False
    except ValueError:
        pass

    try:
        int(tokens[2])
    except ValueError:
        if tokens[2] in lista_constantes:
            return True
    else:
        return True

    return False  

def rev_name(text: str):
    """
    Revisa que los name estan bien escritos
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 3 or tokens[0] != "=":
        return False
    
    try:
        int(tokens[1])
        return False
    except ValueError:
        pass

    try:
        int(tokens[2])
    except ValueError:
        if tokens[2] in lista_constantes:
            return True
    else:
        return True

    return False  

def rev_move(text: str):
    """
    Revisa que los move estan bien escritos
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 2 or tokens[0] != "move":
        return False
    
    try:
        int(tokens[1])
    except ValueError:
        if tokens[1] in lista_constantes:
            return True
    else:
        return True

    return False  

def rev_skip(text: str):
    """
    Revisa que los skip estan bien escritos
    """
    tokens = dividir_comandos(text)

    if len(tokens) != 2 or tokens[0] != "skip":
        return False
    
    try:
        int(tokens[1])
    except ValueError:
        if tokens[1] in lista_constantes:
            return True
    else:
        return True

    return False  

def rev_turn(text: str):
    """
    Revisa que los turn estan bien escritos
    """
    tokens = dividir_comandos(text)
    
    if tokens[0] == "turn" and tokens[1] in lista_op  and len(tokens) == 2:
        return True
 
    return False

def rev_face(text: str):
    """
    Revisa que los face estan bien escritos
    """
    tokens = dividir_comandos(text)
    
    if tokens[0] == "face" and tokens[1] in lista_orientaciones  and len(tokens) == 2:
        return True
 
    return False

def rev_put(text: str):
    """
    Revisa que los put estan bien escritos
    """
    tokens = dividir_comandos(text)

    if tokens[0] != "put" or tokens[1] not in b_or_c or len(tokens) != 3:
        return False
    
    try:
        int(tokens[1])
    except ValueError:
        if tokens[1] in lista_constantes:
            return True
    else:
        return True
    
    return False

print(rev_put("put :balloons 3"))


def rev_pick(text: str):
    """
    Revisa que los pick estan bien escritos
    """
    tokens = dividir_comandos(text)

    if tokens[0] != "pick" or tokens[1] not in b_or_c or len(tokens) != 3:
        return False
    
    try:
        int(tokens[1])
    except ValueError:
        if tokens[1] in lista_constantes:
            return True
    else:
        return True
    
    return False

def rev_move_dir(text: str):
    """
    Revisa que los move-dir estan bien escritos
    """
    tokens = dividir_comandos(text)

    if tokens[0] != "move_dir" or tokens[1] not in lista_direcciones or len(tokens) != 3:
        return False
    
    try:
        int(tokens[1])
    except ValueError:
        if tokens[1] in lista_constantes:
            return True
    else:
        return True
    
    return False

def rev_run_dir(text: str):
    """
    Revisa que los run-dirs estan bien escritos
    """
    tokens = dividir_comandos(text)

    if tokens[0] == "run-dirs":
        return all(elemento in lista_direcciones for elemento in tokens[1:])
    
    return False

def rev_move_face(text: str):
    """
    Revisa que los move-face estan bien escritos
    """
    tokens = dividir_comandos(text)

    if tokens[0] != "move_face" or tokens[1] not in lista_orientaciones or len(tokens) != 3:
        return False
    
    try:
        int(tokens[1])
    except ValueError:
        if tokens[1] in lista_constantes:
            return True
    else:
        return True
    
    return False

def rev_null(text: str):
    """
    Revisa que los move-face estan bien escritos
    """
    tokens = dividir_comandos(text)

    if tokens[0] == "null" and len(tokens) == 1:
        return True
    
    return False

"""Segunda parte, revisar todos los condicionales"""


