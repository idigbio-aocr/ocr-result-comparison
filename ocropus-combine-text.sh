#!/bin/bash

i=$1
o=$2

cat `ls $i/*.txt | sort` > $o.ocropus.bin.txt || touch $o.ocropus.bin.txt