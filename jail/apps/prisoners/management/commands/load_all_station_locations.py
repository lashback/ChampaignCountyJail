from django.core.management.base import BaseCommand
import csv
import os
from apps.incidents.models import *
from settings.common import SITE_ROOT
from django.contrib.localflavor.us.us_states import STATE_CHOICES


class Command(BaseCommand):
    help = 'Loads all Border Patrol station addresses from CSV'

    def handle(self, *args, **options):
        try:
            if len(args) > 0:
                self.stdout.write('Using manual CSV location ...\n')
                file_path = args[0]
            else:
                self.stdout.write('Using default CSV location ...\n')
                working_dir = os.path.join(SITE_ROOT, '../data')
                file_path = os.path.join(working_dir, 'bpstation2.csv')

            handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
            handle.next()  # Skip header row

            for h in handle:
                try:
                    match_found = False
                    for station in BPStation.objects.all():
                        if station.name == h[6].strip():
                            match_found = True
                            self.stdout.write('Matched station: %s\n' % (station.name))
                            station.address = h[2].strip()
                            station.city = h[3].strip()
                            station.state = STATE_CHOICES[[i for i, v in enumerate(STATE_CHOICES) if v[1] == h[4].strip()][0]][0]
                            station.zip = h[5].strip()

                            sector_name = h[0].strip()
                            sector_load, sector_loaded = BPSector.objects.get_or_create(
                                name = sector_name)
                            print sector_load
                            station.sector = sector_load
                            
                            

                            station.save()

                    if not match_found:
                        self.stdout.write('Station in CSV not found in DB: %s\n' % h[1].strip())

                except:
                    raise

            station_count = BPStation.objects.all().count()
            address_count = BPStation.objects.exclude(address__isnull=True).exclude(address__exact='').count()
            self.stdout.write('%s of %s stations have address information\n' % (address_count, station_count,))

            self.stdout.write('Successfully loaded Border Patrol station addresses.\n')
        except AttributeError:
            raise
