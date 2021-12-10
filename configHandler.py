# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 11:13:05 2021

@author: dilan
"""

import json
import logging

# Get config data
# Takes varName, which is a key in the myconfig.yaml dictionary
# Returns the value stored for this key
 
def getConfigData(varName):
    with open("myconfig.json") as f:
         logging.info("Retrieving variable " + varName + " from config file")
         configData = json.load(f)
         return configData[varName]
    
             