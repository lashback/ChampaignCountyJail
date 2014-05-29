#from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from omgeo import Geocoder
from numpy import median, mean
from django.core.exceptions import ObjectDoesNotExist
import datetime

# Create your models here.
class Charge(models.Model):
	description = models.CharField(max_length=255)
	statute = models.CharField(max_length = 255, blank = True, null = True)
	count = models.IntegerField(default = 0)
	average_bond = models.FloatField(default = 0)
	black_count = models.FloatField(default = 0)
	white_average_bond = models.FloatField(default = 0)
	black_average_bond = models.FloatField(default = 0)

	CLASS_CHOICES = (
		('Federal', 'Federal'),
		('State', 'State'),
		('City', 'City')
		)
	is_felony = models.BooleanField(default = False)
	crime_class = models.CharField(max_length = 255, null = True, blank = True, choices = CLASS_CHOICES)

	def __unicode__(self):
		return self.description

	def get_average_bond(self):
		charges = self.bookingcharge_set.all()

		bonds = []

		for c in charges:
			bonds.append(c.booking.total_bond)

		print bonds

		return mean(bonds)

	def get_counts(self):
		return self.bookingcharge_set.all().count()

		#counts = []
		#races = Race.objects.all()

		#for r in races:
	
		#	counts[r.name] = []


	def get_black_percent(self):
		blacks = self.bookingcharge_set.filter(identity__race__name = 'B')
		b = len(blacks)
		alls = self.bookingcharge_set.all()
		a = len(alls)
		return float(b) / a

	def get_race_average(self, race):
		charges = self.bookingcharge_set.filter(identity__race__name = race)
		bonds = []
		for c in charges:
			bonds.append(c.booking.total_bond)
		print bonds
		return mean(bonds)



	def build_stats(self):
		self.count = self.get_counts()
		self.average_bond = self.get_average_bond()
		self.black_count = self.get_black_percent()
		black = 'B'
		white = 'W'
		self.black_average_bond = self.get_race_average(black)
		self.white_average_bond = self.get_race_average(white)
		self.save()



	def save(self, *args, **kwargs):
		super(Charge, self).save(*args, **kwargs)

class Race(models.Model):
 	name = models.CharField(max_length=50)
 	count = models.IntegerField(default = 0)
	average_bond = models.FloatField(default = 0)
	median_bond = models.FloatField(default = 0)
	total_days = models.IntegerField(default = 0)

	def get_days(self):
		days = 0
		inmates = self.inmate_set.all()
		for i in inmates:
			for b in i.booking_set.all():
				days += b.booking_length
		print days
		return days


	def get_average_bond(self):
		charges = self.bookingcharge_set.all()
		bonds = []
		for c in charges:
			bonds.append(c.booking.total_bond)
		print bonds
		return mean(bonds)

	def get_median_bond(self):
		charges = self.bookingcharge_set.all()
		bonds = []
		for c in charges:
			bonds.append(c.booking.total_bond)
		print bonds
		return median(bonds)

	def get_counts(self):
		return self.bookingcharge_set.all().count()
		#counts = []
		#races = Race.objects.all()

		#for r in races:
		#	counts[r.name] = []

	def build_stats(self):
		#self.count = self.get_counts()
		#self.average_bond = self.get_average_bond()
		self.total_days = self.get_days()
		self.median_bond = self.get_median_bond()
		self.save()
	def save(self, *args, **kwargs):
		super(Race, self).save(*args, **kwargs)


 	#def build_bonds()
 	def __unicode__(self):
 		return self.name
 		
class City(models.Model):
	name = models.CharField(max_length=255, blank = True, null = True)
	state = models.CharField(max_length = 20, blank = True, null = True)
	def __unicode__(self):
		return self.name


class Address(models.Model):
	string = models.CharField(max_length = 255)
	attempted = models.BooleanField(default = False)
	verified = models.BooleanField(default = False)
	##eventually... we're going to want point geography field. But not yet.
	last_known = models.BooleanField(default = False)
	point_location = models.PointField('GeoDjango point field of this address', null=True, geography=True)

	#def geocode(self):
	def get_race(self):
		inmates = self.inmate_set.all()
		inmate = inmates[0]
		return inmate.race.name

	def get_name(self):
		inmates = self.inmate_set.all()
		inmate = inmates[0]
		return inmate.name.title()

	def get_bond(self):
		inmates = self.inmate_set.all()
		inmate = inmates[0]
		booking_thing = inmate.booking_set.all()[:1].get()
		return booking_thing.total_bond

	def get_booking_date(self):
		inmates = self.inmate_set.all()
		inmate = inmates[0]
		booking_thing = inmate.booking_set.all()[:1].get()
		return booking_thing.booking_date

	def get_bond(self):
		inmates = self.inmate_set.all()
		inmate = inmates[0]
		booking_thing = inmate.booking_set.all()[:1].get()

		return booking_thing.total_bond

	def get_charges(self):
		inmate = self.inmate_set.all()[:1].get()
		booking_thing = inmate.booking_set.all()[:1].get()
		
		charges = ''
		print booking_thing

		try:
			for c in booking_thing.bookingcharge_set.all():
			#charge_thing = booking_thing.bookingcharge_set.all()[:1].get()
#			return charge_thing.charge.description.title()
				charges += c.charge.description.title()
				if len(booking_thing.bookingcharge_set.all()) > 1:
					charges += ', '
			return charges			

		except ObjectDoesNotExist:
			return "No charge listed"

	def __unicode__(self):
		return self.string

class Inmate(models.Model):
	name = models.CharField(max_length=255)
	first_name = models.CharField(max_length= 50, null =True)
	middle_name = models.CharField(max_length= 50, null =True)
	last_name = models.CharField(max_length= 50, null =True)
	jacket_number = models.CharField(max_length=255, blank = True)
	race = models.ForeignKey(Race, null=True)
	gender = models.CharField(max_length = 6, null = True)
	address = models.ForeignKey(Address, blank = True, null= True)
	def __unicode__(self):
		return self.last_name
	#def get_race(self):


#### Many to many address field - then get last known address based on scrape####
#### 
class HousingFacility(models.Model):
	name = models.CharField(max_length = 10)
	def __unicode__(self):
		return self.name


class Block(models.Model):
	name = models.CharField(max_length = 10)
	housing_facility = models.ForeignKey(HousingFacility, null = True)
	
	def build_races(self):
		
		
		counts = []
		for r in Race.objects.all():
			
			count = self.booking_set.filter(identity__race = r).count()
			
			counts.append({r.name : count })
		return counts
	def __unicode__(self):
		return self.name

class Booking(models.Model):
	time_created = models.DateTimeField(null = True)
	last_seen = models.DateTimeField(null = True)
	identity = models.ForeignKey(Inmate, null = True)
	booking_date = models.DateField(null=True)
	booking_time = models.TimeField(null=True)
	rough_release_date = models.DateTimeField(null = True)
	booking_number = models.CharField(max_length=255, null = True)
	booking_length = models.IntegerField(null =True, blank =True)
	housing_facility = models.CharField(max_length = 10, null = True)
	age = models.IntegerField(null=True, blank=True)
	total_bond = models.FloatField(null = True,blank = True)
	block = models.CharField(max_length = 10, null = True)
	blockmodel = models.ForeignKey(Block, null= True)


	def build_block(self):
		housing_facility_import, hf_created = HousingFacility.objects.get_or_create(
			name = self.housing_facility
			)
		block_import, block_created = Block.objects.get_or_create(
			name = self.block,
			housing_facility = housing_facility_import
		)
		self.blockmodel = block_import
		self.save()

	#for csv export -- sorry, everyone. I feel shame for doing this.
	#drop these when you're done, Nathaniel.
	#race = models.CharField(null = True, blank = True, max_length=255)
	#gender = models.CharField(null = True, blank = True, max_length =255)
	#name = models.CharField(null = True, blank = True, max_length = 255)
	#charges_list = models.TextField(null = True, blank = True)
	
	def get_release_date(self):
		#self.rough_release_date = None
		#self.save()
		now = datetime.datetime.now()
		d = now - self.last_seen
		print d.days
		if d.days > 0:

			self.rough_release_date = self.last_seen
			print self.rough_release_date
		
			self.save()
	def get_booking_length(self):
		print self.identity.name
		time = self.last_seen.date() - self.booking_date
		return time.days
		
	def save_things(self):
		#self.get_release_date()
		self.booking_length = self.get_booking_length()
		self.save()

	def save(self, *args, **kwargs):
	#	length_of_booking = self.get_booking_length()
	#	self.booking_length = length_of_booking
	#	print lengthof__booking
		#if self.identity.race:
		#	self.race = self.identity.race.name 
		
		#charges_set = []
		#bond = 0
		#for b in bookings:
		#	charges_set.append(b.charge.description)
		#	if b.bond_amount:
		#		print b.bond_amount
		#		bond += b.bond_amount
		#self.total_bond = bond
		#self.gender = arbritrarily_first_booking.gender
		#self.charges_list = charges_set


		super(Booking, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.identity.name
	
#just a description for statuses (hearing, bond court, etc) for easy(er) filtering
class Action(models.Model):
	description = models.CharField(max_length = 100)

#point in the criminal justice system
class SystemPoint(models.Model):
	action = models.ForeignKey(Action)
	court_datetime = models.DateTimeField()

class BookingCharge(models.Model):
	identity = models.ForeignKey(Inmate)
	booking = models.ForeignKey(Booking, null = True)
	charge = models.ForeignKey(Charge)
	race = models.ForeignKey(Race)
	system_points = models.ManyToManyField(SystemPoint)
	release_date = models.DateField(null=True)
	#GENDER_CHOICES = (
#		('m', "male")
#		('f', "female")
#		)
	#
#	gender = models.CharField(max_length = 255, null = True)
	#age = models.IntegerField(blank=True, null = True)
	
	#bond_type = models.CharField(max_length = 255, null = True)
	#bond_amount = models.FloatField(blank = True, null = True)
	
#	booking_number = models.CharField(max_length=255, blank = True, null = True)
#	booking_date = models.DateField(null = True)
#	release_date = models.DateField(null = True)

#	photo_filename = models.CharField(max_length=255, blank	= True, null = True)

	#random fields...
#	city = models.ForeignKey(City, null = True)
#	zip_code = models.IntegerField(blank = True, null = True)

	def __unicode__(self):
		return self.charge.description
	def save(self, *args, **kwargs):
		super(BookingCharge, self).save(*args, **kwargs)

