import re
from bloques import validar_estructura_bloque, obtener_bloques, Resultado
import estructura_control
import comandos

def validar_instruccion(texto: str, variables: list, funciones: list) -> tuple[bool, str, str]:
	validacion_variable = comandos.chequeo_defvar(texto.strip(), variables)

	if validacion_variable is not None:
		return (True, "DEFVAR", validacion_variable)

	return (comandos.es_comando_valido(texto, variables, funciones), "NONE", "")


def validar_bloque(texto: str, variables: list[str], funciones: list[tuple[str, int]], es_funcion = False, debug = False) -> Resultado:
	if debug: print(f"Validando [{texto}]")
	resultado = Resultado(False, "NONE", "")

	sub_bloques = obtener_bloques(texto.strip())

	if sub_bloques is None:
		return resultado

	if len(sub_bloques) == 0:
		if debug: print("DETERMINA INSTRUCCION SIMPLE... VALINDANDO LA INSTRUCCIÓN")
		validez, tipo, valor = validar_instruccion(texto.strip(), variables, funciones)

		if validez:
			resultado.valido = True
			resultado.tipo = tipo
			resultado.informacion = valor

			if es_funcion:
				if resultado.tipo == "DEFVAR":
					variables.append(str(resultado.informacion))
		return resultado

	validacion_funcion = estructura_control.chequeo_funcion(texto, variables, funciones, validar_bloque)

	if validacion_funcion is not None:
		if debug: print("DETERMINA FUNCION")
		resultado.valido = True
		resultado.tipo = "DEFUN"
		resultado.informacion = validacion_funcion
		return resultado
	elif estructura_control.es_estructura_valida(texto, variables, funciones, validar_bloque, es_funcion):
		if debug: print("DETERMINA ESTRUCTURA VALIDA:", sub_bloques)
		resultado.valido = True
		resultado.tipo = "NONE"
	else:
		if debug: print("DETERMINA BLOQUE ANIDADO")
		validez = True

		for sub_parte in sub_bloques:
			validez = validar_bloque(sub_parte.strip(), variables, funciones, es_funcion, debug).valido
			if not validez:
				break
		resultado.valido = validez # No chequeamos creación de nuevas funciones o variables dentro de bloques anidados


	return resultado


def validar(archivo: str, debug = False) -> tuple[bool, list[str], list[tuple[str, int]]]:
	info = open(archivo, "r")
	codigo = info.read().lower().strip()
	info.close()

	if not validar_estructura_bloque(codigo):
		return (False, [], [])

	variables: list[str] = []
	funciones: list[tuple[str, int]] = []
	valido = True

	partes = obtener_bloques(codigo)

	if partes is None:
		return (False, [], [])

	for parte in partes:
		resultado = validar_bloque(parte, variables, funciones, debug = debug)
		if debug: print(resultado.valido, resultado.tipo, resultado.informacion)
		valido = resultado.valido
		if not valido:
			break
		if resultado.tipo == "DEFVAR":
			variables.append(str(resultado.informacion))
		elif resultado.tipo == "DEFUN":
			funciones.append(tuple[str, int](resultado.informacion))

	return (valido, variables, funciones)