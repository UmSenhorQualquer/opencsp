# PEDINGPID=`cat pid.txt`
# kill -9 $PEDINGPID;
# if [ -f pending_PID.txt ]
# then
# 	PEDINGPID=`cat pending_PID.txt`
# 	kill -9 $PEDINGPID;
# fi
# if [ -f busy.yes ]
# then
# 	mv busy.yes busy.no
# fi
for line in $(cat pid.txt)
do
	kill -9 $line
done

if [ -f pending_PID.txt ]
then
	for line in $(cat pending_PID.txt)
	do
		kill -9 $line
	done
fi

if [ -f busy.yes ]
then
	mv busy.yes busy.no
fi