#!/bin/bash

r=$1
s=0
shift 1
echo "Running $* $r times"
mkdir -p logs

for i in $(seq $r)
do
    echo "Starting run $i/$r"
    $* >> logs/run_$i.txt
    if [ $? -eq 0 ]
    then
        s=$((s + 1))
        echo "Finished run $i/$r"
        echo "Success rate is $s/$i"
        echo `tail -n 2 logs/run_$i.txt`;
    else
        echo "Run $i/$r failed"
        exit 1;
    fi
done
