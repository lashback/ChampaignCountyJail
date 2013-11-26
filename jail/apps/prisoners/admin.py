from django.contrib.gis import admin
from apps.prisoners.models import *

class BookingChargeAdmin(admin.ModelAdmin):
	pass
class InmateAdmin(admin.ModelAdmin):
	list_display = ['name','jacket_number']

class BookingAdmin(admin.ModelAdmin):
	list_display = ['identity', 'booking_date', 'total_bond', 'rough_release_date', 'last_seen']
	list_filter = ['time_created', 'housing_facility', 'block']

class AddressAdmin(admin.OSMGeoAdmin):
	list_display = ['string', 'verified', 'attempted', 'point_location']
	pass

class RaceAdmin(admin.ModelAdmin):
	pass

class ChargeAdmin(admin.ModelAdmin):
	list_display = ['description', 'statute', 'crime_class']



admin.site.register(Charge, ChargeAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(BookingCharge, BookingChargeAdmin)
admin.site.register(Inmate, InmateAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Race, RaceAdmin)
