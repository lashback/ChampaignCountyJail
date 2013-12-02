#from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry
from omgeo import Geocoder
from numpy import median, mean

# Create your models here.
class Charge(models.Model):
	description = models.CharField(max_length=255)
	statute = models.CharField(max_length = 255, blank = True, null = True)
	CLASS_CHOICES = (
		('Federal', 'Federal'),
		('State', 'State'),
		('City', 'City')
		)
	crime_class = models.CharField(max_length = 255, null = True, blank = True, choices = CLASS_CHOICES)

	def __unicode__(self):
		return self.description

	def get_counts(self):
		counts = []
		races = Race.objects.all()

		for r in races:
			counts[r.name] = []

class Race(models.Model):
 	name = models.CharField(max_length=50)

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
		return self.name
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
	

	def get_booking_length(self):
		print self.identity.name
		if self.release_date:
			time = self.release_date - self.booking_date
			return time.days
		else:
			return None

	def save_things(self):
		bookings = self.bookingcharge_set.all()
		arbritrarily_first_booking = bookings[0]
		self.name = self.identity.name
		if arbritrarily_first_booking.race:
			self.race = arbritrarily_first_booking.race.name
			print self.race
		print self.names
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
	

class BookingCharge(models.Model):
	identity = models.ForeignKey(Inmate)
	booking = models.ForeignKey(Booking, null = True)
	charge = models.ForeignKey(Charge)
	race = models.ForeignKey(Race)
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
		return self.identity
	def save(self, *args, **kwargs):
		super(BookingCharge, self).save(*args, **kwargs)

	