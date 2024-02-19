DIRECCIONES = [":front", ":right", ":left", ":back", ":down", ":up"]
ORIENTACIONES = [":north", ":south", ":west", ":east"]
ROTACIONES = [":left", ":right", ":around"]
CONSTANTES = list(map(lambda x: x.lower(), ["Dim", "myXpos", "myYpos", "MyChips", "myBalloons", "balloonsHere", "ChipsHere", "Spaces"]))
OBJETOS = [":balloons", ":chips"]
COMANDOS = ["name", "move", "skip", "turn", "face", "put", "pick", "move-dir", "run-dirs", "move-face", "null"]

CONDICIONES = ["facing?", "blocked?", "can-put?", "can-pick?", "can-move?", "iszero?", "not"]

RESERVADAS = DIRECCIONES + ORIENTACIONES + ROTACIONES + CONSTANTES + OBJETOS + COMANDOS + CONDICIONES