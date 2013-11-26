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
            file_path = os.path.join(working_dir, '2012.csv')

        handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
        handle.next()  # Skip header row

            #BAAAAhhhhhhhhhh

        for index, h in enumerate(handle):
            try:
                charge_tuple = split(h[11].strip(), ';')
                for c in charge_tuple:
                    charge_import, charge_created = Charge.objects.get_or_create(
                        description = c
                        )
                    race_import, race_created = Race.objects.get_or_create(
                        name = h[5].strip()
                        )

                    inmate_import, inmate_created = Inmate.objects.get_or_create(
                        name = h[2].strip(),
                        jacket_number = h[1].strip(),
                        race = race_import
                        )
                    city_import, city_created = City.objects.get_or_create(
                        name = h[7].strip(),
                        state = h[8].strip()
                        )
                    bond_amount = h[13].strip()
                    print bond_amount
                    release_date = h[14].strip()
                    zip_code = h[9].strip()
                    age = h[6].strip()


                    if len(bond_amount)>0:
                        if len(release_date) > 0:
                            if len(zip_code)>0 and len(age) > 0:
                                bookingcharge_import, bookingcharge_created = BookingCharge.objects.get_or_create(
                                    identity = inmate_import,
                                    charge = charge_import,
                                    race = race_import,
                                    city = city_import,
                                    gender = h[4].strip(),
                                    bond_amount = bond_amount,
                                    booking_number = h[0].strip(),
                                    photo_filename = h[10].strip(),
                                    bond_type = h[12].strip(),
                                    booking_date = h[3].strip(),
                                    release_date = h[14].strip(),
                                    age = age,
                                    zip_code = zip_code
                                    )
                            else: 
                                bookingcharge_import, bookingcharge_created = BookingCharge.objects.get_or_create(
                                    identity = inmate_import,
                                    charge = charge_import,
                                    race = race_import,
                                    city = city_import,
                                    gender = h[4].strip(),
                                    bond_amount = bond_amount,
                                    booking_number = h[0].strip(),
                                    photo_filename = h[10].strip(),
                                    bond_type = h[12].strip(),
                                    booking_date = h[3].strip(),
                                    release_date = h[14].strip(),
                                    
                                    )
                        else: 
                            bookingcharge_import, bookingcharge_created = BookingCharge.objects.get_or_create(
                                identity = inmate_import,
                                charge = charge_import,
                                race = race_import,
                                city = city_import,
                                gender = h[4].strip(),
                                bond_amount = bond_amount,
                                booking_number = h[0].strip(),
                                photo_filename = h[10].strip(),
                                bond_type = h[12].strip(),
                                booking_date = h[3].strip(),
                                #release_date = h[14].strip()
                                )
                    else: 
                        bookingcharge_import, bookingcharge_created = BookingCharge.objects.get_or_create(
                            identity = inmate_import,
                            charge = charge_import,
                            race = race_import,
                            city = city_import,
                            gender = h[4].strip(),
                    #        bond_amount = bond_amount,
                            booking_number = h[0].strip(),
                            photo_filename = h[10].strip(),
                            bond_type = h[12].strip(),
                            booking_date = h[3].strip(),
                            release_date = h[14].strip()
                            )
                    print inmate_import.name
            except Exception:
                raise