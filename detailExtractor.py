import os
import re
import csv
import json
import time
#import csv

'''
This is the main parsing engine that creates an entity JSON file per every individual BTC ATM Details page.
It uses regex and .split() to find and extract exactly the information we want. At the end of this function
the dictionary object that was created is converted to a JSON file using the buildJson() function.
'''
def getDetails(inputFile):
    print("Gathering Details")
    siteEntity = {
        'Operator':'',
        'Location':'',
        'Street':'',
        'City':'',
        'State':'',
        'Zip':'',
        'Country':'',
        'Address':'',
        'InstallDate':'',
        'Status':'',
        'UserReported_Status':'',
        'SitePhone':'',
        'OperatorPhone':'',
        'OperatingHours':'',
    }

    with open(inputFile, 'r') as htmlFile:
        for line in htmlFile:

            if "Installed on" in line:
                #print("Install Date! The line is: ")
                #print(line)
                match = re.search('>Installed on (.*)<', line)
                if match:
                    #print(match.group(1))
                    try:
                        siteEntity['InstallDate'] = match.group(1)
                    except AttributeError as e:
                        siteEntity['InstallDate'] = 'Error'

            elif "machine-status provider-status" in line:
                #print("Status! The line is:")
                #print(line)
                if 'Online' in line or 'Available' in line:
                    #print('Online')
                    try:
                        siteEntity['Status'] = 'Online'
                    except AttributeError as e:
                        siteEntity['Status'] = 'Error'
                elif 'Not reported' in line:
                    #print('Online')
                    try:
                        siteEntity['Status'] = 'Unknown'
                    except AttributeError as e:
                        siteEntity['Status'] = 'Error'
                else:
                    #print('Offline')
                    try:
                        siteEntity['Status'] = 'Offline'
                    except AttributeError as e:
                        siteEntity['Status'] = 'Error'

            elif '"machine-status">Based on user feedback' in line:
                #print("Status! The line is:")
                #print(line)
                match = re.search('">(.*)</span></div>', line)
                if match:
                    #print(match.group(1).split(">"))
                    placeholder = match.group(1).split(">")
                    #print(placeholder[len(placeholder)-1])
                    try:
                        siteEntity['UserReported_Status'] = placeholder[len(placeholder)-1]
                    except AttributeError as e:
                        siteEntity['UserReported_Status'] = 'Error'

            elif "Operator's name:" in line:
                #siteEntity['Operator'] = line
                #print("Operator Found! The line is: ")
                #print(line)
                match = re.search('target="_blank">(.*)</a>', line)
                match2 = re.search('</strong> (.*)</p>', line)#</strong> Coinsource </p>

                #print(match)
                #print(match2)
                if match:
                    #print(match.group(1))
                    try:
                        siteEntity['Operator'] = match.group(1)
                    except AttributeError as e:
                        siteEntity['Operator'] = 'Error'

                elif match2:
                    try:
                        siteEntity['Operator'] = match2.group(1)
                    except AttributeError as e:
                        siteEntity['Operator'] = 'Error'


            elif "Voice call" in line: #="tel:(786) 686-2983"><span
                #print("OPERATOR NUMBER! The line is:")
                # print(line)
                match = re.search('tel:(.*)"><span', line)
                if match:
                    #print(match.group(1))
                    try:
                        siteEntity['OperatorPhone'] = match.group(1)
                    except AttributeError as e:
                        siteEntity['OperatorPhone'] = 'Error'

            elif "Location" in line:
                #print("Location! The line is:")
                # print(line)
                match = re.search('</strong> (.*)</p>', line)
                match2 = re.search('"_blank">(.*)</a>', line)
                #match3 = re.search('</strong> (.*)</p>', line) #</strong> The Boulevard</p>
                if siteEntity['Location'] == '':
                    #print("Location is Empty you can change it")
                    if match:
                        # print(match.group(1))
                        try:
                            siteEntity['Location'] = match.group(1)
                        except AttributeError as e:
                            siteEntity['Location'] = 'Error'
                    if match2:
                        try:
                            siteEntity['Location'] = match2.group(1)
                        except AttributeError as e:
                            siteEntity['Location'] = 'Error'
                    #if match3:
                     #   try:
                      #      siteEntity['Location'] = match3.group(1)
                       # except AttributeError as e:
                        #    siteEntity['Location'] = 'Error'

            elif "Show number" in line: #class="biz-phone hidden">(205) 324-8895<br/><span
                #print("SITE NUMBER! The line is:")
                #print(line)
                match = re.search(' hidden">(.*)<br/>', line)
                if match:
                    #print(match.group(1))
                    try:
                        siteEntity['SitePhone'] = match.group(1)
                    except AttributeError as e:
                        siteEntity['SitePhone'] = 'Error'

            elif 'Address:' in line:
                address = ""
                street = ""
                statezip = ""
                country = "United States"
                #print("Address Found! The line is: ")
                #print(line)
                match = re.search('</strong><br />(.*)<br />', line)
                if match:
                    s = match.group(1)
                    #print(s)
                    #print(s.split(">")[1])
                    try:
                        street = s.split("<")[0]
                    except AttributeError as e:
                        street = 'Error'
                    try:
                        statezip = s.split(">")[1]
                    except (AttributeError, IndexError) as e:
                        statezip = 'Error'
                    try:
                        city = statezip.split(",")[0]
                    except (AttributeError, IndexError) as e:
                        city = 'Error'
                    try:
                        zip_re = re.search(r'.(\d{5}(\-\d{4})?)$', statezip)
                        zip = zip_re.group(0).lstrip()
                    except AttributeError as e:
                        zip = 'Error'
                    #print(zip)
                    #print (statezip)
                    #print(country)
                    address = street + ", " + statezip + ", " + country
                    #print(address)
                    siteEntity['Street'] = street
                    siteEntity['City'] = city
                    siteEntity['State'] = inputFile.split("/")[1]
                    siteEntity['Zip'] = zip
                    siteEntity['Country'] = country
                    siteEntity['Address'] = address

            elif "Open hours" in line:
                match = re.search('<span>(.*)</span>', line)
                if match:
                    #print(match.group(1))
                    siteEntity['OperatingHours'] = match.group(1)
    print(siteEntity)

    #print("\n\n")
    if "Washington D.C." in inputFile:
        placeholder = inputFile.split("/")
        filePath = placeholder[0]+"/"+placeholder[1]
        file = placeholder[2].split(".")[0]
        #print(file)
        completePath = os.path.join(filePath, file)
        #print("Sending Parameter: " + completePath+ "\n\n")
        buildJson(completePath, siteEntity)

    else:
        print("\n\nABOUT TO BUILD JSON FILE FROM: ")
        print(inputFile)
        print("Sending Parameter: " + inputFile.split(".")[0] + "\n\n")
        buildJson(inputFile.split(".")[0], siteEntity)
'''
This is a utility function for the parseDetails() function. It takes a file name and a dictionary object and outputs an equivalent JSON file.
'''
def buildJson(filename, dictionary):
    outfile = filename+".json"
    print("Building Thi JSON FILE: " + outfile)
    with open(outfile, 'a+') as entityjson:
        json.dump(dictionary, entityjson)

'''
This function is used to build a CSV from a JSON file.
'''
def buildCSV(rootdir):
    for dirName, subdirList, fileList in os.walk(rootdir):
        print ("Currently In: " + dirName)
        state = dirName.split("/")[1]
        count = 0
        for fname in fileList:
            if ".json" in fname:
                infile = os.path.join(dirName, fname)
                outfile = os.path.join(dirName, str(state) + "_Sites.csv")
                print("DECODING: " + infile)
                with open(infile, 'r') as jsonfile:
                    json_data = json.load(jsonfile)
                with open(outfile, 'a+') as csvOutput:
                    csvwriter = csv.writer(csvOutput)
                    if count == 0:
                        #print("Addidng ONE TIME HEADERS TO FILE")
                        csvwriter.writerow(json_data.keys())
                        count = count + 1
                    csvwriter.writerow(json_data.values())

'''
This function is utilized to find all the .csv files in a directory and combine them into a single csv file.
'''

def aggregateCSV(rootdir):
    outfile = os.path.join(rootdir, "allStates.csv")
    count = 0
    for dirName, subdirList, fileList in os.walk(rootdir):
        print("Currently In: " + dirName)
        for fname in fileList:
            if ".csv" in fname:
                print("Combining " + fname + " To ---->" + outfile)
                with open(outfile, 'a+') as masterCSV:
                    if count == 0:
                        masterCSV.write('Operator,Location,Street,City,State,Zip,Country,Address,InstallDate,Status,SitePhone,OperatorPhone,OperatingHours\n')
                        count = count + 1
                    with open(os.path.join(dirName,fname), 'r') as inFile:
                        for line in inFile:
                            if "Operator,Location,Street," in line:
                                pass
                            else:
                                masterCSV.write(line)

def builHTML(dictionary):
    pass
