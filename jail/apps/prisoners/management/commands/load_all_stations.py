import csv
import os
from django.core.management.base import BaseCommand
from apps.incidents.models import *
from settings.common import SITE_ROOT


class Command(BaseCommand):
    help = 'Loads all Border Patrol station names and codes from CSV'

    def handle(self, *args, **options):
        try:
            if len(args) > 0:
                self.stdout.write('Using manual CSV location ...\n')
                file_path = args[0]
            else:
                self.stdout.write('Using default CSV location ...\n')
                working_dir = os.path.join(SITE_ROOT, '../data')
                file_path = os.path.join(working_dir, 'bp_stations_20120823.csv')

            handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
            handle.next()  # Skip header row

            for h in handle:
                try:
                    #filter for old station codes
                    code = h[1].strip()

                    #Temecula Station, became Murrieta in 2006/2007
                    if h[1].strip() == 'TEM':
                        code = 'MUR'

                    #Weslaco, new abbreviation
                    if h[1].strip() == 'MER':
                        code = 'WSL'

                    #filter for sector codes, set station to None
                    if h[1].strip() in ['SDC', 'YUM', 'ELC', 'MCA', 'DRT', 'LRT', 'TCA', 'N/A']:
                        code = False

                    #unknown stations in El Paso sector, set station to None
                    if h[1].strip() in ['CSB', 'ESO']:
                        code = False

                    if code:

                        station, station_created = BPStation.objects.get_or_create(
                            code=h[1].strip(),
                            name=h[0].strip(),
                            
                        )

                        #station.save()

                except:
                    raise

            self.stdout.write('Successfully loaded Border Patrol stations.\n')
        except AttributeError:
            raise
