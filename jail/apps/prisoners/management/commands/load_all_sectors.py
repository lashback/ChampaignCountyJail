from django.core.management.base import BaseCommand, CommandError
import csv, os, sys, re
from time import strptime, strftime
from string import split
from apps.incidents.models import *
from settings.common import SITE_ROOT

class Command(BaseCommand):
    help = 'Loads all Border Patrol sector names and codes from CSV'
    
    def handle(self, *args, **options):
        try:
            if len(args) > 0:
                self.stdout.write('Using manual CSV location ...\n')
                file_path = args[0]
            else:
                self.stdout.write('Using default CSV location ...\n')
                working_dir = os.path.join(SITE_ROOT, '../data')
                file_path = os.path.join(working_dir, 'bp_sectors_20120824.csv')
                    
            handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
            header = handle.next()
            
            for h in handle:
                try:
                    code = h[1].strip()
                    
                    #Rio Grande Valley Sector, formerly McAllen Sector
                    if h[1].strip() == 'MCA':
                        code = 'RGV'
                        
                    #Big Bend, renamed from Marfa Oct. 1, 2011
                    if h[1].strip() == 'MAR':
                        code = 'BBT'
                    
                    sector, sector_created = BPSector.objects.get_or_create(
                        code = code
                    )
                    sector.name = h[0].strip()
                    sector.save()
                                        
                except:
                    raise
            
            self.stdout.write('Successfully loaded Border Patrol sectors.\n')
        except AttributeError:
            raise
