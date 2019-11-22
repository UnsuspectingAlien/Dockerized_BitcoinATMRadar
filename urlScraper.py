import re
import os
import sys
#import os
import time
import dataCollector
'''
This function takes structured HTML and outputs a text file containing a list of harvested URLs that need to be followed.
'''
def harvestCityLinks(file, outdir):
    locationCount = 1
    stateList = ["Alabama", "Arizona", "Arkanzas", "California", "Colorado", "Connecticut",
                 "Delaware", "Florida", "Georgia", "Hawai", "Idaho", "Illinois", "Indiana",
                 "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
                 "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada",
                 "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio",
                 "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
                 "Tennessee", "Texas", "Utah", "Virginia", "Washington", "Washington D.C.", "Wisconsin"]
    State = ""
    outputDirectory = ""
    with open(file) as htmlFile:
        print(htmlFile.name)
        for line in htmlFile:
            match = re.search(r'href=[\'"]?([^\'" >]+)', line)
            if match:
                #print("The line is: " + line)

                try:
                    if stateList[0] in line:
                        #print("City Found SETTING OuputDir")
                        #print(stateList)
                        State = stateList[0]
                        outputDirectory = os.path.join(outdir, State)
                        #outputDirectory = "Unimportant_HTML/" + State + "/"
                        #print("CITY FOUND SETTING OutputDir to: " + outputDirectory)
                        stateList.pop(0)
                except IndexError as e:
                    pass

                #print("########### Writting to the file for " + State + "###################")
                noequal = match.group(0).split('=')
                slash = noequal[1].split('/')
                #locationCount = locationCount + 1
                try:
                    if slash[1] == 'city':
                        # print (noequal[1][1:])
                        outFile = State+'_links.txt'
                        outPath = os.path.join(outputDirectory, outFile)
                        with open(outPath, 'a+') as outputFile:
                            if "promo/go/?u" in line:
                                pass
                            else:
                                print("Writting To The Output File ---> " + outPath)
                                outputFile.write(noequal[1][1:] + "\n")


                except IndexError as e:
                    print(e)

        #print("################################# Remove Dups From:" + outputDirectory + "/" + outFile)
        #removeDups(outFile, outputDirectory)
        return
'''
This funciton also harvests URLs from a structured HTML file but it specifically looks for the ATM links which is what we are mostly after.
'''
def harvestATMLinks(file, outputDir):
    locationCount = 0
    with open(file) as htmlFile:
        print(htmlFile.name)
        for line in htmlFile:
            if 'Details' in line:
                # print (line)
                match = re.search(r'href=[\'"]?([^\'" >]+)', line)
                noequal = match.group(0).split('=')
                # print(match.group(0))
                slash = noequal[1].split('/')
                locationCount = locationCount + 1
                try:
                    with open(os.path.join(outputDir, 'allATMs.txt'), 'a+') as outFile:
                        print("OUTPUT FILE IS: " + os.path.join(outputDir, 'allATMs.txt'))
                        if "promo/go/?u" in line:
                            pass
                        else:
                            outFile.write(noequal[1][1:] + "\n")
                            print(noequal[1][1:])
                except IndexError as e:
                    print(e)
        #removeDups('allATMs.txt', outputDir)
    return
        # print(match.group(0))

'''
This is a utility function that assists in removing any duplicatel URLs that are collected.
'''
def removeDups(outdir):
    dupcount = 0
    #outfile = ""
    for dirName, subdirList, fileList in os.walk(outdir):
        print ("Currently In: " + dirName)
        for fname in fileList:
                if ".txt" in fname:
                    dupCount = 0
                    noExt = fname.split(".")[0]
                    #print(noExt)
                    lines_seen = set() # holds lines already seen
                    outFile = str(noExt) + "_noDups.txt"
                    inFile = os.path.join(dirName,fname)
                    #print(outFile)
                    #print(dirName)
                    print("outpath is ---->" + dirName + "/" + outFile)
                    outfile = open(os.path.join(dirName, outFile), "w")
                    for line in open(inFile, "r"): #Test2/Alabama/allATMs.txt
                        if line not in lines_seen: # not a duplicate
                            outfile.write(line)
                            lines_seen.add(line)
                        else:
                            dupCount = dupCount + 1
                    outfile.close()
            #print("Duplicate FOUND")
        #outfile.close()
                    print("THERE WERE " + str(dupCount) + " DUPLICATES FOUND IN -- " + str(fname))

def printHello():
	#print("Hello! Your call worked!")
	return "IT_WORKED_DUDE"
