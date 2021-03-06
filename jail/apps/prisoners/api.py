from tastypie.contrib.gis.resources import ModelResource  # Using GeoDjango ModelResource
from django.http import HttpResponse
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from apps.prisoners.models import *
from tastypie.cache import SimpleCache
from tastypie import fields
from django.utils import simplejson as json


class AddressResource(ModelResource):
	class Meta:
		queryset = Address.objects.filter(point_location__isnull=False)
		resource_name = 'address'
		allowed_methods = ['get']
		excludes = ['point_location']
		max_limit = None
		filtering = {
			'type': ALL		
		}

	def dehydrate(self, bundle):
		bundle.data['type'] = 'Feature'
		#bundle.data['properties'] = {}
		bundle.data['geometry'] = json.loads(bundle.obj.point_location.geojson)
		bundle.data['properties'] = {
			'race': bundle.obj.get_race(),
			'name': bundle.obj.get_name(),
			'charge':bundle.obj.get_charges(),
			'bond': bundle.obj.get_bond(),
			'booking_date': bundle.obj.get_booking_date()
		}	

		return bundle

class BlockResource(ModelResource):
	class Meta:
		queryset = Block.objects.all()
		resource_name = 'block'
		allowed_methods = ['get']
		max_limit = None
		filtering = {
			'type': ALL
		}

	def dehydrate(self,bundle):
		bundle.data['properties'] = {
			'races': bundle.obj.build_races()

		}
		return bundle
