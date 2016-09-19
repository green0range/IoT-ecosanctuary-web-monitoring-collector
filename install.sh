#! /bin/bash

echo "This script will automatically install the collector system to this device."
echo "Note that this is designed to be used on a debian or debian based OS. It will"
echo "also need root permissions, so if you have not run this with sudo, it will fail."
echo "Continue? y/n."
read cont
if [ "$cont" == "y" ]; then
	echo "We just need to setup the config file"
	echo "What protcol will the server be using? (eg HTTP://)"
	read prot
	echo "What is the server domain address? (eg greenorange.space)"
	read dom
	echo "What is the submit path? (eg /orokonui/resource/datahandling/submit.php"
	read sub
	echo "What is the submit code?"
	read code
	echo "Generating sensor.config..."
	echo "PROTOCOL:" prot > sensor.config
	echo "DOMAIN:" dom >> sensor.config
	echo "PATH:" sub >> sensor.config
	echo "CODE:" code >> sensor.config
	echo "Done. Generating startup script..."
	echo "#! /bin/bash" > /etc/init.d/collector_startup.sh
	echo "$(pwd)/run.sh" >> /etc/init.d/collector_startup.sh
	chmod 755 /etc/init.d/collector_startup.sh
	update-rc.d collector_startup.sh defaults
	echo "Done. Installation complete."
	
else
	echo "Quiting.."
fi
