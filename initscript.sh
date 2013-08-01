! /bin/sh
# /etc/init.d/ampel
#

# Some things that run always
touch /var/lock/ampel

# Carry out specific functions when asked to by the system
case "$1" in
	start)
		screen /home/pi/ampel/ampelwebserver.py >> /var/log/ampel.log 2>> /var/log/ampel.log
		;;
	stop)
		echo "Stopping script blah"
		echo "Could do more here"
		;;
	*)
		echo "Usage: /etc/init.d/blah {start|stop}"
		exit 1
		;;
esac

exit 0