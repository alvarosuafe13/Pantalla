#!/bin/bash

ip=$(hostname -I | awk '{print $1}')

#ping=$(ping -c1 8.8.8.8 &>/dev/null)



#if ping -c1 8.8.8.8 >/dev/null 2>/dev/null; 
#	then 
	        #/usr/bin/chromium --no-sandbox --start-fullscreen localhost/Central&
		xset s noblank
		xset s off
		xset -dpms

		#unclutter -idle 0.5 -root &
		#sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
		#sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences


		/usr/bin/python3 /home/pi/Pantalla/almacenar_pantalla.py&
		
		url=$(/usr/bin/python3  /home/pi/Pantalla/obtener_url_central.py)

		sleep 5


		#/usr/bin/chromium --start-fullscreen --noerrdialogs --disable-infobars  $url &

		/usr/bin/firefox-esr -url $url &
		
		sleep 5

		xdotool search --sync --onlyvisible --class "Firefox" windowactivate key F11

		while true; do
        	sleep 10000
		done

#fi

