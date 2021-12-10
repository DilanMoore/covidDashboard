#!/usr/bin/env python
# coding: utf-8

import datetime, sched, time
from datetime import date
from uk_covid19 import Cov19API
import pandas as pd
from requests import get
import csv
import logging

# parse csv data
# takes csv_filename and returns a list of strings for rows of the file

def parse_csv_data (csv_filename) -> list:
    with open(csv_filename) as file:
        logging.info("Opened CSV file " + str(csv_filename))
        rowList = file.read().splitlines()
        file.close()
        logging.info("Closed CSV file " + str(csv_filename))
    return rowList


# WeekFlag
# takes two dates, todaysDate and targetDate
# returns true if a targetDate is within a week of todaysDate
# allows to return case total for seven preceding days
# datediff comparisons offset by +1 to ignore todays date
# hence returns value for seven day period ending yesterday

def weekFlag(todaysDate, targetDate) -> bool:
    
    try:
        d1 = datetime.datetime.strptime(todaysDate, "%d/%m/%Y")
    except:
        try:
            d1 = datetime.datetime.strptime(todaysDate, "%Y/%m/%d")
        except:
            d1 = datetime.datetime.strptime(todaysDate, "%Y-%m-%d")
    #try/except necessary as date format varies between national and local covid API calls
    try:
        d2 = datetime.datetime.strptime(targetDate, "%d/%m/%Y") 
    except:
        try:
            d2 = datetime.datetime.strptime(todaysDate, "%Y/%m/%d")
        except:
            d2 = datetime.datetime.strptime(targetDate, "%Y-%m-%d") 
        
    dateDiff = (d1 - d2).days
    
    if(dateDiff >= 9): return False
    if(dateDiff < 2): return False
    if(dateDiff < 9): return True
    

# process csv data
# takes covid_csv_data as list
# returns three variables from the list:
# 1- number of cases in the last 7 days
# 2- current number of hospital cases
# 3- cumulative number of deaths 

def process_covid_csv_data(covid_csv_data) -> [int, int, int]:   
    
    logging.info("Procesing covid CSV data")
    today = date.today().strftime("%d/%m/%Y")
    
    current_hospital_cases = 0
    last7days_cases = 0
    total_deaths = 0
     
    rowCount = 0
    for rows in covid_csv_data[1:]:
        splitData = rows.split(",")
        
        if(rowCount == 0):
            today = splitData[3]
            # try/except needed as local API returns null values for current hospital cases
            try:
                current_hospital_cases = int(float(splitData[5]))
            except:
                current_hospital_cases = 0
            logging.info("Retrieved hospital cases from CSV (" + str(current_hospital_cases) + ")")
        
        if(weekFlag(today, splitData[3]) == True):
            last7days_cases += int(float(splitData[6]))
            logging.info("Retrieved seven day cases from CSV (" + str(last7days_cases) + ")")
            
        if(splitData[4] != ""):
            if(int(splitData[4]) > total_deaths):
                total_deaths = int(splitData[4])
                logging.info("Updated cumulative death count from CSV (" + str(total_deaths) + ")")
        
        rowCount += 1

    return last7days_cases, current_hospital_cases, total_deaths


# covid API request
# takes location and location type
# returns relevant, up to date covid data as a dictionary

# Need to overhaul and use legit API method

def covid_API_request(location = "Exeter", location_type = "ltla") -> dict:
    
    locationFilter = ["areaType=" + location_type , "areaName=" + location]

    cases_and_deaths = {
        "areaCode": "areaCode",
        "areaName": "areaName",
        "areaType": "areaType",
        "date": "date",
        "cumDailyNoDeathsByDeathDate": "cumDeathsByDeathDate",
        "hospitalCases": "hospitalCases",
        "newCasesBySpecimenDate": "newCasesBySpecimenDate",
    }
    
    logging.info("Location set to " + location + " with location type " + location_type)
    
    logging.info("Attempting COVID API call")
    try:
        api = Cov19API(filters = locationFilter, structure = cases_and_deaths)
        data = api.get_json()
        logging.info("COVID API called succesfully")
    except:
        logging.error("Unable to perform covid API request")
    
    return data

# api to CSV
# takes input as a dictionary, as per COVID API request
# saves this as a CSV file and returns name of file for future processing

def api_to_CSV(input, fileName = "covidAPIdata.csv"):
    
    logging.info("Converting covid API data from json to CSV")
    
    df = pd.DataFrame.from_dict(input["data"])
    df.to_csv(fileName, index = False)
    return fileName

# schedule covid updates
# takes update interval and update name
# schedules updates using sched module for given time interval
# uses s1 to allow for use of s2 for news scheduler

s1 = sched.scheduler(time.time, time.sleep)

def schedule_covid_updates(update_interval, update_name, location = "Exeter", location_type = "ltla") -> None:
    
    logging.info("Scheduling COVID API request")
    
    try:
        covid_API_request(location, location_type)
        s1.enter(update_interval, 1, schedule_covid_updates, (update_interval, update_name, location, location_type))
        logging.info("COVID API request performed, with next update called " + update_name + " scheduled for " + str(update_interval) + " seconds")
    except:
        logging.error("Unable to schedule COVID API request called " + update_name + " for " + str(update_interval) + " seconds")
    

