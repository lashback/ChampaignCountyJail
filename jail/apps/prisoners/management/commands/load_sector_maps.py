import os
from django.core.management.base import BaseCommand
from django.contrib.gis.utils import LayerMapping
from apps.incidents.models import BPSectorMap, BPSector, BPStation
from settings.common import SITE_ROOT


class Command(BaseCommand):
    help = 'Matches Border Patrol sector names and multipolygon borders from shapefile'

    def handle(self, *args, **options):
        try:
            if len(args) > 0:
                self.stdout.write('Using manual shapefile location ...\n')
                sector_shp = args[0]
            else:
                self.stdout.write('Using default shapefile location ...\n')
                working_dir = os.path.join(SITE_ROOT, '../data')
                sector_shp = os.path.join(working_dir, 'border_patrol_sectors_new_miami/border_patrol_sectors_new_miami.shp')

            # Auto-generated `LayerMapping` dictionary for BPSectorMap model
            bpsectormap_mapping = {
                'objectid': 'objectid',
                'sec_name': 'sec_name',
                'sec_code': 'sec_code',
                'area_sqmi': 'area_sqmi',
                # Following fields are totally unverified, so not using to prevent confusion
                # 'marijuana_field': 'marijuana_',
                # 'cocaine_lb': 'cocaine_lb',
                # 'heroin_lbs': 'heroin_lbs',
                # 'meth_lbspe': 'meth_lbspe',
                # 'numcrossin': 'numcrossin',
                # 'numillegal': 'numillegal',
                # 'numsmuggle': 'numsmuggle',
                'shape_leng': 'shape_leng',
                'shape_area': 'shape_area',
                'geom_orig': 'geom_orig',
                'geom': 'MULTIPOLYGON',
            }

            lm = LayerMapping(
                BPSectorMap,
                sector_shp,
                bpsectormap_mapping,
                transform=False,
                encoding='iso-8859-1'
            )

            lm.save(strict=True, verbose=True)
            
                
            for s in BPSector.objects.all():
                try:
                    sm = BPSectorMap.objects.get(sec_name = s.name)
                    self.stdout.write(sm.sec_name)
                    s.aor_multipoly = sm.geom
                    s.save()
                    self.stdout.write('%s Sector matched.\n' % (s.name,))
                except:
                    self.stdout.write('   WARNING: No shapefile match found for %s Sector.\n' % (s.name,))

            #Re-save BPStation objects to get sector matches
            for s in BPStation.objects.all():
                s.save()

            self.stdout.write('Successfully matched Border Patrol sectors to their AOR boundaries.\n')
        except AttributeError:
            raise
