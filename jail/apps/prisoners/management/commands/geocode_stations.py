from django.core.management.base import BaseCommand, CommandError
import csv, os, sys, re
from time import strptime, strftime
from string import split
from apps.incidents.models import *
from django.contrib.gis.geos import GEOSGeometry
from settings.common import SITE_ROOT
from omgeo import Geocoder

class Command(BaseCommand):
    help = 'Uses OMGeocoder to geocode Border Patrol station locations, with manual overrides for known stragglers'
    
    def handle(self, *args, **options):
        
       # from omgeo import Geocoder
        g = Geocoder([
            ['omgeo.services.Bing',{
                'settings':{
                    'api_key':'AnoU4IZjQyL3BLIVJNmfpUgqh86Z8jVEk4n2uQNRzSWAu1Suu5I1NvmjGslFS1Dk'
                }
            }],
        #     ['omgeo.services.Nominatim',{}],
        #     ['omgeo.services.MapQuest',{
        #         'settings':{
        #             'api_key':'Fmjtd%7Cluua2501lu%2C2a%3Do5-962gq6'
        #         }    
        #     }]
        ])

        for s in BPStation.objects.filter(address__isnull=False):
            #get geocoded address for this address
            address_string = '%s, %s, %s, %s' % (s.address, s.city, s.state, s.zip,)
            geocode_results = g.geocode(address_string,True)
            geocode_candidates = geocode_results['candidates']
            for c in geocode_candidates:
                if c.confidence == 'High':
                    s.point_location = GEOSGeometry('POINT(%s %s)' % (c.x, c.y,),4326)
                    s.save()
                    self.stdout.write("Location found: %s %s\n" % (c.x, c.y,))
            
            if not s.point_location:
                self.stdout.write("No good geocode found\n")
        
        #manual override of locations that don't geocode well
        try:
            if len(args) > 0:
                self.stdout.write('Using manual CSV location ...\n')
                file_path = args[0]
            else:
                self.stdout.write('Using default CSV location ...\n')
                working_dir = os.path.join(SITE_ROOT, '../data')
                file_path = os.path.join(working_dir, 'geocodestragglers20120830.csv')
                    
            handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
            header = handle.next()
            
            for h in handle:
                print h
                try:
                    station = BPStation.objects.get(name=h[1].strip())
                    
                    station.point_location = GEOSGeometry('POINT(%s %s)' % (h[7].strip(), h[8].strip(),),4326)
                    station.save()
                    self.stdout.write('%s: %s %s\n' % (h[0].strip(), h[7].strip(), h[8].strip(),))
                    
                except:
                    raise
            
            self.stdout.write('Successfully loaded manual Border Patrol geocodes.\n')
        except AttributeError:
            raise
