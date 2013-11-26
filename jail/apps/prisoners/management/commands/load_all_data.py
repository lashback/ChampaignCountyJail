from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Run a series of commands to load all data. Takes around an hour.'

    def handle(self, *args, **options):
        try:
            self.stdout.write('ARISE, MIGHTY PHOENIX!.\n')
            self.stdout.write('ARISE, MIGHTY PHOENIX!.\n')
            self.stdout.write('ARISE, MIGHTY PHOENIX!.\n')
            self.stdout.write('ARISE, MIGHTY PHOENIX!.\n')
            self.stdout.write('ARISE, MIGHTY PHOENIX!.\n')

           

            # Border Patrol
            call_command('load_all_sectors', interactive=False)
            call_command('load_all_stations', interactive=False)
            call_command('load_all_station_locations', interactive=False)
            call_command('load_stuffs', interactive=False)
            call_command('geocode_stations', interactive=False)
            call_command('load_sector_maps', interactive=False)
            
            self.stdout.write('\nIT IS DONE. IT IS FINISHED.\n')

        except AttributeError:
            raise
