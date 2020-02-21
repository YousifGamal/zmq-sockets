#!/bin/sh

#to rum ./testscript.sh 3 

#defines a variable called num and takes the first value
#passed to the script from the cmd
num=$1

#while loop in num -gt -> (greater)
while [ $num -gt 0 ]
do
    python consumer.py a7a
    num=$(( $num - 1 ))
done