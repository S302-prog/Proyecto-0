from bloques import validar_estructura_bloque, obtener_bloques
import estructura_control
import comandos

class Resultado:
	valido: bool
	tipo: str
	informacion: str

	def __init__(self, valido: bool, tipo: str, informacion: str) -> None:
		self.valido = valido
		self.tipo = tipo
		self.informacion = informacion


def validar_instruccion(texto: str, variables: list, funciones: list) -> tuple[bool, str, str]:
	validacion_variable = comandos.chequeo_defvar(texto.strip(), variables)

	if validacion_variable is not None:
		return (True, "DEFVAR", validacion_variable)

	return (comandos.es_comando_valido(texto, variables, funciones), "NONE", "")


def validar_bloque(texto: str, variables: list, funciones: list) -> Resultado:
	print(f"Validando [{texto}]")
	resultado = Resultado(False, "NONE", "")

	sub_bloques = obtener_bloques(texto.strip())

	if sub_bloques is None:
		return resultado

	if len(sub_bloques) == 0:
		print("DETERMINA INSTRUCCION SIMPLE")
		validez, tipo, valor = validar_instruccion(texto.strip(), variables, funciones)

		if validez:
			resultado.valido = True
			resultado.tipo = tipo
			resultado.informacion = valor
		return resultado

	validacion_funcion = estructura_control.chequeo_funcion(texto, variables)

	if validacion_funcion is not None:
		print("DETERMINA FUNCION")
		resultado.valido = True
		resultado.tipo = "DEFUN"
		resultado.informacion = validacion_funcion
		return resultado
	elif estructura_control.es_estructura_valida(texto, variables, funciones):
		print("DETERMINA INSTRUCCION VALIDA:", sub_bloques)
		resultado.valido = True
		resultado.tipo = "NONE"
	else:
		print("DETERMINA BLOQUE ANIDADO")
		validez = True

		for sub_parte in sub_bloques:
			validez = validar_bloque(sub_parte.strip(), variables, funciones).valido
			if not validez:
				break
		resultado.valido = validez # No chequeamos creación de nuevas funciones o variables dentro de bloques anidados


	return resultado


def validar(archivo: str) -> tuple[bool, list[str], list[str]]:
	info = open(archivo, "r")
	codigo = info.read().lower().strip()
	info.close()

	if not validar_estructura_bloque(codigo):
		return (False, [], [])

	variables = []
	funciones = []
	valido = True

	partes = obtener_bloques(codigo)

	if partes is None:
		return (False, [], [])

	for parte in partes:
		resultado = validar_bloque(parte, variables, funciones)
		valido = resultado.valido
		if not valido:
			break
		if resultado.tipo == "DEFVAR":
			variables.append(resultado.informacion)
		elif resultado.tipo == "DEFUN":
			funciones.append(resultado.informacion)

	return (valido, variables, funciones)