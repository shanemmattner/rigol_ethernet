#!/bin/bash
#Script to copy the current DB to a USB stick

myfilesize=$(wc -c "/home/pi/rigol_ethernet/g3v2_motor_drive_signals.db" | awk '{print $1}')
echo "$myfilesize"

if [ $myfilesize -gt 10000000 ]
then
	echo file over 10MB
	#turn off the cycle testing and wait 10 seconds to let all tests finish
	t_running=`cat run_testing.txt`
	echo "$t_running"
	echo "0" > run_testing.txt
	sleep 5
	mount -t vfat -o rw /dev/sda /home/pi/rigol_ethernet/usb
	now=$(date +"%d-%b-%Y-%H-%M")
	cp /home/pi/rigol_ethernet/g3v2_motor_drive_signals.db /home/pi/rigol_ethernet/usb/g3v2_motor_drive_signals_$now.db
	rm /home/pi/rigol_ethernet/g3v2_motor_drive_signals.db
	if [ $t_running == 1 ]
	then
		echo "1" > run_testing.txt
	fi
	sleep 1


else
	echo file not over 100KB
fi
exit
