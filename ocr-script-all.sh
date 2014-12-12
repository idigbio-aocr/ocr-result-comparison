#!/bin/bash

corecount=$(cat /proc/cpuinfo | grep processor | wc -l)

./versions.sh

# Generate Bin Images
ls images/ | xargs -I[] -P$corecount ocropus-nlbin -n images/[]\

# Run Ocropus
ls images/ | sed 's/\([^\.]*\)\..*$/\1/' | sort -u | xargs -I[] -P$corecount ocropus-gpageseg images/[].bin.png
ls images/ | sed 's/\([^\.]*\)\..*$/\1/' | sort -u | xargs -I[] -P$corecount ocropus-rpred "images/[]/??????.bin.png"
ls images/ | sed 's/\([^\.]*\)\..*$/\1/' | sort -u | xargs -I[] -P$corecount ./ocropus-combine-text.sh images/[] output/[]

# Generate OCR
ls images/ | sed 's/\([^\.]*\)\..*$/\1/' | sort -u | xargs -I[] -P$corecount ./ocr-script-each.sh images/[] output/[]