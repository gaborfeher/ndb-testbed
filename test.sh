#!/bin/bash

# curl https://2-dot-incidecoder2.appspot.com/test1 --header "X-Cloud-Trace-Context:$(tr -dc 'a-f0-9' < /dev/urandom | head -c32);o=1"; echo

for t in test1 test2; do
  SUM=0
  NUM=10
  for i in `seq 1 $NUM`; do
    VAL=$(curl https://2-dot-incidecoder2.appspot.com/$t 2>/dev/null  | sed -e 's/^.*time= //')
    echo $VAL
    SUM=$(bc -l <<< $SUM+$VAL )
  done
  echo "$t AVG: $(bc -l <<< $SUM/$NUM)"
done
