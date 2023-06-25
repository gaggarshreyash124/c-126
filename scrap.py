from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import csv

starturl = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"

browser = webdriver.Chrome("C:\Users\frame\Downloads\chromedriver_win32")
browser.get(starturl)
time.sleep(10)

headers = ["name","lightyearsfromearth","planatmass","stellarmagintude","discoverydate"]
planetdata = []

def scrap():
    soup = BeautifulSoup(browser.page_source)
    for ultag in  soup.find_all("ul"): 
        litag=ultag.find_all("li")
        templist = []
        for index,litag in enumerate(litag):
            if index == 0:
                templist.append(litag)
            else:
                try:
                    templist.append(litag.contents[0])
                except:
                    templist.append("")
        
        planetdata.append(templist)

newplanetsdata = []

def scrapmoredata(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content)
        templist = []
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags = tr_tag.findall("td")
            for tdtag in td_tags:
                try:
                    templist.append(tdtag.findall("div",attrs = {"class":"value"})[0].contents[0])
                except:
                    templist.append("")
        newplanetsdata.append(templist)
    except:
        time.sleep(1)
        scrapmoredata(hyperlink)
for index,data in enumerate(planetdata):
    scrapmoredata(data[5])
    print("scraping at hyperlink is completed")

print(newplanetsdata[0:10])
finalplanetdata = []
for index,data in enumerate(planetdata):
    newplanetsdataelement = newplanetsdata[index]
    finalplanetdata.append(data+newplanetsdataelement)


with open("space.csv","w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(planetdata)

scrap()