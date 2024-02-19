class Resultado:
	valido: bool
	tipo: str
	informacion: str | tuple[str, int]

	def __init__(self, valido: bool, tipo: str, informacion: str | tuple[str, int]) -> None:
		self.valido = valido
		self.tipo = tipo
		self.informacion = informacion
		

def validar_estructura_bloque(text: str) -> bool:
	if len(text.strip()) < 2:
		return False

	parentesis = 0

	for t in text:
		if parentesis < 0: return False
		if t == "(":
			parentesis += 1
		elif t == ")":
			parentesis -= 1

	return parentesis == 0


def solo_un_bloque(text: str) -> bool:
	parentesis = 0
	abierto = False
	cerradas = 0

	for t in text:
		if parentesis < 0: return False
		if t == "(":
			parentesis += 1
			abierto = True
		elif t == ")":
			parentesis -= 1
		if parentesis == 0 and abierto:
			cerradas += 1
	return cerradas == 1



def obtener_bloques(text: str) -> list[str] | None:
	if not validar_estructura_bloque(text.strip()):
		return None

	if solo_un_bloque(text.strip()):
		text = text[1:-1]

	bloques = []

	actual = 0
	parentesis = 0
	bloque_actual = ""
	abierto = False

	for t in text:
		if t == "(":
			parentesis += 1
			abierto = True
		elif t == ")":
			parentesis -= 1

		if parentesis == 0 and actual > 0 and bloque_actual.strip() != "" and abierto:
			bloques.append(bloque_actual.strip() + t)
			bloque_actual = ""
		elif abierto:
			bloque_actual += t

		actual += 1

	return bloques
