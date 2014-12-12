from __future__ import division
import nltk
import pprint
from difflib import SequenceMatcher
import os
import numpy
import json
import csv

#filename = "WIS-L-0012069_lg.txt"

pct_corrects = []
ratios = []

ocrs = ["abbyy.bin","abbyy","gocr","gocr.bin","ocrad", "ocrad.bin","ocropus.bin","tesseract","tesseract.bin"]


results = {}
for o in ocrs:
    results[o] = {}

for root, dirs, files in os.walk("human/"):       
    for filename in files:
        human_tokens = None
        with open("human/{0}".format(filename),'rb') as human:    
            human_tokens = nltk.word_tokenize(human.read().decode("utf8"))

        s = SequenceMatcher()
        s.set_seq1(human_tokens)
        
        for o in ocrs:               
            ocr_tokens = None
            with open("output/{1}.{0}.txt".format(o,filename[:-4]),'rb') as ocr:
                ocr_tokens = nltk.word_tokenize(ocr.read().decode("utf8"))
                
            s.set_seq2(ocr_tokens)

            matches = 0
            for (i, j, n) in s.get_matching_blocks():
                matches += n

            results[o][filename] = {}
            results[o][filename]["pctcor"] = 100*(matches/len(human_tokens))
            results[o][filename]["ratio"] = 100*s.ratio()
            
#pprint.pprint(results)

files = {}
ocrs = {}
for o in results:
    for f in results[o]:
        if not (o in ocrs):
            ocrs[o] = {"pctcor": [], "ratio": [], "points": {"pctcor": 0, "ratio": 0}}
        ocrs[o]["pctcor"].append(results[o][f]["pctcor"])
        ocrs[o]["ratio"].append(results[o][f]["ratio"])
        
        if not (f in files):
            files[f] = {}
        files[f][o] = {}
        files[f][o]["pctcor"] = results[o][f]["pctcor"]
        files[f][o]["ratio"]= results[o][f]["ratio"]

points_assignment = {
}
for i,_ in enumerate(ocrs):
    points_assignment[i] = len(ocrs) - i - 1


for f in files:
    pctcor_scores = []
    ratio_scores = []
    for o in ocrs:
        pctcor_scores.append((files[f][o]["pctcor"],o))
        ratio_scores.append((files[f][o]["ratio"],o))
    pctcor_scores = sorted(pctcor_scores,key=lambda x: x[0],reverse=True)
    ratio_scores = sorted(ratio_scores,key=lambda x: x[0],reverse=True)
    for p in points_assignment:
        ocrs[pctcor_scores[p][1]]["points"]["pctcor"] += points_assignment[p]
        ocrs[ratio_scores[p][1]]["points"]["ratio"] += points_assignment[p]


stats = { "ocrs": {}, "files": files}
for o in ocrs:
    pctcor = numpy.array(ocrs[o]["pctcor"])
    ratio =  numpy.array(ocrs[o]["ratio"])
    (pn, pbins) = numpy.histogram(pctcor, 10, [0,100])
    (rn, rbins) = numpy.histogram(ratio, 10, [0,100])
    stats["ocrs"][o] = {
        "pctcor": {
            "median": float(numpy.median(pctcor)),
            "average": float(numpy.average(pctcor)),
            "stddev": float(numpy.std(pctcor)),
            "range": [float(numpy.amin(pctcor)), float(numpy.amax(pctcor))],
            "hist": [[ int(x) for x in pn ], [float(x) for x in pbins]]
        },
        "ratio": {
            "median": float(numpy.median(ratio)),
            "average": float(numpy.average(ratio)),
            "stddev": float(numpy.std(ratio)),
            "range": [float(numpy.amin(ratio)), float(numpy.amax(ratio))],
            "hist": [[ int(x) for x in rn ], [float(x) for x in rbins]]
        },
        "points": ocrs[o]["points"]
    }

with open("ocr-stats.json","wb") as outf:
    json.dump(stats,outf,indent=4)

with open("ocr-stats.csv","wb") as outf:
    cw = csv.writer(outf)

    ha = ["filename"]
    for o in ocrs:
        ha.append(o+"_pctcor")
        ha.append(o+"_ratio")

    cw.writerow(ha)

    
    for f in files:
        fa = []
        fa.append(f)
        for o in ocrs:
            fa.append(files[f][o]["pctcor"])
            fa.append(files[f][o]["ratio"])
        cw.writerow(fa)

with open("points.csv","wb") as outf:
    cw = csv.writer(outf)

    cw.writerow(["engine","pctcor_score","ratio_score"])
    for o in ocrs:
        cw.writerow([o,ocrs[o]["points"]["pctcor"],ocrs[o]["points"]["ratio"]])
