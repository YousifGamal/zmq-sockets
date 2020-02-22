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
    
    nohup python producer.py $videoName &

    collector1Counter=$(( $consumerCount / 2 ))
    if [ $(($collector1Counter%2)) -eq 0 ]
    then
        collector1Counter = $(( $collector1Counter + 1 ))
    fi
    while [ $collector1Counter -gt 0 ]
    do
        nohup python collector.py $collector1Counter $ip &
        collector1Counter=$(( $collector1Counter - 1 ))
    done


    consumer1Counter=$consumerCount
    while [ $consumer1Counter -gt 0 ]
    do
        nohup python consumer1.py $consumer1Counter &
        consumer1Counter=$(( $consumer1Counter - 1 ))
    done


#machine 2
else
    collector2Counter=$(( $consumerCount / 2 ))
    if [ $(( $collector2Counter % 2 )) -eq 0 ]
    then
        collector2Counter = $(( $collector2Counter + 1 ))
    fi
    while [ $collector2Counter -gt 0 ]
    do
        nohup python collector2.py $collector2Counter &
        collector2Counter=$(( $collector2Counter - 1 ))
    done

    consumer2Counter=$consumerCount
    while [ $consumer2Counter -gt 0 ]
    do
        nohup python consumer2.py $consumer2Counter $ip &
        consumer2Counter=$(( $consumer2Counter - 1 ))
    done

fi

