#ChampaignCountyJail

###Tracking inmates in the Champaign County Jail system

Its beating heart is [the jail scraper](https://github.com/lashback/ChampaignCountyJail/blob/master/jail/apps/prisoners/management/commands/champaign_jail_scrape.py), influenced heavily by the neighboring [Cook County Jail scraper](https://github.com/sc3/cookcountyjail), but prior to their the heavy rewrite in early 2014.

Currently set up as a cron job every two hours (courtesy of the [tutorial](http://kevin.schaul.io/2011/11/07/tutorial-web-scraping-with-django/) by [Kevin Schaul](https://github.com/kevinschaul))

---
##Setup and Installation
###Prereqs
####Server with LAPP stack.
The easiest way to set this up is with **L**inux machine with **A**pache, **PostGRES** and **P**ython.

####Postgres
This app requires some sort of SQL database to operate. Given the geographical nature of some of these fields, it's advised to use PostGRES due to its GIS capabilities, but the setup of this system is kind of hard. It should already be installed, but the preferred version is 9.1 for this project (anything above 9.1 should be fine).
When PostGRES is installed, you need to install PostGIS. Directions [here](https://docs.djangoproject.com/en/dev/ref/contrib/gis/install/postgis/)
Once you've installed PostGRES with the proper requirements
`createdb -T template_postgis jail`


###Admin

###Cron job
The system is designed to execute a command every two hours, but you can adjust . Check the cron job docs for more information about setting the frequency. 

####Python Virtual Environment
Python virtual environments allow you to encapsulate all of the python-based tools your app will need in order to operate. 


###Data exports
A pure SQL dump is probably not going to be fun for us. 

###Dashboard
The homepage displays 

##Getting started
####Installation
Clone the git repo here:
`git clone git://github.com/lashback/ChampaignCountyJail`
Create your python virtual env:
`mkvirtualenv jail`
Install the requirements: 
`pip install -r requirements.txt

####Set up the database







