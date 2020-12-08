#!/usr/bin/python3.6
#-*- coding: utf-8 -*-

# Se importan los módulos que van a ser utilizados.
from subprocess import Popen, PIPE
import sys
import argparse
import re
import collections
from collections import Counter

# Se crea un objeto parser para procesar los parámetros que se la van a pasar al script.
parser = argparse.ArgumentParser()

# Se definen los distintos modificadores del script. Se van adicionando uno a uno al parser.
parser.add_argument("-r", "--recursivo", help = "Busca los archivos en forma recursiva a partir del directorio pasado como parámetro.", action = "store_true")

parser.add_argument("-t", "--archivosTxt", help = "Busca los correos en archivos .txt", action = "store_true")

parser.add_argument("-d", "--modDominio", type = str, help = "Busca correos pertenecientes al dominio ingresado.")

parser.add_argument("-e", "--cantidad", type = str, choices = ["d", "t", "c"], help = "Muestra la cantidad de correos por dominio (d), cantidad de dominios diferentes (t), o ambos (c).")

parser.add_argument("-f", "--exp_reg", type = str, help = "Busca correos que cumplan con la expresión regular ingresada.")

parser.add_argument("-o", "--orden", type = str, choices = ["a", "d", "l"], help = "Ordena los correos alfabéticamente creciente (a), dominios alfabéticamente creciente (d), o el largo de caracteres en forma creciente (l).")

parser.add_argument("directorio", type = str, help = "Directorio donde se va a hacer la búsqueda.")

# Se crea un try catch que procese excepciones, por si algun parámetro es ingresado erróneamente.
try:
    args = parser.parse_args()
except SystemExit as e:
    print("La sintaxis correcta del script es: ej2_busca_correos_expandido.py [-r] [-t] [-d dominio] [-e {d,t,c}] [-f RegExp] [-o {a,d,l}] directorio")
    exit(20)

# Se crea la lista con el directorio que se le va a pasar al script del ejercicio 1. Los parámetros que hayan sido ingresados también se van sumando a la lista.
ej1ListaParametros = ['/home/nacho/DevOps/ej1_busca_correos.sh']

if args.recursivo:
    ej1ListaParametros.append("-r")

if args.archivosTxt:
    ej1ListaParametros.append("-t")

if args.modDominio:
    ej1ListaParametros.append("-d")
    ej1ListaParametros.append(args.modDominio)

ej1ListaParametros.append(args.directorio)

# Usando Popen, PIPE y process, se ejecuta el script del ejercicio con los parámetros de la lista creada anteriormente, y se guarda el stdout y el stderr.
process = Popen(ej1ListaParametros, stdout = PIPE, stderr = PIPE)

output = process.communicate()

# Si hay errores, el script 2 interpreta los códigos enviados por el script 2 y muestra los mensajes acorde.
if process.returncode > 0:
    print(output[1].decode('utf-8'), file = sys.stderr, end = "")
    exit(process.returncode)

# Si no hay errores, pero el script no encuentra ningún archivo o correo, igualmente se usa el mensaje recibido, con el código 0.
if output[1].decode('utf-8') !="":
    print(output[1].decode('utf-8'), file = sys.stderr)
    exit(0)

# Una vez se reciba la lista de correos del script 1, se guarda en "listaCorreos".
# Como en esa lista, el último ítem es un espacio vacío, se elimina con pop(-1), y el mensaje de la cantidad de correos encontrados también se quita de la lista
# y se guarda por separado, en caso de que el usuario quiera filtrar por una expresión regular y haya que cambiar el mensaje.
listaCorreos = output[0].decode('utf-8').split("\n")
listaCorreos.pop(-1)
msjCantidad = [listaCorreos[-1]]
listaCorreos.pop(-1)

# Se procesa el parámetro -f y la expresión regular ingresada. Primero se prueba que la expresión regular sea válida.
# Luego se crea la lista "correosExpReg", en donde se guardan solo los correos que cumplan con la expresión regular, 
# y después se sobreescribe "listaCorreos" con "corresExpReg", para poder alterarla mas adelante en caso de que se reciba -o.
# También se cambia el mensaje de cantidad, ya que ahora la cantidad es diferente a la que nos dice el script 1.
if args.exp_reg != None:
    try:
        patron = re.compile(args.exp_reg)
    except Exception as e:
        print("La expresión regular ingresada es incorrecta, ingrese una expresión regular válida.", file = sys.stderr)
        exit(10)
    correosExpReg = []
    for correo in listaCorreos:
        if patron.match(correo):
            correosExpReg.append(correo)
    listaCorreos = correosExpReg
    msjCantidad = ["Cantidad de correos encontrados que cumplen con la expresion:", len(listaCorreos)]

# Se procesa el parámetro -o y sus opciones: a, d y l.
if args.orden == "a":
  listaCorreos.sort()

if args.orden == "d":
    for correo in listaCorreos:
        listaCorreos.sort(key = lambda correo: correo.split("@")[1])

if args.orden == "l":
    for correo in listaCorreos:
        listaCorreos.sort(key = lambda correo: len(correo))

# Habiendo terminado de alterar la lista de correos, según si hay expresión regular u orden, se imprime la lista junto al mensaje de cantidad.
for correo in listaCorreos:
  print(correo)
print(*msjCantidad)

# Se procesa el parámetro -e y sus opciones: d, t y c.
listaDominio = []
for lineaCorreo in listaCorreos:
    listaDominio.append(lineaCorreo.split("@")[1])

if args.cantidad == "d":
    diccionario = collections.Counter(listaDominio)
    print("Reporte cantidad de correos encontrados por dominio:", "\n")
    for key, value in diccionario.items():
        print(key, ":", value)

if args.cantidad == "t":
    print("Cantidad de dominios diferentes encontrados:", len(collections.Counter(listaDominio).keys()))

if args.cantidad == "c":
    diccionario = collections.Counter(listaDominio)
    print("Reporte cantidad de correos encontrados por dominio:", "\n")
    for key, value in diccionario.items():
        print(key,":", value)
    print("\n")
    print("Cantidad de dominios diferentes encontrados:", len(collections.Counter(listaDominio).keys()))
