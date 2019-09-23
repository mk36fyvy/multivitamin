#!/bin/bash

#tries a python script on all graphs in graphs/ and puts the output in test_run.txt

#put the script to test after the bash script like './try_on_all_graphs.sh parser.py'
#maybe the script must be made executable first: 'chmod +x try_on_all_graphs.py'


out=run_test_on_$1.txt

if [ -a $out ]
  then
    echo "deleting run_test.txt"
    rm $out
fi


touch $out


for file in ~/git/graph_alignment/graphs/*.graph
do
  echo "Processing file '$file'"
  python $1 "$file" >> $out
  echo >> $out
  echo >> $out
  echo >> $out
done

echo "Done."
