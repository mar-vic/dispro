#!/bin/bash

file_to_copy="danko_a_janko__vansova__neografia.xml"
x=0

for n in 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 
do
    x=$(($x+1))
    echo "Copying $file_to_copy to danko_a_janko__vansova__neografia__$x.xml"
    cp $file_to_copy "danko_a_janko__vansova__neografia__$x.xml"
done
