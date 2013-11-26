from django.core.management.base import BaseCommand, CommandError
import csv, os, sys, re
from time import strptime, strftime
from string import split
from apps.prisoners.models import *
from settings.common import SITE_ROOT

class Command(BaseCommand):

	def handle(self, *args, **options):
		#grab all the inmates, go through them one by one.
		for inmate in Inmate.objects.all():
			
			print inmate.name
			#Get all the bookingcharges associated with them.
			charges = inmate.bookingcharge_set.all()
			
			#and go through them.
			for c in charges:
				#Either create a new Booking superclass or get one that matches the same basic identifiers:
				#We're treating each prison 'visit' as a booking, such that the same 
				#inmate with the same in/out dates will be the same booking
				
				booking_import, booking_created = Booking.objects.get_or_create(
					identity = c.identity,
					booking_date = c.booking_date,
					release_date = c.release_date
					)
				#each bookingcharge has a link to a Booking (null before this runs).
				#Set that link as the booking we got above, and we're good!
				c.booking = booking_import
				c.save()
