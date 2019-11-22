from urlScraper import harvestCityLinks, harvestATMLinks, removeDups
from dataCollector import collect, seleniumCollect
from detailExtractor import getDetails, buildCSV, aggregateCSV
import os
import time
import subprocess
import sys
#import time
from datetime import datetime



def purgeDir():
    #rootdir = "/home/cs/PycharmProjects/RadarScraper/Unimportant_HTML/"
    rootdir = "/home/cs/PycharmProjects/RadarScraper/States"
    #rootdir = "/home/cs/PycharmProjects/RadarScraper/Test2"
    for dirName, subdirList, fileList in os.walk(rootdir):
        # print ("Currently In: " + dirName)
        for fname in fileList:
            if ".json" in fname or ".csv" in fname:
                print("Deleting: " + os.path.join(dirName,fname))

                subprocess.call('rm -r ' + '"' + os.path.join(dirName,fname) + '"', shell=True)
                # state = dirName.split("/")[1]
                # print(state)
                # print(os.path.join(outputdir,dirName.split("/")[1]+"/"))
def countFiles():
    #rootdir = "/home/cs/PycharmProjects/RadarScraper/Unimportant_HTML/"
    rootdir = "/home/cs/PycharmProjects/RadarScraper/States"
    totalfileCount = 0
    for dirName, subdirList, fileList in os.walk(rootdir):
        dirfileCount = 0
        print ("Currently In: " + dirName)
        for fname in fileList:
            if ".html" in fname:
                dirfileCount = dirfileCount + 1
        print("\t |_> There are " + str(dirfileCount) + " .html files in this directory")
        totalfileCount = totalfileCount + dirfileCount
    print("############## There are a total of: >>> " + str(totalfileCount) + " <<< . html site files ####################")
if __name__ == "__main__":
    #removeDups('allATMs.txt', 'Test2/Alabama')
    #purgeDir()
    #countFiles()
    #start_time = time.time()
    #start = datetime.now()
    #print("Starting Scrape at: " + str(start))

#    print("[INFO]           /\/\/\/\/\/\/\/\ Starting To Scrape All State URLs /\/\/\/\/\/\/\/")
#    #FIRST GATHER ALL THE CITY LINKS FROM ALL THE STATES
#    mainHTML = 'radarUS.html'
#    outDir = "Unimportant_HTML/"
#    harvestCityLinks(mainHTML, outDir)

    #Before Scraping Remove All Duplicate Links
#    removeDups("Unimportant_HTML/")

    #Now Call DataCollector to utilize Selenium  go out and crawl all of the CITY links found. Selenium helps get past the lazy load on the base html page. (WORKING)
#    print ("[INFO]          /\/\/\/\/\/\/\/\ Links have been gathered Time to go Scrape /\/\/\/\/\/\/\/")
#    rootdir = "Unimportant_HTML/"
#    for dirName, subdirList, fileList in os.walk(rootdir):
#        print ("Currently In: " + dirName)
#        for fname in fileList:
#            if "_noDups.txt" in fname:
#               print(dirName)
#               print(fname)
#               seleniumCollect(os.path.join(dirName, fname), dirName)

#    #NOW GO THROUGH ALL THE HTML AND GATHER ALL LINKS FOR EACH INDIVIDUAL BTC ATM SITE (WORKING)
#    print("[INFO]          /\/\/\/\/\/\/\/\ Extracting All ATM Site URLs /\/\/\/\/\/\/\/")
#    rootdir = "Unimportant_HTML/"
#    outputdir = "States/"
#    for dirName, subdirList, fileList in os.walk(rootdir):
#        print ("Currently In: " + dirName)
#        for fname in fileList:
#            if ".html" in fname:
#                print("File name is: " + fname)
#                state = dirName.split("/")[1]
#                print(state)
#                print("The PATH IS: " + os.path.join(outputdir,dirName.split("/")[1]+"/"))
#                harvestATMLinks(os.path.join(dirName,fname),os.path.join(outputdir,dirName.split("/")[1]+"/"))
        # print(dirName)



     #Remove Duplicates before crwaling
#    removeDups("States/")
#    #Now Call DataCollector to go out and crawl all of the SITE links found (WORKING)

#    print ("[INFO]          /\/\/\/\/\/\/\/\ Links have been gathered Time to go Scrape /\/\/\/\/\/\/\/")
#    rootdir = "States/"
#    for dirName, subdirList, fileList in os.walk(rootdir):
#        #print ("Currently In: " + dirName)
#        for fname in fileList:
#            if "_noDups.txt" in fname:
#                print(dirName)
#                print(fname)
#                collect(os.path.join(dirName, fname), dirName)

    #EXTRACT THE PERTINENT DETAILS (!!!!!!!!!! IN DEVELOPMENT !!!!!!!!!!!!!!!!)
    rootdir = "States/"
    for dirName, subdirList, fileList in os.walk(rootdir):
        #print ("Currently In: " + dirName)
        for fname in fileList:
            if ".html" in fname:
   #     print("Time Elapsed:" + str(elapsed_time))
                #print(dirName)
                #print(fname)
                #print(os.path.join(dirName, fname))
                getDetails(os.path.join(dirName,fname))

    buildCSV(rootdir)
    aggregateCSV(rootdir)

#    elapsed_time = time.time() - start_time
#    finish = datetime.now()
#    print("Started Scrape at:" + str(start))
#    print("Finished Scrape at: " + str(finish))
#    print("Time Elapsed:" + str(elapsed_time) + "seconds")
