#!/usr/bin/env Python
#Este script se lanza cada vez que se inicie una Raspberry y se encarga de guardar en el servidor externo los datos del equipo para el evento actual
#Habra un directorio(/home/pi/Monitor) en cada Rasberry con un archivo json que contiene la informacion para cada evento
import socket
import json
import requests
import sys
import paramiko

#Lee el json con los datos del evento y los retorna
def obtener_info_equipo():
    try:
        with open('/home/pi/Pantalla/evento.json', 'r') as f:
            info = json.load(f)
        return info

    except IOError:
        print("No se ha podido abrir el archivo")
        sys.exit()


#Obtiene la ip priada del equipo y lo retorna
def obtener_ip_equipo():
    nombre_equipo = socket.gethostname()
    # print(nombre_equipo)
    try:
        ip_equipo = socket.gethostbyname(nombre_equipo)
        # print(ip_equipo)
        #if (not ip_equipo.startswith("10.") or not ip_equipo.startswith("172.") or not ip_equipo.startswith("192.") or not ip_equipo.startswith("192.")):
         #   s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          #  s.connect(("8.8.8.8", 80))
           # ip_equipo = s.getsockname()[0]
         #   s.close()

       # if (ip_equipo.startswith("10.") or  ip_equipo.startswith("172.") or  ip_equipo.startswith("192.") or ip_equipo.startswith("192.")):
            #time.sleep(30)
           # url = 'localhost/Central/Raspberries/Central.php'
            #chrome_path = '/usr/bin/chromium'
            #webbrowser.get(chrome_path).open(url)



    except OSError as err:
        print("Error OS: {0}".format(err))
        sys.exit()

    except:
        print("Error inesperado:", sys.exc_info()[0])
        sys.exit()


    return ip_equipo

def obtener_ip_central():
	
    datos_raspberry = obtener_info_equipo()

    info = [datos_raspberry["CodEvento"]]

    #print(info)
    

    parametros = {'CodEvento': datos_raspberry["CodEvento"]}
    print(info)

    try:	
        #msg = requests.get('http://192.168.181.1/dashboard/server/PDO/obtenerIPCentral.php', params=parametros)
        msg = requests.get('http://34.70.183.119/Login/db_scripts/obtenerIpCentral.php', params=parametros)
        print(msg.json()['IpPantalla'])
        #print(msg.json()['IpPantalla']+"/ControlPaneles/Central/Raspberries/"+datos_raspberry["CodPantalla"]+".php")
        #print(msg.text)
        print("d")
        return msg.json()['IpPantalla']
    except ConnectionError as err:
        #  print("Error ConnectionError: {0}".format(err))
        sys.exit()
    except OSError as err:
        #  print("Error OS: {0}".format(err))
        sys.exit()
    except:
        #  print("Error inesperado:", sys.exc_info()[0])
        sys.exit()

#Una vez obtenidos todos los datos del equipo se guardarán en la BD
def almacenar_info_bd():
    		
    datos_raspberry = obtener_info_equipo()
	
    ip_raspberry = obtener_ip_equipo()

    info = [datos_raspberry["CodEvento"], datos_raspberry["CodPantalla"], ip_raspberry, datos_raspberry["NomPantalla"]]

    #print(info)

    parametros = {'CodEvento': info[0], 'CodPantalla': info[1], 'IpPantalla': info[2], 'NomPantalla': info[3]}
    try:
    	 
        #msg = requests.get('http://192.168.181.1/dashboard/server/PDO/almacenapantalla.php', params=parametros)
        msg = requests.get('http://34.70.183.119/Login/db_scripts/almacenapantalla.php', params=parametros)        
        crear_template(info[1])
        
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
        
        
def crear_template(codPantalla):
	
	ip_central = obtener_ip_central()
	print("d")
	client = paramiko.SSHClient()
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())	
	client.connect(ip_central, username="pi", password="alvaro")
	print(ip_central)
	
	html = "<html ><head></head><body><style> <?php include '../css/templates.css'; ?> </style></body></html>"
	
	
	client.exec_command('echo \"'+html+'\" > /var/www/html/ControlPaneles/Central/Raspberries/' + str(codPantalla)+'.php')
	
	client.exec_command('sudo chmod 777 /var/www/html/ControlPaneles/Central/Raspberries/'+ str(codPantalla)+'.php')

	client.close()
	
	
if __name__ == "__main__":
        almacenar_info_bd()
