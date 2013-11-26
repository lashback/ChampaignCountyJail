from django.core.management.base import BaseCommand
import os
from settings.common import STATIC_ROOT
from django.test.client import Client
#import boto
#from boto.s3.connection import S3Connection


class Command(BaseCommand):
    help = 'Parse super-complex totals into static JSON, upload to S3.'

#    def deploy_to_s3(self, inputbucket, inputkey, inputfile):
#        target_bucket = None
#        conn = S3Connection(S3_ACCESS_KEY, S3_SECRET_KEY)
#        for bucket in conn.get_all_buckets():
#            if bucket.name == inputbucket:
#                target_bucket = bucket
#        remote_json = boto.s3.key.Key(target_bucket)
#        remote_json.key = inputkey
#        remote_json.set_contents_from_filename(inputfile)
#        remote_json.set_acl('public-read')

    def cache_and_deliver(self, content, filename):
        if not os.path.exists(os.path.join(STATIC_ROOT, 'json')):
            os.makedirs(os.path.join(STATIC_ROOT, 'json'))

        cached_json = open(os.path.join(STATIC_ROOT, 'json', filename), 'w')
        cached_json.write(content)
        cached_json.close()

        self.stdout.write('Cached file: %s.\n' % (filename,))

        # self.deploy_to_s3('static.apps.cironline.org', 'border-seizures/json/%s' % (filename,), os.path.join(STATIC_ROOT, 'json', filename))

        # self.stdout.write('Uploaded file: %s.\n' % (filename,))

    def handle(self, *args, **options):
        try:
            c = Client()

            response = c.get('/api/v1/station/?format=json&limit=200', {}, follow=True)
            self.cache_and_deliver(response.content, 'bp_station_cached.json')

            response = c.get('/api/v1/sector/?format=json&limit=50', {}, follow=True)
            self.cache_and_deliver(response.content, 'bp_sector_cached.json')

            response = c.get('/api/v1/reasonforce/?format=json&limit=15', {}, follow=True)
            self.cache_and_deliver(response.content, 'reasonforce_cached.json')

            response = c.get('/api/v1/typeforce/?format=json&limit=15', {}, follow=True)
            self.cache_and_deliver(response.content, 'typeforce_cached.json')

            response = c.get('/api/v1/agents/?format=json&limit=1', {}, follow = True)
            self.cache_and_deliver(response.content, 'agents_cached.json')
            self.stdout.write('Successfully uploaded JSON files.\n')

        except AttributeError:
            raise
