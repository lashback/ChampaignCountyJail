from django.core.management.base import BaseCommand, CommandError
import csv, os, sys, re
from time import strptime, strftime
from string import split
from apps.prisoners.models import *
from django.contrib.gis.geos import GEOSGeometry
from settings.common import SITE_ROOT
import datetime
from django.db.models import Q


class Command(BaseCommand):
    help = 'does things'
    
    def handle(self, *args, **options):
        starting_date = datetime.date(2013, 11, 18)
        sample_size = 20
        dates = []
        for x in range (0, sample_size):
            dates.append(starting_date + datetime.timedelta(days = x))
        print dates
        chips_block = Block.objects.get(name = 'CHIP')
        for date in dates:
            for r in Race.objects.all():

                count = Booking.objects.filter(booking_date__lte = date, rough_release_date__gte = date, identity__race = r).exclude(blockmodel = chips_block).count()
                count += Booking.objects.filter(booking_date__lte = date, rough_release_date__isnull = True, identity__race = r).exclude(blockmodel = chips_block).count()
                print "%s, %s, %s" %(r.name, count, date)


