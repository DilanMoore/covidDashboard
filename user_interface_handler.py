#!/usr/bin/env python
# coding: utf-8

# Setup current working directory to match location of file
import os
os.chdir((__file__).replace("user_interface_handler.py", ""))

# Import and setup logging
import logging
logging.basicConfig(filename="logFile.log", level=logging.DEBUG)
logging.info("Logging started")

# Standard imports
from flask import Flask, render_template, request
import covid_data_handler as cdh
from covid_data_handler import s1
import covid_news_handling as cnh
from covid_news_handling import s2
import configHandler as cfg
from datetime import datetime


# Global Variables relating to updates and news info
updateList = cfg.getConfigData("updateList")
updateObjectList1 = []

newsList = cfg.getConfigData("newsList")
updateObjectList2 = [] 
newsBlackList = []


app = Flask(__name__)

@app.route('/index')
def index():
    
    logging.info("index called")
    
    # general variables
    
    title = cfg.getConfigData("title")
    image = cfg.getConfigData("image")
    location = cfg.getConfigData("location")
    location_type = cfg.getConfigData("location_type")
    nation_location = cfg.getConfigData("nation_location")
    
    # Covid stuff data
     
    local_7day_infections, hospital_cases, deaths_total = cdh.process_covid_csv_data(cdh.parse_csv_data(cdh.api_to_CSV(cdh.covid_API_request(location, location_type))))
    national_7day_infections = cdh.process_covid_csv_data(cdh.parse_csv_data(cdh.api_to_CSV(cdh.covid_API_request(nation_location, "nation")))) [0]

    
    # News variable
    news_articles = checkNews() # list of elements containing 'title' and 'content' columns
    
    # Updates variable
    updates =  updateManager() # dict of elements containing 'title and 'content' columns
    
    # Assignment of variables to template
    return render_template('index.html', 
                           title = title,
                           image = image,
                           
                           location = location,
                           nation_location = nation_location,
                           
                           local_7day_infections = local_7day_infections,
                           national_7day_infections = national_7day_infections,
                           hospital_cases = hospital_cases,
                           deaths_total = deaths_total,
                           
                           updates = updates,
                           
                           news_articles = news_articles,
                           )
    
# updateManage
# takes no input
# returns list of scheduled updates
# retrieves any scheduled updates and adds them to relevent queue
# also ensures scheduled updates are shown/deleted on UI

def updateManager() -> list:
    
    contentData = ""
    
    repeatFlag = False
    covidFlag = False
    newsFlag = False
    
    
    if str(request.args.get("repeat")) == "repeat":
        repeatFlag = True
        
    if str(request.args.get("covid-data")) == "covid-data":
        covidFlag = True
        
    if str(request.args.get("news")) == "news":
        newsFlag = True
        
        
    if covidFlag == True: 
        contentData += " Covid data will update."
    
    if newsFlag == True: 
        contentData += " News will update."

    if repeatFlag == True:
        contentData += " Update will repeat."
        
        
    updateTime = str(request.args.get("update"))
    
    if (updateTime == ""):
        contentData += " Time not selected. Please re-schedule, choosing an update time before submission."
    else: contentData += " Scheduled for " + updateTime
    
    if (newsFlag == False and covidFlag == False):
        contentData += " No data selected. Please re-schedule, using tickboxes to indicate which data to update."
    
                           
    titleData = str(request.args.get("two"))
     
    updateList.append({"title": titleData , "content": contentData})

    deleteItem = request.args.get("update_item")
    
    for i in updateList:
        if i["title"] == "None":
            updateList.remove(i)
            
    for i in updateList:
        if i["title"] == str(deleteItem):
            updateList.remove(i)
            logging.info("Removed update called " + i["title"] + " from schedule queue.")
    
    if(titleData != "None"):
        # calculate time to first interval and schedule for then
        today = datetime.now()
        today = today.strftime("%H:%M")
        
        d1 = datetime.strptime(today, "%H:%M")
        d2 = datetime.strptime(updateTime, "%H:%M") 
        update_interval = d2 - d1
        update_interval_seconds = update_interval.total_seconds()
        
        if update_interval_seconds < 0:
            update_interval_seconds = (60*60*24) + update_interval_seconds
        
        location = cfg.getConfigData("location")
        location_type = cfg.getConfigData("location_type")
        
        if(repeatFlag == True and covidFlag == True):
            
            # first interval is after desired time, all following are daily (60*60*24)
            e = s1.enter(int(update_interval_seconds), 1, cdh.schedule_covid_updates, (60*60*24, titleData, location, location_type))
            updateObjectList1.append(e)
            logging.info("Repeater 1 scheduled for " + str(update_interval_seconds)) 
        
        if(repeatFlag == False and covidFlag == True):
            e = s1.enter(int(update_interval_seconds), 1, cdh.covid_API_request, (location, location_type))
            updateObjectList1.append(e)
            logging.info("Non-repeater 1 scheduled")
            
        if(repeatFlag == True and newsFlag == True):
            
            # first interval is after desired time, all following are daily (60*60*24)
            e = s2.enter(int(update_interval_seconds), 1, cnh.schedule_news_updates, (60*60*24, titleData))
            updateObjectList2.append(e)
            logging.info("Repeater 2 scheduled for " + str(update_interval_seconds)) 
        
        if(repeatFlag == False and newsFlag == True):
            e = s2.enter(int(update_interval_seconds), 1, cnh.update_news(),())
            updateObjectList2.append(e)
            logging.info("\n\n\nNon-repeater 2 scheduled\n\n\n")
            
    
    updateName = ""
    for i in updateObjectList1:
        
        item = str(i)
        splitData = item.split(",")
        
        j = 0
        while j < len(splitData):
            
            if "argument=(" in str(splitData[j]):
                updateName = splitData[j+1]
                
            j += 1
                
                # NB - leading space for below concatenation is VERY necessary
        if str(updateName) == str(" '" + str(deleteItem) + "'"):
            s1.cancel(i)
            updateObjectList1.remove(i)
            logging.info("Deleted update called ", str(updateName))

    s1.run(blocking = False)
    s2.run(blocking = False)
        
    return updateList

# checkNews
# takes no input
# returns top four news articles
# uses covid news handler to retrieve news articles
# appends these to list as required for UI display, which is then returned

def checkNews() -> list:
    
    logging.info("Refreshing news for UI")
    
    newsList = cnh.update_news()["articles"]
    filteredNewsList = []
    
    deleteItem = request.args.get("notif")
    if deleteItem != None:
        newsBlackList.append(deleteItem)
        logging.info("Added '" + deleteItem + "' to blacklist")
        
    for i in newsList:
        if i["title"] == None:
            newsList.remove(i)
     
    for i in newsList:
        includeFlag = True
        
        for j in newsBlackList:
            if i["title"] == str(j):
                
                includeFlag = False
                logging.info("Omitted " + i["title"] + " from displayed articles")

        
        if(includeFlag == True):
            i["content"] = str(i["description"]) + "            " + str(i["url"]) 
            filteredNewsList.append(i)

    return filteredNewsList[0:4]
    
if __name__ == '__main__':
    app.run()
