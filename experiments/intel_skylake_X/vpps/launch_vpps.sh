#!/bin/bash

#Launch vpprouters
for (( i=1; i<3; i++))
do
	echo --------------------------------------------router$i----------------------------------------------------------------
	./vpprouter$i.conf &
	BACK_PID=$!
	wait $BACK_PID
	sleep 1
	echo
done

#Launch vpps
for (( i=1; i<9; i++))
do
	echo -----------------------------------------------vpp$i----------------------------------------------------------------
	./vpp$i.conf &
	BACK_PID=$!
	wait $BACK_PID
	sleep 1
	echo
done
