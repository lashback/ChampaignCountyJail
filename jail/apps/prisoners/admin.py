from django.contrib.gis import admin
from apps.prisoners.models import *

class BookingChargeAdmin(admin.ModelAdmin):
	pass
class InmateAdmin(admin.ModelAdmin):
	list_display = ['name','jacket_number']

class BookingAdmin(admin.ModelAdmin):
	list_display = ['identity', 'booking_date', 'total_bond', 'rough_release_date', 'last_seen', 'address', 'booking_length']
	list_filter = ['time_created', 'housing_facility', 'block']
	def address(self, obj):
		return obj.identity.address.string

class AddressAdmin(admin.OSMGeoAdmin):
	list_display = ['string', 'verified', 'attempted', 'point_location']
	pass

class RaceAdmin(admin.ModelAdmin):
	list_display = ['name', 'count','average_bond', 'median_bond', 'total_days']


class ChargeAdmin(admin.ModelAdmin):
	list_display = ['description', 'statute' ,'crime_class', 'count','average_bond', 'white_average_bond', 'black_average_bond', 'black_count']

admin.site.register(Charge, ChargeAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(BookingCharge, BookingChargeAdmin)
admin.site.register(Inmate, InmateAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Race, RaceAdmin)
