# Generated by Django 2.1.2 on 2018-10-09 18:20

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PlanetOsmLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osm_id', models.BigIntegerField(blank=True, null=True)),
                ('access', models.TextField(blank=True, null=True)),
                ('addr_housename', models.TextField(blank=True, db_column='addr:housename', null=True)),
                ('addr_housenumber', models.TextField(blank=True, db_column='addr:housenumber', null=True)),
                ('addr_interpolation', models.TextField(blank=True, db_column='addr:interpolation', null=True)),
                ('admin_level', models.TextField(blank=True, null=True)),
                ('aerialway', models.TextField(blank=True, null=True)),
                ('aeroway', models.TextField(blank=True, null=True)),
                ('amenity', models.TextField(blank=True, null=True)),
                ('area', models.TextField(blank=True, null=True)),
                ('barrier', models.TextField(blank=True, null=True)),
                ('bicycle', models.TextField(blank=True, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
                ('bridge', models.TextField(blank=True, null=True)),
                ('boundary', models.TextField(blank=True, null=True)),
                ('building', models.TextField(blank=True, null=True)),
                ('construction', models.TextField(blank=True, null=True)),
                ('covered', models.TextField(blank=True, null=True)),
                ('culvert', models.TextField(blank=True, null=True)),
                ('cutting', models.TextField(blank=True, null=True)),
                ('denomination', models.TextField(blank=True, null=True)),
                ('disused', models.TextField(blank=True, null=True)),
                ('embankment', models.TextField(blank=True, null=True)),
                ('foot', models.TextField(blank=True, null=True)),
                ('generator_source', models.TextField(blank=True, db_column='generator:source', null=True)),
                ('harbour', models.TextField(blank=True, null=True)),
                ('highway', models.TextField(blank=True, null=True)),
                ('historic', models.TextField(blank=True, null=True)),
                ('horse', models.TextField(blank=True, null=True)),
                ('intermittent', models.TextField(blank=True, null=True)),
                ('junction', models.TextField(blank=True, null=True)),
                ('landuse', models.TextField(blank=True, null=True)),
                ('layer', models.TextField(blank=True, null=True)),
                ('leisure', models.TextField(blank=True, null=True)),
                ('lock', models.TextField(blank=True, null=True)),
                ('man_made', models.TextField(blank=True, null=True)),
                ('military', models.TextField(blank=True, null=True)),
                ('motorcar', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('natural', models.TextField(blank=True, null=True)),
                ('office', models.TextField(blank=True, null=True)),
                ('oneway', models.TextField(blank=True, null=True)),
                ('operator', models.TextField(blank=True, null=True)),
                ('place', models.TextField(blank=True, null=True)),
                ('population', models.TextField(blank=True, null=True)),
                ('power', models.TextField(blank=True, null=True)),
                ('power_source', models.TextField(blank=True, null=True)),
                ('public_transport', models.TextField(blank=True, null=True)),
                ('railway', models.TextField(blank=True, null=True)),
                ('ref', models.TextField(blank=True, null=True)),
                ('religion', models.TextField(blank=True, null=True)),
                ('route', models.TextField(blank=True, null=True)),
                ('service', models.TextField(blank=True, null=True)),
                ('shop', models.TextField(blank=True, null=True)),
                ('sport', models.TextField(blank=True, null=True)),
                ('surface', models.TextField(blank=True, null=True)),
                ('toll', models.TextField(blank=True, null=True)),
                ('tourism', models.TextField(blank=True, null=True)),
                ('tower_type', models.TextField(blank=True, db_column='tower:type', null=True)),
                ('tracktype', models.TextField(blank=True, null=True)),
                ('tunnel', models.TextField(blank=True, null=True)),
                ('water', models.TextField(blank=True, null=True)),
                ('waterway', models.TextField(blank=True, null=True)),
                ('wetland', models.TextField(blank=True, null=True)),
                ('width', models.TextField(blank=True, null=True)),
                ('wood', models.TextField(blank=True, null=True)),
                ('z_order', models.IntegerField(blank=True, null=True)),
                ('way_area', models.FloatField(blank=True, null=True)),
                ('way', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'planet_osm_line',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanetOsmNodes',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('lat', models.IntegerField()),
                ('lon', models.IntegerField()),
            ],
            options={
                'db_table': 'planet_osm_nodes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanetOsmPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osm_id', models.BigIntegerField(blank=True, null=True)),
                ('access', models.TextField(blank=True, null=True)),
                ('addr_housename', models.TextField(blank=True, db_column='addr:housename', null=True)),
                ('addr_housenumber', models.TextField(blank=True, db_column='addr:housenumber', null=True)),
                ('addr_interpolation', models.TextField(blank=True, db_column='addr:interpolation', null=True)),
                ('admin_level', models.TextField(blank=True, null=True)),
                ('aerialway', models.TextField(blank=True, null=True)),
                ('aeroway', models.TextField(blank=True, null=True)),
                ('amenity', models.TextField(blank=True, null=True)),
                ('area', models.TextField(blank=True, null=True)),
                ('barrier', models.TextField(blank=True, null=True)),
                ('bicycle', models.TextField(blank=True, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
                ('bridge', models.TextField(blank=True, null=True)),
                ('boundary', models.TextField(blank=True, null=True)),
                ('building', models.TextField(blank=True, null=True)),
                ('capital', models.TextField(blank=True, null=True)),
                ('construction', models.TextField(blank=True, null=True)),
                ('covered', models.TextField(blank=True, null=True)),
                ('culvert', models.TextField(blank=True, null=True)),
                ('cutting', models.TextField(blank=True, null=True)),
                ('denomination', models.TextField(blank=True, null=True)),
                ('disused', models.TextField(blank=True, null=True)),
                ('ele', models.TextField(blank=True, null=True)),
                ('embankment', models.TextField(blank=True, null=True)),
                ('foot', models.TextField(blank=True, null=True)),
                ('generator_source', models.TextField(blank=True, db_column='generator:source', null=True)),
                ('harbour', models.TextField(blank=True, null=True)),
                ('highway', models.TextField(blank=True, null=True)),
                ('historic', models.TextField(blank=True, null=True)),
                ('horse', models.TextField(blank=True, null=True)),
                ('intermittent', models.TextField(blank=True, null=True)),
                ('junction', models.TextField(blank=True, null=True)),
                ('landuse', models.TextField(blank=True, null=True)),
                ('layer', models.TextField(blank=True, null=True)),
                ('leisure', models.TextField(blank=True, null=True)),
                ('lock', models.TextField(blank=True, null=True)),
                ('man_made', models.TextField(blank=True, null=True)),
                ('military', models.TextField(blank=True, null=True)),
                ('motorcar', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('natural', models.TextField(blank=True, null=True)),
                ('office', models.TextField(blank=True, null=True)),
                ('oneway', models.TextField(blank=True, null=True)),
                ('operator', models.TextField(blank=True, null=True)),
                ('place', models.TextField(blank=True, null=True)),
                ('population', models.TextField(blank=True, null=True)),
                ('power', models.TextField(blank=True, null=True)),
                ('power_source', models.TextField(blank=True, null=True)),
                ('public_transport', models.TextField(blank=True, null=True)),
                ('railway', models.TextField(blank=True, null=True)),
                ('ref', models.TextField(blank=True, null=True)),
                ('religion', models.TextField(blank=True, null=True)),
                ('route', models.TextField(blank=True, null=True)),
                ('service', models.TextField(blank=True, null=True)),
                ('shop', models.TextField(blank=True, null=True)),
                ('sport', models.TextField(blank=True, null=True)),
                ('surface', models.TextField(blank=True, null=True)),
                ('toll', models.TextField(blank=True, null=True)),
                ('tourism', models.TextField(blank=True, null=True)),
                ('tower_type', models.TextField(blank=True, db_column='tower:type', null=True)),
                ('tunnel', models.TextField(blank=True, null=True)),
                ('water', models.TextField(blank=True, null=True)),
                ('waterway', models.TextField(blank=True, null=True)),
                ('wetland', models.TextField(blank=True, null=True)),
                ('width', models.TextField(blank=True, null=True)),
                ('wood', models.TextField(blank=True, null=True)),
                ('z_order', models.IntegerField(blank=True, null=True)),
                ('way', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'planet_osm_point',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanetOsmPolygon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osm_id', models.BigIntegerField(blank=True, null=True)),
                ('access', models.TextField(blank=True, null=True)),
                ('addr_housename', models.TextField(blank=True, db_column='addr:housename', null=True)),
                ('addr_housenumber', models.TextField(blank=True, db_column='addr:housenumber', null=True)),
                ('addr_interpolation', models.TextField(blank=True, db_column='addr:interpolation', null=True)),
                ('admin_level', models.TextField(blank=True, null=True)),
                ('aerialway', models.TextField(blank=True, null=True)),
                ('aeroway', models.TextField(blank=True, null=True)),
                ('amenity', models.TextField(blank=True, null=True)),
                ('area', models.TextField(blank=True, null=True)),
                ('barrier', models.TextField(blank=True, null=True)),
                ('bicycle', models.TextField(blank=True, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
                ('bridge', models.TextField(blank=True, null=True)),
                ('boundary', models.TextField(blank=True, null=True)),
                ('building', models.TextField(blank=True, null=True)),
                ('construction', models.TextField(blank=True, null=True)),
                ('covered', models.TextField(blank=True, null=True)),
                ('culvert', models.TextField(blank=True, null=True)),
                ('cutting', models.TextField(blank=True, null=True)),
                ('denomination', models.TextField(blank=True, null=True)),
                ('disused', models.TextField(blank=True, null=True)),
                ('embankment', models.TextField(blank=True, null=True)),
                ('foot', models.TextField(blank=True, null=True)),
                ('generator_source', models.TextField(blank=True, db_column='generator:source', null=True)),
                ('harbour', models.TextField(blank=True, null=True)),
                ('highway', models.TextField(blank=True, null=True)),
                ('historic', models.TextField(blank=True, null=True)),
                ('horse', models.TextField(blank=True, null=True)),
                ('intermittent', models.TextField(blank=True, null=True)),
                ('junction', models.TextField(blank=True, null=True)),
                ('landuse', models.TextField(blank=True, null=True)),
                ('layer', models.TextField(blank=True, null=True)),
                ('leisure', models.TextField(blank=True, null=True)),
                ('lock', models.TextField(blank=True, null=True)),
                ('man_made', models.TextField(blank=True, null=True)),
                ('military', models.TextField(blank=True, null=True)),
                ('motorcar', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('natural', models.TextField(blank=True, null=True)),
                ('office', models.TextField(blank=True, null=True)),
                ('oneway', models.TextField(blank=True, null=True)),
                ('operator', models.TextField(blank=True, null=True)),
                ('place', models.TextField(blank=True, null=True)),
                ('population', models.TextField(blank=True, null=True)),
                ('power', models.TextField(blank=True, null=True)),
                ('power_source', models.TextField(blank=True, null=True)),
                ('public_transport', models.TextField(blank=True, null=True)),
                ('railway', models.TextField(blank=True, null=True)),
                ('ref', models.TextField(blank=True, null=True)),
                ('religion', models.TextField(blank=True, null=True)),
                ('route', models.TextField(blank=True, null=True)),
                ('service', models.TextField(blank=True, null=True)),
                ('shop', models.TextField(blank=True, null=True)),
                ('sport', models.TextField(blank=True, null=True)),
                ('surface', models.TextField(blank=True, null=True)),
                ('toll', models.TextField(blank=True, null=True)),
                ('tourism', models.TextField(blank=True, null=True)),
                ('tower_type', models.TextField(blank=True, db_column='tower:type', null=True)),
                ('tracktype', models.TextField(blank=True, null=True)),
                ('tunnel', models.TextField(blank=True, null=True)),
                ('water', models.TextField(blank=True, null=True)),
                ('waterway', models.TextField(blank=True, null=True)),
                ('wetland', models.TextField(blank=True, null=True)),
                ('width', models.TextField(blank=True, null=True)),
                ('wood', models.TextField(blank=True, null=True)),
                ('z_order', models.IntegerField(blank=True, null=True)),
                ('way_area', models.FloatField(blank=True, null=True)),
                ('way', django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'planet_osm_polygon',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanetOsmRels',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('way_off', models.SmallIntegerField(blank=True, null=True)),
                ('rel_off', models.SmallIntegerField(blank=True, null=True)),
                ('parts', models.TextField(blank=True, null=True)),
                ('members', models.TextField(blank=True, null=True)),
                ('tags', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'planet_osm_rels',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanetOsmRoads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osm_id', models.BigIntegerField(blank=True, null=True)),
                ('access', models.TextField(blank=True, null=True)),
                ('addr_housename', models.TextField(blank=True, db_column='addr:housename', null=True)),
                ('addr_housenumber', models.TextField(blank=True, db_column='addr:housenumber', null=True)),
                ('addr_interpolation', models.TextField(blank=True, db_column='addr:interpolation', null=True)),
                ('admin_level', models.TextField(blank=True, null=True)),
                ('aerialway', models.TextField(blank=True, null=True)),
                ('aeroway', models.TextField(blank=True, null=True)),
                ('amenity', models.TextField(blank=True, null=True)),
                ('area', models.TextField(blank=True, null=True)),
                ('barrier', models.TextField(blank=True, null=True)),
                ('bicycle', models.TextField(blank=True, null=True)),
                ('brand', models.TextField(blank=True, null=True)),
                ('bridge', models.TextField(blank=True, null=True)),
                ('boundary', models.TextField(blank=True, null=True)),
                ('building', models.TextField(blank=True, null=True)),
                ('construction', models.TextField(blank=True, null=True)),
                ('covered', models.TextField(blank=True, null=True)),
                ('culvert', models.TextField(blank=True, null=True)),
                ('cutting', models.TextField(blank=True, null=True)),
                ('denomination', models.TextField(blank=True, null=True)),
                ('disused', models.TextField(blank=True, null=True)),
                ('embankment', models.TextField(blank=True, null=True)),
                ('foot', models.TextField(blank=True, null=True)),
                ('generator_source', models.TextField(blank=True, db_column='generator:source', null=True)),
                ('harbour', models.TextField(blank=True, null=True)),
                ('highway', models.TextField(blank=True, null=True)),
                ('historic', models.TextField(blank=True, null=True)),
                ('horse', models.TextField(blank=True, null=True)),
                ('intermittent', models.TextField(blank=True, null=True)),
                ('junction', models.TextField(blank=True, null=True)),
                ('landuse', models.TextField(blank=True, null=True)),
                ('layer', models.TextField(blank=True, null=True)),
                ('leisure', models.TextField(blank=True, null=True)),
                ('lock', models.TextField(blank=True, null=True)),
                ('man_made', models.TextField(blank=True, null=True)),
                ('military', models.TextField(blank=True, null=True)),
                ('motorcar', models.TextField(blank=True, null=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('natural', models.TextField(blank=True, null=True)),
                ('office', models.TextField(blank=True, null=True)),
                ('oneway', models.TextField(blank=True, null=True)),
                ('operator', models.TextField(blank=True, null=True)),
                ('place', models.TextField(blank=True, null=True)),
                ('population', models.TextField(blank=True, null=True)),
                ('power', models.TextField(blank=True, null=True)),
                ('power_source', models.TextField(blank=True, null=True)),
                ('public_transport', models.TextField(blank=True, null=True)),
                ('railway', models.TextField(blank=True, null=True)),
                ('ref', models.TextField(blank=True, null=True)),
                ('religion', models.TextField(blank=True, null=True)),
                ('route', models.TextField(blank=True, null=True)),
                ('service', models.TextField(blank=True, null=True)),
                ('shop', models.TextField(blank=True, null=True)),
                ('sport', models.TextField(blank=True, null=True)),
                ('surface', models.TextField(blank=True, null=True)),
                ('toll', models.TextField(blank=True, null=True)),
                ('tourism', models.TextField(blank=True, null=True)),
                ('tower_type', models.TextField(blank=True, db_column='tower:type', null=True)),
                ('tracktype', models.TextField(blank=True, null=True)),
                ('tunnel', models.TextField(blank=True, null=True)),
                ('water', models.TextField(blank=True, null=True)),
                ('waterway', models.TextField(blank=True, null=True)),
                ('wetland', models.TextField(blank=True, null=True)),
                ('width', models.TextField(blank=True, null=True)),
                ('wood', models.TextField(blank=True, null=True)),
                ('z_order', models.IntegerField(blank=True, null=True)),
                ('way_area', models.FloatField(blank=True, null=True)),
                ('way', django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326)),
            ],
            options={
                'db_table': 'planet_osm_roads',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlanetOsmWays',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('nodes', models.TextField()),
                ('tags', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'planet_osm_ways',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Topology',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1, unique=True)),
                ('srid', models.IntegerField()),
                ('precision', models.FloatField()),
                ('hasz', models.BooleanField()),
            ],
            options={
                'db_table': 'topology',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('topology', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='myapp.Topology')),
                ('layer_id', models.IntegerField()),
                ('schema_name', models.CharField(max_length=1)),
                ('table_name', models.CharField(max_length=1)),
                ('feature_column', models.CharField(max_length=1)),
                ('feature_type', models.IntegerField()),
                ('level', models.IntegerField()),
                ('child_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'layer',
                'managed': False,
            },
        ),
    ]