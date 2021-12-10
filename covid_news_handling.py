#!/usr/bin/env python
# coding: utf-8

import requests, sched, time
import json
import datetime
from datetime import date
import configHandler as cfg

import logging


# news API request
# takes covid_terms
# returns news relevant to covid_terms in query

def news_API_request(covid_terms = "Covid COVID-19 coronavirus") -> requests.models.Response:
    
    logging.info("Attempting News API call")
    
    keyTerms = covid_terms.replace(" ", " OR ")
    
    url = ('https://newsapi.org/v2/everything?'
            'q='+ keyTerms + '&'
            'from=' + str(datetime.datetime.strptime(str(date.today()), "%Y-%m-%d")) + '&'
            'sortBy=popularity&' +
            str(cfg.getConfigData("apiKey")))
    
    
    try:
        covidNews = requests.get(url)
        logging.info("News API request called succesfully")
    except:
        logging.error("Unable to perform News API request")  
        
    return covidNews


# update news
# uses news_API_request to retrieve current news
# then uses this to update existing news (oldNews)
# integrated with update scheduler

oldNews = {}

def update_news() -> dict:
    
    logging.info("Retrieving new News aricles")
    newNews = news_API_request().json()
    oldNews.update(newNews)
    
    return oldNews

    
# schedule nws updates
# takes update interval and update name
# schedules updates using sched module for given time interval
# Uses s2 to keep queue seperate from covid API queue


s2 = sched.scheduler(time.time, time.sleep)

def schedule_news_updates(update_interval, update_name) -> None:
    
    logging.info("Scheduling News API request")
    
    try:
        update_news()
        s2.enter(update_interval, 1, schedule_news_updates, (update_interval, update_name))
        logging.info("newsAPI request performed, with next update called " + update_name + " scheduled for " + str(update_interval) + " seconds")
    except:
        logging.error("Unable to schedule News API request called " + update_name + " for " + str(update_interval) + " seconds")
    
    