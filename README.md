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

####Python and the Virtual Env
Python virtual environments allow you to encapsulate all of the python-based tools your app will need in order to operate. This installation and setup is probably the hardest. 

###Data exports
A pure SQL dump is probably not going to be fun for us. Let's talk about better ways to display and process data that reporters and developers both can use.

A lot of the things you'll need will be detailed [here](https://github.com/overview/overview-server/wiki/Setting-up-a-development-Environment).

##Getting started
------

####Installation
Clone the git repo here:
`git clone git://github.com/lashback/ChampaignCountyJail`
Create your python virtual env:
`mkvirtualenv jail`
Install the requirements: 
`pip install -r requirements.txt`
Navigate into the next directory:
`cd jail`

####Set up the database
First create the database. 
`createdb -T template_postgis jail`
Then sync and migrate:
`python manage.py syncdb
python manage.py schemamigration prisoners --intial
python manage.py migrate`
You might have to fiddle with the database connection settings to make everything Cool and Froody. 

####Cron job
The system is designed to execute a command every two hours, but you can adjust that. Check the [cron job docs](https://help.ubuntu.com/community/CronHowto) for more information about setting the frequency.
Make sure scrapeit.sh looks like this: (This is under dev to execute within python virtualenv)
'#!/bin/bash
python manage.py champaign_jail_scrape
echo "Worked: $(date)" >> /home/nlash/Documents/jail/app/jail/jail/scrape.log'
Now, open up your Crontab:
`crontab -e`
And have that script run according to the docs above. Here's every two hours:
`0 */2 * * * /home/nlash/Documents/jail/app/jail/jail/scrapeit.sh >> /home/nlash/Documents/jail/app/jail/jail/scrape.log`

You should be good to go! Whoopee!