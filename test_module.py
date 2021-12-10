# -*- coding: utf-8 -*-
"""
Created on Wed Dec  8 15:17:21 2021

@author: dilan
"""

# Setup current working directory to match location of file
import os
os.chdir((__file__).replace("test_module.py", ""))

# import necessary modules for testing
import pytest
from configHandler import *
#from user_interface_handler import *
from covid_news_handling import *
from covid_data_handler import *

# import random for truly random testing
import random
import time



""" 

Testing for covid_data_handler module
All tests named in format test_NAME(), where NAME is the name of the function being tested

"""


# Test parse_csv_data
# Hard-coded to check returned length of the test CSV against known value

def test_parse_csv_data():
    data = parse_csv_data('nation_2021-10-28.csv')
    assert len(data) == 639    


# Tets weekFlag
# Generates a random date no more than 20 years after 1/1/2020
# Iterates through the 10 dates before/after this start date
# Checks if days in correct seven day period are flagged by weekFlag

import datetime
def test_weekFlag():
    
    start_date = datetime.date(2020, 1, 1)
    startOffset = random.randint(0, 365*20)
    start_date += datetime.timedelta(days = startOffset)
    
    i = -10
    while i < 10:
        
        output = weekFlag(datetime.datetime.strftime(start_date + datetime.timedelta(days = i), "%d/%m/%Y"), datetime.datetime.strftime(start_date, "%d/%m/%Y"))
        
        if i < 2: assert output == False
        elif i < 9: assert output == True
        else: assert output == False

        i+=1
    

# Test process_covid_csv_data
# Calls function to returne values for last7days_cases, current_hospital_cases and total_deaths 
# Hard coded to compare these against known values

def test_process_covid_csv_data():
    last7days_cases, current_hospital_cases, total_deaths = process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544
    
    
# Test covid_API_request
# Calls function to generate an API request using default values ("Exeter", "ltla")
# Checks that the retrieved areaName and areaType match the input areaName and areaType
    
def test_covid_API_request():
    apiCall = covid_API_request()
    data = apiCall["data"]
    assert data[0]["areaName"] == "Exeter" 
    assert data[0]["areaType"] == "ltla" 
   
    
# Test api_to_CSV
# Calls function taking known dictionary input 
# Test then attempts to read from created CSV file
# If data can be read, compares to known input values

def test_api_to_CSV():
    inputDict = {"data" : [{"h0":"r0", "h1":"r0", "h2":"r0"},
                           {"h0":"r1", "h1":"r1", "h2":"r1"},
                           {"h0":"r2", "h1":"r2", "h2":"r2"}]}
    api_to_CSV(inputDict, "tempFile.csv")
    
    try:
        with open("tempFile.csv") as file:
            rowList = file.read().splitlines()
            file.close()
        
        assert rowList[0][0:2] == "h0"
        assert rowList[0][3:5] == "h1"
        assert rowList[0][6:8] == "h2"
        
        i = 1
        while i < 4:
            j = 0
            while j < 7:
                assert rowList[i][j:j+2] == "r" + str(i-1)
                j += 3
            i +=1
                
    except:
        assert False
        

# Test schedule_covid_updates
# Generates a randomInterval no more than 7 days worth of seconds
# Calls the function to schedule and update for this interval
# Adds the known interval to the current time and compares this to the scheduled update time 
# Has a tolerance of +/- 2 seconds as scheduling for the "correct" time

def test_schedule_covid_updates():
    currentTime = time.time()
    randomInterval = random.randint(0, 60*60*24*7)
    schedule_covid_updates(randomInterval, "testName")
    s1.run(blocking = False) 
    timeDiff = int(s1.queue[0][0]) - (int(currentTime) + randomInterval)
    assert (-2 < timeDiff < 2)
    

    


""" 

Testing for covid_news_handling module

"""

# Tests news_API_requests
# The function called returns a response class
# Test is hard coded to check the response class is a valid one (code [200])

def test_news_API_request():
    newsOutput = news_API_request()
    assert str(newsOutput) == "<Response [200]>"
    
    
# Tests update_news
# This function repeatedly updates a dictionary from the news_API_request output
# Test is hard coded to check the status of the latest update request (status "ok")
    
def test_update_news():
    updatedNews = update_news()
    print(updatedNews.keys())
    assert updatedNews["status"] == "ok"
    
    
# Test schedule_news_updates
# Uses same method as tests_schdule_covid_updates (copied below):
# Generates a randomInterval no more than 7 days worth of seconds
# Calls the function to schedule and update for this interval
# Adds the known interval to the current time and compares this to the scheduled update time 
# Has a tolerance of +/- 2 seconds as scheduling for the "correct" time

def test_schedule_news_updates():
    currentTime = time.time()
    randomInterval = random.randint(0, 60*60*24*7)
    schedule_news_updates(randomInterval, "testName")
    s2.run(blocking = False) 
    timeDiff = int(s2.queue[0][0]) - (int(currentTime) + randomInterval)
    assert (-2 < timeDiff < 2)
        

    


""" 

Testing for configHandler module

"""

# Tests getConfigData
# Calls the function to get a test variable
# Hard coded to compare the returned value to a known value

def test_getConfigData():
    testVar = getConfigData("testVar")
    assert testVar == "thisIsATest"


