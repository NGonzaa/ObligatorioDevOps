#!/usr/bin/python3.6
#-*- coding: utf-8 -*-

from subprocess import Popen, PIPE
import sys
import argparse
import re
import collections
from collections import Counter

parser = argparse.ArgumentParser()

# Se definen los distintos modificadores
# con el texto que los describe. Se van adicionando uno a uno.
# Se define el modificador para recursividad.
parser.add_argument("-r", "--recursivo", help="Busca los archivos en forma recursiva a partir del directorio pasado como parámetro.", action="store_true")

parser.add_argument("-t", "--archivosTxt", help="Busca los correos en archivos .txt", action="store_true")

parser.add_argument("-d", "--modDominio", help="Modificador -d del dominio", action="store_true")

parser.add_argument("dominio", type=str, nargs='?', default="", help="Dominio del correo.")

parser.add_argument("-e", "--cantidad", type=str, choices=["d", "t", "c"], help="Cantidad de correos por dominio (parámetro d) o cantidad de dominios diferentes (parámetro t) o ambos (parámetro c).")

#parser.add_argument("-f", "--modExpRegular", help="Modificador -f de la expresion regular", action="store_true")
parser.add_argument("-f", "--exp_reg", type=str, help="Expresion regular")

#parser.add_argument("expRegular", type=str, help="Expresion regular.")

parser.add_argument("-o", "--orden", type=str, choices=["a", "d", "l"], help="Orden de los correos, alfabeticamente creciente (parámetro a) /"
                                                                             "o dominios ordenados alfabeticamente creciente (parámetro d)/"
                                                                             "o el largo de caracteres en forma creciente (parámetro l.")

parser.add_argument("directorio", type=str, help="Directorio donde se va a hacer la búsqueda.")

try:
    args = parser.parse_args()
except SystemExit as e:
 # Se define a 10 como el código de salida en caso que se detecte
 # algún problema en los argumentos de entrada.
    print("Error la sintaxis correcta del script es: ej2_busca_correos_expandido.py [-r] [-t] [-d dom] [-e {d,t,c}] [-f RegExp] [-o {a,d,l}] Dir")
    exit(20)

ej1_y_lista_parametros = ['/home/nacho/DevOps/ej1_busca_correos.sh']

if args.recursivo:
    ej1_y_lista_parametros.append("-r")

if args.archivosTxt:
    ej1_y_lista_parametros.append("-t")

if args.modDominio:
    ej1_y_lista_parametros.append("-d")

ej1_y_lista_parametros.append(args.dominio)

ej1_y_lista_parametros.append(args.directorio)

# salida estándar y la salida estándar de errores.
process = Popen(ej1_y_lista_parametros, stdout = PIPE, stderr = PIPE)

output = process.communicate()

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

#for correo in listaCorreos:
#    print(correo)

if args.exp_reg != None:
    try:
        patron = re.compile(args.exp_reg)
    except Exception as e:
        std=file = sys.stderr
        print("La expresion regular ingresada es incorrecta, ingrese una expresion regular valida.", std)
        exit(10)
    correosExpReg=[]
    for correo in listaCorreos:
        if patron.match(correo):
            correosExpReg.append(correo + "\n")
    print(correosExpReg)

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

#argumentos requeridos ojoooo
#errores de la salida estandar de errores del ej1
#error en el print con file=sys.stderr
