#!/bin/bash
#Pass in directory as first system argument and filename as second system argument
BaseDir=${1}
Filename=${2}
maxTrim=${3}
OutputDir=$BaseDir"Output/"
div=100
#dv=(div/10)

#Trimming the reverse reads
for (( i = 0; i <= ${maxTrim}; i+=5))
do
 	inc=$(awk -v dividend="${i}" -v divisor="${div}" 'BEGIN {printf "%.2f",dividend/divisor; exit(0)}')
	#nm=$(awk -v dividend="${i}" -v divisor="${div}" 'BEGIN {printf "%.2f",dividend/divisor; exit(0)}')

#Trimming with CutAdapt on the simulated data
	echo "Running CutAdapt on" $Filename".bed.rev.fasta"
	/home/sara/Documents/cutadapt-1.8.1/bin/cutadapt \
		-a AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT \
		--minimum-length 30 \
		-e $inc \
		-o ""$OutputDir$Filename"_trimmed_"$inc".bed.rev.fasta" \
			""$BaseDir$Filename".bed.rev.fasta" \
			&>""$OutputDir$Filename"_trimmed_"$inc"_CAlog.rev.txt"
	echo "CutAdapt step completed"

	#Pass in trimmed output from previous step to CAOutputFA script
	#Need to fix this to take in the .rev files
	#echo "$1.bed.fasta"
	#echo "$1_trimmed_$inc.bed.fasta"
	python "/home/sara/Dropbox/000LINUX/Trimming/CAOutputFA.py" "$BaseDir" \
								"$OutputDir" \
								""$Filename".bed.rev.fasta" \
								""$Filename"_trimmed_"$inc".bed.rev.fasta"
	echo "Finding differences completed"
	
	#Pass in output from previous step to the ParseCAFAOutfile script
	trim=`python "/home/sara/Dropbox/000LINUX/Trimming/ParseCAFAOutfile.py" "$OutputDir" \
								""$Filename"_trimmed_"$inc"_differences.rev.txt"`
	echo "Trimmed bases counted"
	#echo $trim > "trimmed.txt"
	echo $trim
done
