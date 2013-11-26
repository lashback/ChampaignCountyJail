import csv
import os
import re
from time import strptime, strftime
from string import split
from django.core.management.base import BaseCommand
from apps.incidents.models import *
from settings.common import SITE_ROOT

#run dis guy first.
#as of right now, it works! hooray!

class Command(BaseCommand):
	def handle(self, *args, **options):
		working_dir = os.path.join(SITE_ROOT, '../data')
		file_path = os.path.join(working_dir, 'bpStatsPDFs/sectorStaffing.csv')
		handle = csv.reader(open(file_path, 'rU'), delimiter=',', quotechar='"')
		handle.next()

		for h in handle:
			
			for sector in BPSector.objects.all():
				if sector.name == h[0].strip():
					self.stdout.write("Matched sector: %s\n" % (sector.name))
					year = 1993
					for column in h[1:]:
						if year < 2013:
							print year
							stats_import, stats_made = SectorStat.objects.get_or_create(
								sector = sector,
								staffing = column.strip(),
								year = year)
							self.stdout.write("Made records for %s\n" % (year))
							year += 1
						
