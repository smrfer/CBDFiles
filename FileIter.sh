#!/bin/bash
#Directory could be set as a sysarg if needed
Directory="/home/sara/Dropbox/000LINUX/Trimming/Fastas/"
#Set the maximum amount of error rate to go for (actual rate wanted /100)- could change this to calc with awk if need
err="50"
#Clear the text in the log of the trimmed bases
cat /dev/null > ""$Directory"Output/trimming.txt"
for fasta in "$Directory"*.fasta; do
	#echo $fasta
	filename=$(basename "$fasta")
	#echo $filename
	#source TrimmingSimData.sh
	xpref=${filename%.*}
	#echo $xpref
	xlot=${xpref##*.}
	xfn=$(basename "$xpref")
	#echo $xfn
	fn=${xfn%.*}
	#echo $xlot
	if [[ "$xlot" == "rev" ]]; then
		fn=${fn%.*}
		echo "Initiating trimming for "$filename""		
		source TrimmingSimDataR.sh "$Directory" "$fn" "$err"
	elif [[ "$xlot" == "bed" ]]; then
		echo "Initiating trimming for "$filename""	
		source TrimmingSimDataF.sh "$Directory" "$fn" "$err"
	else echo "error"
	fi
done

