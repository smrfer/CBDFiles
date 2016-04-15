import numpy as n, sys, os
#directory = '/home/sr/ValidationDataTest/SoftClip/0rounds/CorMal//'
#directory = '/home/sr/ValidationDataTest/SoftClip/3rounds/CorMal//'
#directory = '/home/sr/ValidationDataTest/SoftClip/0rounds/Epilepsy//'
#directory = '/home/sr/ValidationDataTest/SoftClip/3rounds/Epilepsy//'
#directory = 'E:\TestTrimStatsData\Epilepsy\\'
#directory = 'H:\TestTrimStatsData\Epilepsy\\'
#directory = 'E:\SoftClip\\0rounds\CorMal\\'
#directory = 'E:\SoftClip\\3rounds\CorMal\\'
#directory = 'E:\SoftClip\\0rounds\Epilepsy\\'
directory = 'E:\SoftClip\\3rounds\Epilepsy\\'
files = os.listdir(directory)
fnsuffix = directory.split('\\')
#print fnsuffix
fnsuffix = fnsuffix[(len(fnsuffix)-3)] + '_' + fnsuffix[(len(fnsuffix)-2)] #Fix this line
#print fnsuffix
#fnsuffix = 'EpilepsyTest'
#outdir = 'E:\TestTrimStatsData\\'
#outdir = 'H:\TestTrimStatsData\\'
outdir = 'E:\\'
arr = []
filenames = []
dictionary = {}
firstout = {}
secondout = {}
thirdout = {}
if os.path.isfile(outdir + fnsuffix + '_clipstats.tsv'):
	print "Clipstats file exists. Deleting previous file."
	open(outdir + fnsuffix + '_clipstats.tsv', 'w').close()
for fnidx,fn in enumerate(files):
    try:
	print "Working on " + fn
	splitfile = fn.split('_')
	if len(splitfile) == 4 and splitfile[3] == "001.sorted.txt":
	    err = None
	else:
	   err = splitfile[6].split('.')
	   err = err[0]+'.' + err[1]
    except:
        raise Exception ("file with unsupported naming format")
    #Will open file in same location as script
    outfile = open(outdir + fnsuffix + '_clipstats.tsv', 'a')
    #Header line of what is in each column created by if clause- comment out if not required
    ##if fnidx == 0:
        ##outfile.write("filename\terror rate\ttotal clip events\ttotal reads\n") 
    num_clip_events = []
    with open(directory + fn) as infile:
	for lineno,line in enumerate(infile):
		#skip the header line
		if lineno == 0:
			continue
		else:
			line = line.split('\t')
			num_clip_events.append(float(line[2]))
	
	#Total clip events, Total reads, per filename (so per file)
	arr.insert(fnidx, [n.sum(num_clip_events), (lineno)])
	#Write out the filename, total number of reads per filename and total number of clip events
	##outfile.write(fn + '\t') #Write out filename
	##outfile.write(str(err) + '\t') #Write out error rate CutAdapt used
	##outfile.write(str(n.sum(num_clip_events)) + '\t') #Write out number of clip events over all reads
	##outfile.write(str(lineno) + '\n') #Write out total number of reads in sample
	#Find a list of samplenumbers to iterate over later
	filenames.append(splitfile[0])
	#Store the required data in a dictionary with a tuple as a key
	dictionary[(splitfile[0],err)] = [n.sum(num_clip_events), (lineno)]
	
    #print type(fnidx)	
#print arr
#print dictionary
uniquefilenames = list(set(filenames))
#print uniquefilenames
#values = [dictionary[key] for key in dictionary.keys() if key[0] == '11M01522']
#print "whatever is " + str(values)

##Write header line for second lot of output
outfile.write("filename\terror rate\tclip events iterative subtraction\titerative clip normalised\n")

for filename in uniquefilenames:
    baseline = [dictionary[key] for key in dictionary.keys() if key[0] == filename and key[1]== None]
    #baseline = (dictionary[key] for key in dictionary.keys() if key[0] == '11M01522' and key[1]== None)
    #print baseline
    #print baseline[0][0] #Total number of trimming events for that filename at base
    for i in xrange(0, 35, 5):
        trimerr = "%0.2f" %(i/100.0)
        #print str(i)
        errorstrim = [dictionary[key] for key in dictionary.keys() if key[0] == filename and key[1]== trimerr]
        try:
            firstout[trimerr] = (baseline[0][0] - errorstrim[0][0])
            #Write out the result to this calculation here (baseline-errorstrim)
            ##outfile.write("filename\terror rate\tclip events from baseline\n")  #Header line
            ##outfile.write(filename + '\t') #Write out filename
            ##outfile.write(trimerr + '\t') #Write out trim error rate
            ##outfile.write(str(baseline[0][0] - errorstrim[0][0]) + '\n') #Write out clip events for baseline-error rates 

        except:
            continue
    for i in xrange(30,-5, -5):
        trimerr = "%0.2f" %(i/100.0)
        #print trimerr
        itersub = [dictionary[key] for key in dictionary.keys() if key[0] == filename and key[1]== trimerr]
        #print str(i)
        try:
            if i == 30:
                #print "The first stored"
                index = trimerr #i
                #print index
                firstone = itersub[0][0]
                firstonenorm = (itersub[0][0]/itersub[0][1])
                #print firstone
            else:
                #print (itersub[0][0] - firstone)
                secondout[index] = (itersub[0][0] - firstone)
                second = (itersub[0][0] - firstone)
                thirdout[index] = ((itersub[0][0]/itersub[0][1]) - firstonenorm)
                third = ((itersub[0][0]/itersub[0][1]) - firstonenorm)
                firstone = itersub[0][0]
                firstonenorm = (itersub[0][0]/itersub[0][1])
                #Write out the result to these calculations here
                #print second
                outfile.write(filename + '\t') #Write out filename
                outfile.write(index + '\t') #Write out trim error rate
                outfile.write(str(second) + '\t') #Write out clip events for iterative subtraction
                outfile.write(str(third) + '\n') #Write out clip events for normalised iterative subtraction
                index = trimerr #i
        except:
            continue
    #print dictionary
    #print firstout
    #print secondout
    #print thirdout
outfile.close()


    
	
	

