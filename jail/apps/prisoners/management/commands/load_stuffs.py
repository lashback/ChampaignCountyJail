import csv
import os
import re
from time import strptime, strftime
from string import split
from django.core.management.base import BaseCommand
from apps.prisoners.models import *
from settings.common import SITE_ROOT

class Command(BaseCommand):
    help = 'Donteven.'

    def handle(self, *args, **options):
        
        if len(args) > 0:
            self.stdout.write('Using manual CSV location ...\n')
            file_path = args[0]
        else:
            self.stdout.write('Using default CSV location ...\n')
            working_dir = os.path.join(SITE_ROOT, '../data')
            file_path = os.path.join(working_dir, 'all.csv')

        handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
        handle.next()  # Skip header row

            #BAAAAhhhhhhhhhh

        for index, h in enumerate(handle):
    
            charge_import, charge_created = Charge.objects.get_or_create(
                description = h[3].strip(),
                statute = h[4].strip()
                )

            race_import, race_created = Race.objects.get_or_create(
                name = h[6].strip()
                )

            inmate_import, inmate_created = Inmate.objects.get_or_create(
                name = h[5].strip()
                )

            bond_amount = h[2].strip()
            print bond_amount

            release_date = h[1].strip()

            if len(bond_amount)>0:
                if len(release_date) > 0:
                    bookingcharge_import, bookingcharge_created = BookingCharge.objects.get_or_create(
                    identity = inmate_import,
                    charge = charge_import,
                    race = race_import,
                    gender = h[8].strip(),
                    bond_amount = bond_amount,
                    booking_date = h[0].strip(),
                    release_date = h[1].strip()
                    )
                else: 
                    bookingcharge_import, bookingcharge_created = BookingCharge.objects.get_or_create(
                    identity = inmate_import,
                    charge = charge_import,
                    race = race_import,
                    gender = h[8].strip(),
                    bond_amount = bond_amount,
                    booking_date = h[0].strip(),
                    )
            else: 
                bookingcharge_import, bookingcharge_created = BookingCharge.objects.get_or_create(
                    identity = inmate_import,
                    charge = charge_import,
                    race = race_import,
                    gender = h[8].strip(),
                    booking_date = h[0].strip(),
                    release_date = h[1].strip()
                    )
            print inmate_import.name
