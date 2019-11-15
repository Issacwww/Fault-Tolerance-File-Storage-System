#!/bin/bash

client_num=100

for i in `seq 51 $client_num`
do
    python client.py $i c
    for file_num in {1..9}
    do
        python client.py $i a $file_num
        python client.py $i r $file_num
    done
    python client.py $i d
    python client.py $i s
done