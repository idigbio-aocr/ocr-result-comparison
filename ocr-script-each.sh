#!/bin/bash

i=$1
o=$2

if test -e $i.bin.png; then
    pngtopnm $i.bin.png | ocrad -F utf8 > $o.ocrad.bin.txt
    pngtopnm $i.bin.png | gocr -f UTF8 -i - > $o.gocr.bin.txt
    tesseract $i.bin.png stdout > $o.tesseract.bin.txt        
else
    touch $o.ocrad.bin.txt
    touch $o.gocr.bin.txt
    touch $o.tesseract.bin.txt
fi

djpeg -greyscal -pnm $i.jpg | ocrad -F utf8 > $o.ocrad.txt
djpeg -greyscal -pnm $i.jpg | gocr -f UTF8 -i - > $o.gocr.txt
tesseract $i.jpg stdout > $o.tesseract.txt