from django.http import HttpResponse
from django.template import Context, loader
from apps.prisoners.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
import os
from django.template import RequestContext
import datetime
#this isn't working

def map(request):
	return render_to_response('map.html')

def bookings(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="bookings.csv"'

	# The data is hard-coded here, but you could load it from a database or
	# some other source.
	csv_data = [('Name', 'BookingDate', 'Race', 'Gender', 'Total Bond', 'Address', 'Facility')]
	for b in Booking.objects.filter(time_created__gt=datetime.date(2013, 1, 3)):
		
		csv_data += (
			(b.identity.name, b.booking_date, b.identity.race.name, b.identity.gender, b.total_bond, b.identity.address, b.housing_facility)
		)

	t = loader.get_template('bookings.txt')
	c = Context({
	    'data': csv_data,
	})
	response.write(t.render(c))
	return response
