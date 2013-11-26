#!/bin/bash
python manage.py champaign_jail_scrape
echo "Worked: $(date)" >> /home/nlash/Documents/jail/app/jail/jail/scrape.log
