import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver import ActionChains
from time import sleep
import re
#from selenium.webdriver import ActionChains

'''
This function utilizes selenium to be able to bypass the webpages lazy loading and allow us to capture ALL of the URLs.
This function is run primarily to get all of the individual BTC ATM Details Page URLs. Once we have all the individual URLS
we will be able to curl them down and parse out the pertinent data that we are after.
'''
def seleniumCollect(urlList, outputdir):
    baseURL = 'https://coinatmradar.com'
    with open(urlList) as urls:
        for line in urls:
            outputFileName = getName(line)
            urlToCrawl = baseURL + line.rstrip()
            output = os.path.join(outputdir, outputFileName + ".html")
            print(urlToCrawl)
            browser = webdriver.Firefox()
            browser.get(urlToCrawl)
            while (1):
                browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                try:
                    sleep(2)  # time in seconds
                    btn = browser.find_element_by_xpath("//*[text()='Load more']")
                    #print('btn[load more]:', btn, '\n')
                    ActionChains(browser).move_to_element(btn).click(btn).perform()
                    print('btn is clicked')
                except Exception as e:
                    # print(e)
                    if "Unable to locate element: //*[text()='Load more']" in str(e):
                        print("You reached The End")
                        output = os.path.join(outputdir, outputFileName + ".html")
                        print("The output path is for this html file is: " + output)
                        with open(output, 'a+') as outputFile:
                            outputFile.write(browser.page_source)
                        #print(browser.page_source)
                        browser.close()
                        break

'''
This collect function is used to curl down all of the web pages from the individual BTC ATM in the US.
'''
def collect(urlList, outputdir):
    baseURL = 'https://coinatmradar.com'
    with open(urlList) as urls:
        for line in urls:
            if "promo/go/?u" in line:
                pass
            else:
                print(line)
                outputFileName = getName(line)
                urlToCrawl = baseURL+line.rstrip()
                output = os.path.join(outputdir, outputFileName+".html")
                print("output location is: " + output)
                subprocess.call("curl " + urlToCrawl+ " > " + '"'+output+'"', shell=True)
                print ("CMD ---> "+ "curl " + urlToCrawl+ " > " + '"'+output+'"')
                print (urlToCrawl)

'''
This is a small utility function that is used to get the filename without the extension so that we can append the file name however we want.
Ex. if you give it' example.html' the function will return 'example'.
'''
def getName(line):
    if "city" in line:
        outputfileName = line.split('/')[3]
        return outputfileName
    elif "bitcoin_atm" in line or "bitcoin_teller" in line:
        outputfileName = line.split('/')[3]
        return outputfileName



def printCSV():
    pass

