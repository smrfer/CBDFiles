#!/bin/sh
#Converts co-ordinates in a bed file into a fasta

BED="/home/sara/Dropbox/000LINUX/HaloPlexBED/19540-1409129995_CorMal.bed"
fastaFromBed -fi hg19.fa -bed $BED -fo $BED.fasta

