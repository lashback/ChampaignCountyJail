import csv
import os
import re
from time import strptime, strftime
from string import split
from django.core.management.base import BaseCommand
from apps.incidents.models import *
from settings.common import SITE_ROOT

#THIS CAN ONLY BE RUN AFTER LOAD STAFFING
class Command(BaseCommand):
	def handle(self, *args, **options):
		working_dir = os.path.join(SITE_ROOT, '../data')
		file_path = os.path.join(working_dir, 'bpStatsPDFs/total_apprehensions.csv')
		handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
		
		#for each row, in csv...
		for h in handle:
			#look at every sectorStat object
			for sectorstat in SectorStat.objects.all():
				#when a sectorstat object matches the row we're on...
				if sectorstat.sector.name == h[0].strip():
					#set the year at 2000, the (second column of data)
					year = 2000
					#iterate through each column after the sector-name one.
					for column in h[1:]:

						print sectorstat.sector.name
						print year
						print column
						print sectorstat.year

						#if we'reon the right one.... 
						if str(sectorstat.year) == str(year):
							sectorstat.apprehensions = column.strip()
							sectorstat.save()
							print "You got it for "
							print year
						#in any case, increment year.
						year += 1
						#WHY DON'T YOU WORK???
