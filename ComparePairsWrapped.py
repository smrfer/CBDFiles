import sys
'''
Usage: <scriptname> <directory containing both fastq files> <first fastq file (must be R1)> <second fastq file (must be R2)> 
If R1 and R2 are entered the wrong way then the script will not work. There is no check for this at present.
'''
directory = sys.argv[1]
file1 = sys.argv[2]
file2 = file1.split('_')
file2[3] = "R2"
file2 = "_".join(file2)
#file2 = "7M2813_S1_L001_R2_001_FILTERED_CA_0.15.fastq"
file1in = open(directory+file1)
file2in = open(directory+file2)

f1 = []
f2 = []    
#print "ComparePairs is running for "+ file1+ ":"
for line1 in file1in:
        if line1[0] == '@':
            l1len = len(line1)
            #find the part of the string where need to insert the 2 robustly
            strn = line1.split()
            #catches the case where the @ is in another line (probably quality) other than the header
            try:
                strn[1] = '2' + strn[1][1:len(strn[1])]
                line12 = " ".join(strn)
                f1.append(line12.rstrip())
            except:
                continue
                #print line1
#print "Number of reads in R1 = " + str(len(f1))
for line2 in file2in:
        if line2[0] == '@':
            strn2 = line2.split()
            try:
                strn2[1]
                f2.append(line2.rstrip())
            except:
                continue
                #print line2
#print "Number of reads in R2 = " + str(len(f2))
comparator = cmp(f1,f2)
if cmp(f1,f2) == 0:
    #print 'Reads are paired'
    pass
else:
    unpairedoutput = open(directory+file1+"_unpairedoutput.txt", 'w')
    unpairedlog = open(directory+"unpairedfiles.txt", 'a')
    unpairedlog.writelines("File: " + file1 + "\n")
    unpairedlog.writelines('WARNING: Unpaired reads in files\n')
    unpairedlog.writelines(str(len(set(f1)-set(f2)))+" in R1 than aren't in R2\n")
    unpairedlog.writelines(str(len(set(f2)-set(f1)))+" in R2 that aren't in R1\n")
    unpairedoutput.write("UNPAIRED READS\n")
    unpairedoutput.write("READ 1\n")
    for element in (set(f1) - set(f2)):
        element = element.split()
        element[1] = '1' + element[1][1:len(element[1])]
        element = " ".join(element)
        unpairedoutput.write(element + "\n")
    unpairedoutput.write("READ 2\n")
    for element in (set(f2) - set(f1)):
        unpairedoutput.write(element + "\n")
