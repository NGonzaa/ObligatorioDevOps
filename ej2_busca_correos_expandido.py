#!/usr/bin/python3.6
#-*- coding: utf-8 -*-

# Se importan los modulos que van a ser utilizados.
from subprocess import Popen, PIPE
import sys
import argparse
import re
import collections
from collections import Counter

# Se crea un objeto parser para procesar los parametros que se la van a pasar al script.
parser = argparse.ArgumentParser()

# Se definen los distintos modificadores del script. Se van adicionando uno a uno al parser.
parser.add_argument("-r", "--recursivo", help="Busca los archivos en forma recursiva a partir del directorio pasado como parámetro.", action="store_true")

parser.add_argument("-t", "--archivosTxt", help="Busca los correos en archivos .txt", action="store_true")

parser.add_argument("-d", "--modDominio", type=str, help="Busca correos pertenecientes al dominio ingresado.")

parser.add_argument("-e", "--cantidad", type=str, choices=["d", "t", "c"], help="Muestra la cantidad de correos por dominio (d), cantidad de dominios diferentes (t), o ambos (c).")

parser.add_argument("-f", "--exp_reg", type=str, help="Busca correos que cumplan con la expresion regular ingresada.")

parser.add_argument("-o", "--orden", type=str, choices=["a", "d", "l"], help="Ordena los correos alfabeticamente creciente (a), dominios alfabeticamente creciente (d), o el largo de caracteres en forma creciente (l).")

parser.add_argument("directorio", type=str, help="Directorio donde se va a hacer la búsqueda.")

# Se crea un try catch que procese excepciones, por si algun parametro es ingresado erroneamente.
try:
    args = parser.parse_args()
except SystemExit as e:
    print("Error la sintaxis correcta del script es: ej2_busca_correos_expandido.py [-r] [-t] [-d dom] [-e {d,t,c}] [-f RegExp] [-o {a,d,l}] Dir")
    exit(20)

# Se crea la lista con el directorio que se le va a pasar al script del ejercicio 1. Los parametros que hayan sido ingresados tambien se van sumando a la lista.
ej1_y_lista_parametros = ['/home/nacho/DevOps/ej1_busca_correos.sh']

if args.recursivo:
    ej1_y_lista_parametros.append("-r")

if args.archivosTxt:
    ej1_y_lista_parametros.append("-t")

if args.modDominio:
    ej1_y_lista_parametros.append("-d")
    ej1_y_lista_parametros.append(args.modDominio)

ej1_y_lista_parametros.append(args.directorio)

# Usando Popen, PIPE y process, se ejecuta el script del ejercicio con los parametros de la lista creada anteriormente, y se guarda el stdout y el stderr.
process = Popen(ej1_y_lista_parametros, stdout = PIPE, stderr = PIPE)

output = process.communicate()

# Si hay errores, el script 2 interpreta los codigos enviados por el script 2 y muestra los mensajes acorde.
if process.returncode > 0:
    std=file=sys.stderr
    print(output[1].decode('utf-8'), std)
    exit(process.returncode)

if output[1].decode('utf-8') !="":
    std=file=sys.stderr
    print(output[1].decode('utf-8'), std)
    exit(0)

listaCorreos = output[0].decode('utf-8').split("\n")
listaCorreos.pop(-1)
msjCantidad = [listaCorreos[-1]]
listaCorreos.pop(-1)

if args.exp_reg != None:
    try:
        patron = re.compile(args.exp_reg)
    except Exception as e:
        std=file=sys.stderr
        print("La expresion regular ingresada es incorrecta, ingrese una expresion regular valida.", std)
        exit(10)
    correosExpReg=[]
    for correo in listaCorreos:
        if patron.match(correo):
            correosExpReg.append(correo)
    listaCorreos = correosExpReg
    msjCantidad = ["Cantidad de correos encontrados que cumplen con la expresion:", len(listaCorreos)]

# alfabetica creciente
if args.orden == "a":
  listaCorreos.sort()

for correo in listaCorreos:
  print(correo)
print(*msjCantidad)

# -e
listaDominio=[]
for lineaCorreo in listaCorreos[:-1]:
    listaDominio.append(lineaCorreo.split("@")[1])

if args.cantidad == "d":
    diccionario=collections.Counter(listaDominio)
    print("Reporte cantidad de correos encontrados por dominio: ", "\n")
    for key, value in diccionario.items():
        print(key, ":", value)

if args.cantidad == "t":
    print("Cantidad de dominios diferentes encontrados: ", len(collections.Counter(listaDominio).keys()))

if args.cantidad == "c":
    diccionario=collections.Counter(listaDominio)
    print("Reporte cantidad de correos encontrados por dominio: ", "\n")
    for key, value in diccionario.items():
        print(key,":", value)
    print("\n")
    print("Cantidad de dominios diferentes encontrados: ", len(collections.Counter(listaDominio).keys()))

#errores de la salida estandar de errores del ej1
#error en el print con file=sys.stderr
