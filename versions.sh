#!/bin/bash

(
    echo "GOCR";
    gocr 2>&1;
    echo;

    echo "OCRad";
    ocrad -V 2>&1;
    echo;

    echo "Tesseract";
    tesseract -v 2>&1;
    echo;

    echo "OCRopus";
    echo "https://github.com/tmbdev/ocropy.git @ bea90e4ea5d28c3be012e7dfcab0d8a995def46b";
    echo "Model: cedd140c7d7650e910f0550ad0f04727  /usr/local/share/ocropus/en-default.pyrnn.gz, obtained from http://www.tmbdev.net/en-default.pyrnn.gz on 2014/12/10"
    echo;
) > versions