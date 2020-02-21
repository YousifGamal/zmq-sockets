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
    consumer1Counter=$consumerCount
    echo $consumer1Counter
    while [ $consumer1Counter -gt 0 ]
    do
        echo $consumer1Counter
        nohup python consumer1.py $consumer1Counter &
        consumer1Counter=$(( $consumer1Counter - 1 ))
    done
    # collector1Counter = $(( $collector1Counter / 2 ))
    # if [ $(( $collector1Counter % 2 )) -eq 0]
    # then
    #     collector1Counter = $(( $collector1Counter + 1 ))
    # fi
    # while [ $collector1Counter -gt 0 ]
    # do
    #     python collector1.py $collector1Counter
    #     collector1Counter=$(( $collector1Counter - 1 ))
    # done

#machine 2
# else
fi

# consumerCounter = $consumerCount
# collector1Port = 5400
# while [ $consumerCounter -gt 0 ]
# do
#     python consumer1.py $ip $collector1Port
#     consumerCounter=$(( $consumerCounter - 1 ))
#     if [$(( $consumerCounter % 3 )) -eq 0]
#     then 
#         collector1Port =$(( $collector1Port + 1 ))
#     fi

# done