S1=herma582@csel-kh4250-36.cselabs.umn.edu
S2=herma582@remote08.cselabs.umn.edu

if [[ $1 = 1 ]]; then
        echo "sshing into" $S1
        ssh $S1
elif [[ $1 = "" ]]; then
        echo "sshing into" $S2
        ssh $S2
elif [[ $1 = "X" ]]; then
        echo "graphically sshing into" $S2
        ssh -X $S2
else
        echo "sshing into" $1
        ssh "herma582@"$1".cselabs.umn.edu"
fi
