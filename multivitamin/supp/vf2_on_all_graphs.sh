#!/bin/bash

#tries a python script on all graphs in graphs/ and puts the output in test_run.txt

#put the script to test after the bash script like './try_on_all_graphs.sh parser.py'
#maybe the script must be made executable first: 'chmod +x try_on_all_graphs.py'

stats=./vf2/VF2_stats.txt
echo > $stats

for file in *_1.graph
do

  base=$(basename $file | cut -d "_" -f 1,2)
  one=$base'_1.graph'
  two=$base'_2.graph'
  temp=./vf2/$file'_time.temp'

  out=./vf2/VF2_$file.txt

  if [ -a $out ]
    then
      echo "deleting $out"
      rm $out
  fi

  #not using built-in time command, because it's not accurate, so it seems. Using GNU time which (as of now) shows the real clock time in seconds
  echo "Processing files '$one' and '$two'..."
  /usr/bin/time -f "%e" python $1 $one $two 1>> $out 2>> $temp #saving the time here in temp because it is needed in 2 different files
  echo >> $out
  cat $temp >> $out
  echo >> $out
  echo >> $out
     
  echo -n $(basename $file | cut -d "_" -f 1) >> $stats
  echo -ne "\t" >> $stats
  cat $temp >> $stats

  rm $temp
done

echo "Done."
