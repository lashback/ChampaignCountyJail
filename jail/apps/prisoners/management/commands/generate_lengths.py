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
        chips_block = Block.objects.get(name = 'CHIP')
        print "Name, Race, Bond, Length in Jail, Released"
        for r in Race.objects.all():
            bookings = Booking.objects.filter(identity__race = r, total_bond__gte = 1, rough_release_date__isnull = False).exclude(blockmodel = chips_block)
            for b in bookings:
                release = False
                if b.rough_release_date is not None:
                    release = True
                print "%s, %s, %s, %s, %s" %(b.identity.name, r.name, b.total_bond, b.booking_length, release)

