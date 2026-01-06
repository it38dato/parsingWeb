#!/bin/bash
echo -n "Enter a link to the site: "
read linksite
user=$(whoami)
echo -n "Come up with a name for the directory where the files will be written: "
read linkfiles
if [ -d /home/$user/$linkfiles ]; then
		rm -rf /home/$user/$linkfiles
		echo "/home/$user/$filename delete"
else
		mkdir /home/$user/$linkfiles
		cd /home/$user/$linkfiles
		echo "/home/$user/$linkfiles create"
fi
wget --no-check-certificate -r -l 1 -A pdf $linksite
find /home/$user/$linkfiles -size +15M > output