from django.shortcuts import render
from .models import PlanetOsmPoint
from .models import PlanetOsmLine
from .models import PlanetOsmPolygon
from django.http import HttpResponse
from django.core.serializers import serialize
from itertools import chain
import json


def index(request):
    return render(request, 'index.html')


def get_nearest_stations(request):
    queryres1 = PlanetOsmPoint.objects.raw('SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                          'FROM planet_osm_point WHERE railway LIKE \'station\' '
                                          'AND ST_DWithin(ST_Transform(way,4326), '
                                          'ST_SetSRID(ST_Point(%s, %s),4326), '
                                          '56::float*%s::float/6371000::float)',
                                           [request.GET['lon'], request.GET['lat'], request.GET['dist']])
    queryres2 = PlanetOsmPolygon.objects.raw('SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                          'FROM planet_osm_polygon WHERE railway LIKE \'station\' '
                                          'AND ST_DWithin(ST_Transform(way,4326), '
                                          'ST_SetSRID(ST_Point(%s, %s),4326), '
                                          '56::float*%s::float/6371000::float)',
                                           [request.GET['lon'], request.GET['lat'], request.GET['dist']])
    result_list = list(chain(queryres1, queryres2))
    railways = serialize('geojson', result_list, geometry_field='way', fields=('name', 'geometry'))
    return HttpResponse(railways)


def get_station_w_routes(request):
    start = PlanetOsmPoint.objects.raw('SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                          'FROM planet_osm_point WHERE railway LIKE \'station\' '
                                          'AND ST_DISTANCE(ST_Transform(way,4326), '
                                          'ST_SetSRID(ST_Point(%s, %s),4326)) '
                                          '= (SELECT min(ST_DISTANCE(ST_Transform(way,4326), '
                                          'ST_SetSRID(ST_Point(%s, %s),4326))) '
                                          'FROM planet_osm_point WHERE railway LIKE \'station\')',
                                       [request.GET['startLon'], request.GET['startLat'], request.GET['startLon'], request.GET['startLat']])
    rail = PlanetOsmLine.objects.raw('WITH my_station AS (SELECT ST_Transform(way,4326) as geometry '
                                                            'FROM planet_osm_point WHERE railway LIKE \'station\' '
                                                            'AND ST_DISTANCE(ST_Transform(way,4326), '
                                                                            'ST_SetSRID(ST_Point(%s, %s),4326)) '
                                                                '= (SELECT min(ST_DISTANCE(ST_Transform(way,4326), '
                                                                                          'ST_SetSRID(ST_Point(%s, %s),4326))) '
                                                                   'FROM planet_osm_point ' 
                                                                   'WHERE railway LIKE \'station\')), '
                                        'my_dist AS (SELECT min(ST_DISTANCE(ST_ClosestPoint(ST_Transform(way,4326),(SELECT geometry FROM my_station)), '
                                                                               '(SELECT geometry FROM my_station))) as min_dist '
                                                                                'FROM planet_osm_line ' 
                                                                                'WHERE (railway LIKE \'rail\' OR railway LIKE \'subway\')) '
                                        'SELECT osm_id, name, operator, railway, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                        'FROM planet_osm_line '
                                        'WHERE (railway LIKE \'rail\' OR railway LIKE \'subway\') '
                                        'AND ST_DISTANCE(ST_ClosestPoint(ST_Transform(way,4326), (SELECT geometry FROM my_station)), '
                                                        '(SELECT geometry FROM my_station))::numeric '
                                            '< 0.0001::numeric',
                                     [request.GET['startLon'], request.GET['startLat'], request.GET['startLon'],
                                      request.GET['startLat']])
    result_list = list(chain(start, rail))
    result = serialize('geojson', result_list, geometry_field='way', fields=('name', 'geometry', 'operator', 'railway'))
    result = json.loads(result)
    for row in result['features']:
        if row['geometry']['type'] == 'LineString':
            if row['properties']['railway'] == 'subway':
                rail_type = 'metro'
            else:
                rail_type = 'železnica'
            row['properties']['popupContent'] = '<p>Meno: '+row['properties']['name']+'<br>Operátor: '+row['properties']['operator']+'<br>Typ: '+rail_type+'</p>'
    result = json.dumps(result)
    return HttpResponse(result)


def get_routes_w_condition(request):
    #use where ST_INTERSECTS or ST_TOUCHES

    pass


# same as get_station_w_routes for now
def get_route(request):
    start = PlanetOsmPoint.objects.raw('SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                          'FROM planet_osm_point WHERE railway LIKE \'station\' '
                                          'AND ST_DISTANCE(ST_Transform(way,4326), '
                                          'ST_SetSRID(ST_Point('+request.GET['startLon']+', '+request.GET['startLat']+'),4326)) '
                                          '= (SELECT min(ST_DISTANCE(ST_Transform(way,4326), '
                                          'ST_SetSRID(ST_Point('+request.GET['startLon']+', '+request.GET['startLat']+'),4326))) '
                                          'FROM planet_osm_point WHERE railway LIKE \'station\')'
                                       )
    end = PlanetOsmPoint.objects.raw('SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                          'FROM planet_osm_point WHERE railway LIKE \'station\' '
                                          'AND ST_DISTANCE(ST_Transform(way,4326), '
                                          'ST_SetSRID(ST_Point('+request.GET['endLon']+', '+request.GET['endLat']+'),4326)) '
                                          '= (SELECT min(ST_DISTANCE(ST_Transform(way,4326), '
                                          'ST_SetSRID(ST_Point('+request.GET['endLon']+', '+request.GET['endLat']+'),4326))) '
                                          'FROM planet_osm_point WHERE railway LIKE \'station\')'
                                     )
    rail = PlanetOsmLine.objects.raw('WITH my_station AS (SELECT ST_Transform(way,4326) as geometry '
                                                            'FROM planet_osm_point WHERE railway LIKE \'station\' '
                                                            'AND ST_DISTANCE(ST_Transform(way,4326), '
                                                                            'ST_SetSRID(ST_Point('+request.GET['startLon']+', '+request.GET['startLat']+'),4326)) '
                                                                '= (SELECT min(ST_DISTANCE(ST_Transform(way,4326), '
                                                                                          'ST_SetSRID(ST_Point('+request.GET['startLon']+', '+request.GET['startLat']+'),4326))) '
                                                                   'FROM planet_osm_point ' 
                                                                   'WHERE railway LIKE \'station\')), '
                                        'my_dist AS (SELECT min(ST_DISTANCE(ST_ClosestPoint(ST_Transform(way,4326),(SELECT geometry FROM my_station)), '
                                                                               '(SELECT geometry FROM my_station))) as min_dist '
                                                                                'FROM planet_osm_line ' 
                                                                                'WHERE (railway LIKE \'rail\' OR railway LIKE \'subway\')) '
                                        'SELECT osm_id, name, operator, railway, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                        'FROM planet_osm_line '
                                        'WHERE (railway LIKE \'rail\' OR railway LIKE \'subway\') '
                                        'AND ST_DISTANCE(ST_ClosestPoint(ST_Transform(way,4326), (SELECT geometry FROM my_station)), '
                                                        '(SELECT geometry FROM my_station))::numeric '
                                            '< 0.0001::numeric'
                                     )
    result_list = list(chain(start, end, rail))
    result = serialize('geojson', result_list, geometry_field='way', fields=('name', 'geometry', 'operator', 'railway'))
    return HttpResponse(result)


def get_railway_w_station(request):
    queryres = PlanetOsmLine.objects.raw('SELECT osm_id, name, operator, railway, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                         'FROM planet_osm_line WHERE railway LIKE \'rail\' '
                                         'AND ST_DWithin((SELECT way FROM planet_osm_point WHERE railway LIKE \'station\' LIMIT 1),way,10)')
    railways = serialize('geojson', queryres, geometry_field='way', fields=('name', 'operator', 'railway', 'geometry'))
    return HttpResponse(railways)


def get_first_railway(request):
    queryres = PlanetOsmLine.objects.raw('SELECT osm_id, name, operator, railway, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                         'FROM planet_osm_line WHERE railway LIKE \'rail\' LIMIT 1')
    railways = serialize('geojson', queryres, geometry_field='way', fields=('name', 'operator', 'railway', 'geometry'))
    return HttpResponse(railways)


def get_first10_railstations(request):
    # can be done this way too
    #railstations = serialize('geojson', PlanetOsmPoint.objects.filter(railway='station')[:10], geometry_field='way', fields=('name', 'way'))
    queryres = PlanetOsmPoint.objects.raw('SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                                          'FROM planet_osm_point WHERE railway LIKE \'station\' LIMIT 10')
    railstations = serialize('geojson', queryres, geometry_field='way', fields=('name', 'geometry'))
    return HttpResponse(railstations)
