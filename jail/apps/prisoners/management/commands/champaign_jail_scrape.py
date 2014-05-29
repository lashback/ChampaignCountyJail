from datetime import datetime, date
from pyquery import PyQuery as pq
import string
from django.core.management.base import BaseCommand
from optparse import make_option
import httplib, urllib
import urllib2, cookielib
import requests
from time import sleep
from random import random
from BeautifulSoup import BeautifulSoup, NavigableString, Tag
import re
import csv
from apps.prisoners.models import *
from django.core.exceptions import ValidationError
from django.core.exceptions import MultipleObjectsReturned



#BASE_URL = "http://www.co.champaign.il.us/"
BASE_URL = "http://sheriff.co.champaign.il.us/sdwebapp/inmpubsel.pgm?Lname="
BASE_DOMAIN = "http://sheriff.co.champaign.il.us"
NUMBER_OF_ATTEMPTS = 5
STD_INITIAL_SLEEP_PERIOD = 0.1
STD_NUMBER_ATTEMPTS = 3
STD_SLEEP_PERIODS = [1.61, 7, 13, 23, 41]

# Global counters
class Command(BaseCommand):    

    def extract_inmate_urls(self, inmate_search_page):
            # I don't like pyquery because it's unfamiliar not because it's not great
            #print inmate_search_page.text
            soup = BeautifulSoup(inmate_search_page.text)
            print 'im in'
            
            try:
                rows = soup('tr')

                for row in rows:
                    link = row.a['href']
                    print link
                    if not 'javascript' in link:
                        print "now what"                
                        data = row('td')
                        print "i made data"
                        print data
                        first_name = data[0].string.strip()
                        print first_name
                        middle_name = ''
                        if len(data[2].string.strip()) > 0:
                            middle_name = data[2].string.strip()
                        last_name = data[4].string.strip()
                        print last_name
                        age = data[6].string.strip()
                        race = data[8].string.strip()
                        sex = data[10].string.strip()
                        print first_name
                        print last_name
                        print race
                        print sex
                        print link
                        self.create_booking(first_name, middle_name, last_name, age, race, sex, link)
            
            except TypeError:
                print "End of Zs"



            # Get links from last column of each row

    def create_booking(self, first_name, middle_name, last_name, age, race, sex, link):
        #there's a glitch inmate who's been in their system since 2003, and it's fuckign everything up.
        if str(first_name + ' ' + middle_name + ' ' + last_name) == 'TODD EVERETT WALKER':
            pass
        else:
            race_object, race_created = Race.objects.get_or_create(
                name = race
                )


            
            full_link = str(BASE_DOMAIN+link)
            result = requests.get(full_link)
            print 'we got results'
            result_readout = str(result.text)
            
            header_pattern = re.compile('&nbsp;')
            strip_spaces = re.sub(header_pattern,'', result_readout)
       #     print strip_spaces

            address_pattern = re.compile('Address: (.*)')
            addresses = address_pattern.findall(strip_spaces)
            address = addresses[0]
          #  print address

            address_import, address_made = Address.objects.get_or_create(
                string = address.strip(),
                last_known = True
                )
            
            inmate_id, inmate_created = Inmate.objects.get_or_create(
                name = str(first_name + ' ' + middle_name + ' ' + last_name),
                first_name = first_name,
                middle_name = middle_name,
                last_name = last_name,
                race= race_object,
                gender = sex,
                address = address_import
                )

            booking_date_pattern = re.compile('(Booking Date:)(\W+)(\d{1,2})/(\d{1,2})/(\d{4})(\W+)(.*)')
            
            booking_data_over = booking_date_pattern.findall(strip_spaces)
       #     print booking_data_over

            #need regex here that will normalize dates. booking_date_cleaned not great
            booking_data = booking_data_over[0]
        
            month = booking_data[2].strip()
            if len(month) < 2:
                month = '0' + month
       #     print month
            day = booking_data[3].strip()
            if len(day) < 2:
                day = '0' + day
            year = booking_data[4].strip()
            
            booking_date = "%s-%s-%s" % (year, month, day)
    #        booking_date_cleaned = str(booking_date[6:10]+'-'+booking_date[0:2]+'-'+booking_date[3:5])
            booking_time = booking_data[6].strip()

            #print booking_date
            #print booking_time
            facility_pattern = re.compile('(Housing Location:)(.*|\n+)(\n<br>)((.|\n)*?)(\w+)(\s+)(\S+)')
            facility_data_over = facility_pattern.findall(strip_spaces)
           # print facility_data_over
          #  print 'Facility data'
            facility_data = facility_data_over[0]
          #  print facility_data
            facility = facility_data[5].strip()
          #  print facility
            block = facility_data[7].strip()
            print 'is line 143?'
            now = datetime.datetime.now()
            print 'no'
         #   print now
            
                    
            housing_facility_import, housing_facility_created = HousingFacility.objects.get_or_create(
                name = facility
                )

            blockmodel_import, blockmodel_created = Block.objects.get_or_create(
                name = block,
                housing_facility = housing_facility_import
                )
            try: 
                booking, booking_created = Booking.objects.get_or_create(
                
                identity = inmate_id,
                booking_date = booking_date,
                booking_time = booking_time,
                housing_facility = facility,
                
                )
            except ValidationError:
                booking, booking_created = Booking.objects.get_or_create(
                identity = inmate_id,
                booking_date = booking_date,
                housing_facility = facility,
                age = age
                
                )
            
            if booking:
                ###THIS IS SO WRONG I'M EMBARASSED THAT I WROTE IT.
                ### we need a separate command that iterates through the people not yet released, and then release them 
                ###which allllso means that we need to have an . Accidentally releasing or incarcerating someone is going to end very badly for you.                
    #            if not booking_created:
     #               booking.release_date = datetime.today()
      #              booking.save()

                booking.last_seen = now
                
                if not booking.time_created:
                    booking.time_created = now
                    booking.save()

            bond_pattern = re.compile('Bond: \$(.*)')
            bond_over = bond_pattern.findall(strip_spaces)
            bond_data = bond_over[0]
            #print bond_data
            bond = bond_data.strip().replace(",", "")
           # print bond
            booking.total_bond = bond
            booking.gender= sex
            booking.block = block
            booking.age = age
            booking.blockmodel = blockmodel_import
            booking.save()
          #  print booking.total_bond
            soup = BeautifulSoup(strip_spaces)
            
            for row in soup.findAll('tr'):
                print row
                details = row.findAll('td')
                print details
                if details:
                    charge_string = details[0].string
                    charge_string = charge_string.strip()
                    print len(details)
                    action = details[1].string.strip()
                    date = details[2].string.strip()
                    date_pieces = date.split('/')
                    print date_pieces
                    date_fixed = date_pieces[2]+"-"+date_pieces[0]+"-"+date_pieces[1]
                    time = details[3].string.strip()
                    release = details[4].string.strip()
                    datetime_string = date_fixed+" "+time
                    
                    if len(charge_string) > 0:
                        try:
                            charge, charge_created = Charge.objects.get_or_create(
                                description = charge_string
                                )
                        except MultipleObjectsReturned:
                            charge = Charge.objects.filter(description = charge_string.strip())[0]
                        booking_charge, booking_charge_created = BookingCharge.objects.get_or_create(
                            identity = inmate_id,
                            booking = booking,
                            charge = charge,
                            race = race_object
                            )
                    if len(action) > 0:
                        action_import, action_created = Action.objects.get_or_create(
							description = action
                        )
						#try:
                        system_point_import = SystemPoint.objects.create(
							action = action_import,
							court_datetime = datetime_string
                        )
						#except:
						#	print "Something bad occurred"
                        booking_charge.system_point.add(system_point_import)
                        booking_charge.save()
                    if len(release)>0:
                        booking_charge.release_date = release







    #        for br in soup.findAll('br'):
    #        next = br.nextSibling
    #        if not (next and isinstance(next,NavigableString)):
    #            continue
    #        next2 = next.nextSibling
    #        if next2 and isinstance(next2,Tag) and next2.name == 'br':
    #                text = str(next).strip()
    #        if text:
    #                print "Found:", next




        

    def handle(self, *args, **options):
        records = 0
        seen = []
        search_list = string.uppercase
        print search_list
        # Search
        start_date = date.today()
        print start_date



        for search_term in search_list:
            print ("Search: '%s'" % search_term)
            SEARCH_URL = str(BASE_URL + search_term)
            print SEARCH_URL
            results = requests.get(SEARCH_URL)
            if results is None:
                print ("Search failed: '%s'." % search_term)
                continue
            
            self.extract_inmate_urls(results)
            print 'i didnt do it'

            #this works.
            #inmate_urls = self.extract_inmate_urls(results)
            
            # Uniquify urls, reduce the number of queries by about 40%
           # seen_urls = set([])
           # filtered_urls = []
           # for url in inmate_urls:
           #     print url
           #     if self.okay_to_fetch_url(url, seen_urls, start_date):
           #         filtered_urls.append(url)
          #          seen_urls.add(url)

            # Process URLs
            #this is where the magic happens
          
           
      #      for url in inmate_urls:

   #             result = requests.get(url)
    #            print 'we got results'
     #           result_readout = str(result.text)
      #          clean1 = result_readout.replace('&nbsp;', '')
                #print clean1
                #print processed_soup
       #         soup = BeautifulSoup(clean1)
        #        print soup
 #               '''
  #              for br in soup.findAll('br'):
   #                 next = br.nextSibling
    #            if not (next and isinstance(next,NavigableString)):
     #               continue
      #          next2 = next.nextSibling
       #         if next2 and isinstance(next2,Tag) and next2.name == 'br':
        #            text = str(next).strip()
         #       if text:
          #          print "Found:", next
           #         '''





            sleep(10)
#        self.calculate_discharge_date()
        #for b in Booking.objects.filter(release_date__isNull = True).exclude(id__in=seen):
         #   if b.last_seen

#        for b in Booking.objects.filter(release_date__isNull = True):
 #           for c in seen:
#                if b != c:

                

                #new_seen = store_inmates_details(BASE_URL, filtered_urls, options['limit'], records)
                
                #seen += new_seen
                #records = len(seen)

            # Break if limit reached
            #if options['limit'] and records >= options['limit']:
                #break

        # Calculate discharge date range
        #if options['discharge']:
         #   if options['limit'] or options['search']:
          #      raise BaseException("Discharge date option is incompatible with limit and search options")
           # discharged = self.calculate_discharge_date(seen)



    def calculate_discharge_date(self):
            """
            Given a list of jail ids, find inmates with no discharge date that
            aren't in the list. Inmate who haven't been discharged
            """
            today = datetime.today()

            not_present_or_discharged = Booking.objects.filter(release_date=None, last_seen__lt=today)
            for inmate in not_present_or_discharged:
                print inmate.identity.name
                inmate.release_date = today                
                inmate.save()
            return not_present_or_discharged

    def okay_to_fetch_url(self, href, seen_urls, start_date):
            if href not in seen_urls:
                return True
            return False
    #first pass



        