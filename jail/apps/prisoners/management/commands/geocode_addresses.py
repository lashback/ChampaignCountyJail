from django.core.management.base import BaseCommand, CommandError
import csv, os, sys, re
from time import strptime, strftime
from string import split
from apps.prisoners.models import *
from django.contrib.gis.geos import GEOSGeometry
from settings.common import SITE_ROOT

class Command(BaseCommand):
    help = 'Uses OMGeocoder to geocode addresses and gives you results for the stragglers'
    
    def handle(self, *args, **options):
        
        from omgeo import Geocoder
        g = Geocoder([
            ['omgeo.services.Bing',{
                'settings':{
                    'api_key':'AufKQbvq8uGM3qsQWwMwJNtlf6LLxe5bPvOAVcxi-79Qp0tDl0T2qScdOQiBNKkE'
                }
            }],
        #     ['omgeo.services.Nominatim',{}],
        #     ['omgeo.services.MapQuest',{
        #         'settings':{
        #             'api_key':'Fmjtd%7Cluua2501lu%2C2a%3Do5-962gq6'
        #         }    
        #     }]
        ])

        for s in Address.objects.filter(verified=False):
            #get geocoded address for this address
            address_string = s.string
            geocode_results = g.geocode(address_string,True)
            geocode_candidates = geocode_results['candidates']
            for c in geocode_candidates:
                if c.confidence == 'High':
                    s.point_location = GEOSGeometry('POINT(%s %s)' % (c.x, c.y,),4326)
                    s.save()
                    self.stdout.write("Location found: %s %s\n" % (c.x, c.y,))
            
            if not s.point_location:
                
                self.stdout.write("No good geocode found\n")
            s.attempted = True
            s.save()