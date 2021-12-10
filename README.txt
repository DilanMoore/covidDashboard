--- Welcome to the Covid Dashboard program ---

--------- (1) Getting Started ---------
To run the program, please execute the file "user_interface_handler.py" using Python 3.9 or later. Please also read through the customisation information, making sure to
follow the steps for setting up your personal API key (under [2 - Other] in the "Customisation" section of this readme).

--------- (2) Customisation ---------
The program will, by default, show data for Exeter. This, along with other attributes, can be altered via the config file "myconfig.json". These are outlined below.

[1 - Location]

location: Exeter
location_type: ltla
nation_location: England

"location" can be changed to any location or region in the United Kingdom. Once this is done, you must also change the "location_type" and "nation_location" to reflect this.
 
"location_type" should reflect the category of location input. Possible values for "location_type" are as follows (without quotation marks):

"overview" - Overview data for the United Kingdom
"nation" - Nation data (England, Northern Ireland, Scotland, and Wales)
"region" - Region data
"nhsRegion" - NHS Region data
"utla" - Upper-tier local authority data
"ltla" - Lower-tier local authority data

"nation_location" should reflect which nation of the United Kingdom the "location" is in, as follows:

"England"
"Northern Ireland"
"Scotland"
"Wales"

For example, the "location" of 'Exeter' would require a "location_type" of 'ltla' and a "nation_location" of 'england'.


[2 - Other Customisation]
 
title: Covid Dashboard
image: covidLogo.jpg
apiKey: apiKey=7355f35011ab4c9d8c309da19521ba8c

"title" can be changed to whatever the user wants, and will be the title displayed for the dashboard.

"image" can be changed to alter what icon is displayed on the dashboard. The user must first save a file into static -> images.
The value of "image" should then be changed to the filename of the desired image

"apiKey" should be changed to the user's own API key for the news API. Please follow the instructions at https://newsapi.org to first obtain your unique key.
The user should then change the value of "apikey" to 'apiKey=012345', with 012345 being replaced by the unique api key.


[3 - Other Variables in the Config File]

The variables below should not be changed as doing so may stop the program from working.
 
testVar
newsList
updateList

--------- (3) If Something Goes Wrong ---------

If the dashboard stops working, please delete the program and re-install from the github, as in Further Information. 
Those with python experience are welcome to look at the logFile.txt for any errors.

--------- (4) Further Information ---------

News API: https://newsapi.org
Covid API developers gude: https://coronavirus.data.gov.uk/details/developers-guide
GitHub: 
    