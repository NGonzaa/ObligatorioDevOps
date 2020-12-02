#!/bin/bash

# Se define la variable para saber si el comando find va a realizar una busqueda recursiva o no. Si no se pasa el parametro -r, la busqueda no sera recursiva, por lo que hay que limitar al find, que busca recursivo por defecto.
recursivo="-maxdepth 1"

# Se definen variables para la busqueda de todos los archivos, ocultos o no, regulares o no, cualquier terminacion, utilizando expansion de nombres.
ocultosOno="*"
soloRegulares=""

# Se define la expresion regular que matchea dominios de correo.
dominio="[a-zA-Z0-9]{2}[a-zA-Z0-9_.]*"

# Se utiliza getopts para procesar los parametro introducidos por el usuario, y definir las variables correspondientes.
while getopts ":rtd:" modificador
do
	case $modificador in
		r)  # Si se pasa el parametro -r, se vacia la variable "recursivo" para que el find pueda buscar de manera recursiva.
			recursivo=""
		;;
		t)  # Si se pasa el parametro -t, se alteran la "ocultosOno" para que solo busque archivos no ocultos con terminacion .txt, y se define la variable "soloRegulares" para que el find busque solo archivos regulares.
			ocultosOno="[^.]*.txt"
			soloRegulares="-type f"
		;;
		d)  # Si se pasa el parametro -d junto con el dominio deseado, el mismo se guarda en la variable "dominio", reemplazando la expresion regular. A su vez, se valida que el dominio ingresado cumpla las condiciones de ser un dominio.
			dominio=$OPTARG
			if ! [[ "$dominio" =~ [a-zA-Z0-9]{2}[a-zA-Z0-9_.]* ]]
			then
				echo "El dominio ingresado no es posible." >&2
				exit 6
			elif [[ "$dominio" =~ ^[._] | [_.]$]]
				echo "El dominio ingresado no es posible." >&2
				exit 6
			fi
		;;
		*)	# Si se pasa algun parametro distinto de los especificados anteriormente, el script va a terminar con este mensaje de error.
			echo "Modificador "-$OPTARG" incorrecto, solo se acepta -r, -t y -d." >&2
			exit 5
		;;
	esac
done

# Controla que se haya ingresado una cantidad correcta de parametros. Si la cantidad es correcta, se hace un shift para descartar los parametros procesados por el getopts para quedarnos solo con el directorio como $1, y de no ser asi, el script termina con error.
if [ $# -ne $OPTIND ]
then
	echo "Cantidad de parámetros incorrecta, solo se reciben los modificadores -r, -t, -d dominio y un directorio accesible en el sistema de archivos" >&2
	exit 4
else
	shift $((OPTIND-1))
fi

# Se chequea que el usuario haya ingresado un directorio.
if [ -z "$1" ]
then
	echo "Por favor, ingrese un directorio." >&2
	exit 6
fi

# El directorio se pasa a ruta absoluta, sin importar si el usuario introdujo una ruta absoluta o relativa.
directorio=`readlink -m "$1"`

# Se verifica si el directorio existe en el sistema de archivos.
if ! [ -a "$directorio" ]
then
	echo "El directorio "$directorio" no existe." >&2
	exit 1
fi

# Se verifica si el directorio es un directorio y no otro tipo de archivo.
if ! [ -d "$directorio" ]
then
	echo "El parámetro "$directorio" no es un directorio." >&2
	exit 2
fi

# Se verifican los permisos de acceso al directorio probandolos explicitamente. Se busca probar los permisos de lectura y ejecucion.
if ! ([ -r "$directorio" ] && [ -x "$directorio" ])
then
	echo "No se tienen los permisos necesarios para acceder al directorio y buscar correos." >&2
	exit 3
fi

# Se usa el comando find con todas las opcions definidas por el usuario al ejecutar el script, y se define una variable que contenga los archivos encontrados.
archivos_a_recorrer=`find "$directorio" $recursivo -name "$ocultosOno" $soloRegulares`

# Se prueba si se encontraron archivos en el directorio.
if [ -z "$archivos_a_recorrer" ]
then
    echo "No se han encontrado archivos en el directorio $directorio."
    exit 0
fi

# Se usa el comando grep. Se le pasan como parametros una expresion regular que matchee correos, junto a un "@" y la variable dominio, que va a contener o la expresion regular o el dominio ingresado por el usuario, y por ultimo la variable con los archivos encontrados por el find. El resultado del grep va a ser redireccionado a un archivo llamado "resultado".
grep -hos "[a-zA-Z0-9_.]*[^_.]@$dominio" $archivos_a_recorrer > resultado

# Se prueba si se encontraron correos en los archivos encontrados.
if [ -z "$(cat resultado)" ]
then
    echo "No se han encontrado correos en el directorio $directorio."
	rm resultado
    exit 0
fi

# Se hace un cat del archivo "resultado" para listar todos los correos encontrados.
cat resultado

# Luego del listado, se hace un echo con el total de correos.
echo "Cantidad de correos encontrados en el directorio $directorio: $(wc -l resultado | cut -c1)"

# Se borra el archivo "resultado" para evitar que en alguna ejcucion futura del script haya correos o resultados duplicados.
rm resultado
