#!/usr/bin/env Python
#Este script se lanza cada vez que se inicie una Raspberry y se encarga de guardar en el servidor externo los datos del equipo para el evento actual
#Habra un directorio(/home/pi/Monitor) en cada Rasberry con un archivo json que contiene la informacion para cada evento
import socket
import json
import sys
import requests


#Lee el json con los datos del evento y los retorna
def obtener_info_equipo():
    try:
        with open('/home/pi/Pantalla/evento.json', 'r') as f:
            info = json.load(f)

        
        return info

    except IOError:
        print("No se ha podido abrir el archivo")
        sys.exit()


def obtener_ip_central():
	
    datos_raspberry = obtener_info_equipo()

    info = [datos_raspberry["CodEvento"]]

    #print(info)

    parametros = {'CodEvento': datos_raspberry["CodEvento"]}

    try:	
        #msg = requests.get('http://192.168.181.1/dashboard/server/PDO/obtenerIPCentral.php', params=parametros)
        msg = requests.get('http://34.70.183.119/Login/db_scripts/obtenerIpCentral.php', params=parametros)
        #print(msg.json()['IpPantalla'])
        print(msg.json()['IpPantalla']+"/ControlPaneles/Central/Raspberries/"+datos_raspberry["CodPantalla"]+".php")
        #print(msg.text)
        return msg
    except ConnectionError as err:
        #  print("Error ConnectionError: {0}".format(err))
        sys.exit()
    except OSError as err:
        #  print("Error OS: {0}".format(err))
        sys.exit()
    except:
        #  print("Error inesperado:", sys.exc_info()[0])
        sys.exit()
	


if __name__ == "__main__":
        obtener_ip_central()



