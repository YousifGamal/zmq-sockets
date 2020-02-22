#!/bin/sh

#to rum ./testscript.sh 3 

#defines a variable called num and takes the first value
#passed to the script from the cmd
mode=$1 #1 for machine 1 or 2 machine 2
ip=$2 #ip address of machine 1
consumerCount=$3 #no. of consumers

videoName=$4 #name of the video

#machine 1
if [ $mode -eq 1 ]
then
    
    python producer.py $videoName &

    collector1Counter=$(( $consumerCount / 2 ))
    echo $collector1Counter

    if [ $(($consumerCount%2)) -eq 1 ]
    then
        collector1Counter=$(( $collector1Counter + 1 ))
    fi
    echo $collector1Counter
    while [ $collector1Counter -gt 0 ]
    do
        python collector.py $collector1Counter $ip &
        collector1Counter=$(( $collector1Counter - 1 ))
    done


    consumer1Counter=$consumerCount
    while [ $consumer1Counter -gt 0 ]
    do
        python consumer1.py $consumer1Counter &
        consumer1Counter=$(( $consumer1Counter - 1 ))
    done


#machine 2
else

    python collector2.py $collector2Counter &

    consumer2Counter=$consumerCount
    while [ $consumer2Counter -gt 0 ]
    do
        python consumer2.py $consumer2Counter $ip &
        consumer2Counter=$(( $consumer2Counter - 1 ))
    done

fi

