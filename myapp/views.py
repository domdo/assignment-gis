from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers import serialize
from django.db import connection
from itertools import chain
import json
from .models import PlanetOsmPoint
from .models import PlanetOsmLine
from .models import PlanetOsmPolygon
from .result_processing import *

def index(request):
    return render(request, 'index.html')


def get_nearest_stations(request):
    """queryres1 = PlanetOsmPoint.objects.raw('SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
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
    railways = serialize('geojson', result_list, geometry_field='way', fields=('name', 'geometry'))"""
    with connection.cursor() as cursor:
        cursor.execute('WITH my_res AS (SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                       '                FROM planet_osm_point '
                       '				 WHERE railway LIKE \'station\' '
                       '				 AND ST_DWithin(ST_Transform(way,4326), '
                       '							    ST_SetSRID(ST_Point(%s, %s),4326), '
                       '							    56::float*%s::float/6371000::float) '
                       '				 UNION SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                       '                FROM planet_osm_polygon '
                       '				 WHERE railway LIKE \'station\' '
                       '				 AND ST_DWithin(ST_Transform(way,4326), '
                       '							    ST_SetSRID(ST_Point(%s, %s),4326), '
                       '							    56::float*%s::float/6371000::float)) '
                       'SELECT json_build_object( '
                       '    \'type\',       \'Feature\', '
                       '    \'geometry\',   geometry::json, '
                       '    \'properties\', json_build_object( '
                       '        \'name\', name '
                       '     ) '
                       ') '
                       'FROM my_res',
                       [request.GET['lon'], request.GET['lat'], request.GET['dist'],
                        request.GET['lon'], request.GET['lat'], request.GET['dist']])
        stations = cursor.fetchall()
    result = process_no_model_no_length_result(stations)
    return HttpResponse(result)


def get_station_w_routes(request):
    with connection.cursor() as cursor:
        cursor.execute('WITH my_res AS (SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                       '                FROM planet_osm_point '
                       '				 WHERE railway LIKE \'station\' '
                       '				 AND ST_DISTANCE(ST_Transform(way,4326), '
                       '								 ST_SetSRID(ST_Point(%s, %s),4326)) '
                       '					 = (SELECT min(ST_DISTANCE(ST_Transform(way,4326), '
                       '											    ST_SetSRID(ST_Point(%s, %s),4326))) '
                       '					    FROM planet_osm_point WHERE railway LIKE \'station\')) '
                       'SELECT json_build_object( '
                       '    \'type\',       \'Feature\', '
                       '    \'geometry\',   geometry::json, '
                       '    \'properties\', json_build_object( '
                       '        \'name\', name '
                       '     ) '
                       ' ) '
                       'FROM my_res',
                       [request.GET['startLon'], request.GET['startLat'],
                        request.GET['startLon'], request.GET['startLat']])
        station = cursor.fetchall()
    with connection.cursor() as cursor:
        cursor.execute('WITH my_station AS (SELECT ST_Transform(way,4326) as geometry '
                       '					 FROM planet_osm_point WHERE railway LIKE \'station\' '
                       '					 AND ST_DISTANCE(ST_Transform(way,4326), '
                       '									 ST_SetSRID(ST_Point(%s, %s),4326)) '
                       '			             = (SELECT min(ST_DISTANCE(ST_Transform(way,4326), '
                       '												    ST_SetSRID(ST_Point(%s, %s),4326))) '
                       '						    FROM planet_osm_point '
                       '						    WHERE railway LIKE \'station\')), '
                       'my_dist AS (SELECT min(ST_DISTANCE(ST_ClosestPoint(ST_Transform(way,4326),(SELECT geometry FROM my_station)), '
                       '								    (SELECT geometry FROM my_station))) as min_dist '
                       '			 FROM planet_osm_line '
                       '			 WHERE (railway LIKE \'rail\' OR railway LIKE \'subway\')), '
                       'my_res AS (SELECT osm_id, name, operator, railway, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
                       '		    FROM planet_osm_line '
                       '		    WHERE (railway LIKE \'rail\' OR railway LIKE \'subway\') '
                       '		    AND ST_DISTANCE(ST_ClosestPoint(ST_Transform(way,4326), (SELECT geometry FROM my_station)), '
                       '						    (SELECT geometry FROM my_station))::numeric '
                       '				< 0.0001::numeric) '
                       'SELECT json_build_object( '
                       '    \'type\',       \'Feature\', '
                       '    \'geometry\',   geometry::json, '
                       '    \'properties\', json_build_object( '
                       '        \'name\', name, '
                       '		 \'operator\', operator, '
                       '		 \'railway\', railway '
                       '     ) '
                       ') '
                       'FROM my_res',
                       [request.GET['startLon'], request.GET['startLat'],
                        request.GET['startLon'], request.GET['startLat']])
        rails = cursor.fetchall()
    # old code (leaving just for reference)
    """start = PlanetOsmPoint.objects.raw('SELECT osm_id, name, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry '
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
            elif row['properties']['railway'] == 'rail':
                rail_type = 'železnica'
            else:
                rail_type = 'none'
            row['properties']['popupContent'] = '<p>Meno: '+(row['properties']['name'] or 'none')+\
                                                '<br>Operátor: '+(row['properties']['operator'] or 'none')+\
                                                '<br>Typ: '+(rail_type or 'none')+'</p>'
    result = json.dumps(result)"""

    result = process_no_model_no_length_result(rails)
    result = json.loads(result)
    result = append_no_model_no_length_result(result, station)
    return HttpResponse(result)


def get_routes_w_condition(request):
    bridge = None
    tunnel = None
    if request.GET['bridge'] == 'true':
        bridge = 'yes'
    if request.GET['tunnel'] == 'true':
        tunnel = 'yes'
    if request.GET['water'] == 'true':
        with connection.cursor() as cursor:
            cursor.execute('WITH waters AS (SELECT way '
                           '				 FROM planet_osm_polygon '
                           '				 WHERE ST_DWithin(ST_SetSRID(ST_Point(%s, %s),4326), '
                           '								  ST_Transform(way,4326), '
                           '								  56::float*%s::float/6371000::float) '
                           '				 AND (water IS NOT NULL OR waterway IS NOT NULL)), '
                           'my_res AS (SELECT l.osm_id, l.name, l.operator, l.railway, '
                           '		    ST_AsGeoJSON(ST_Transform(l.way,4326)) AS geometry, '
                           '		    ST_Length(ST_Transform(l.way,4326)::geography) AS my_length '
                           '		    FROM planet_osm_line AS l '
                           '		    CROSS JOIN waters AS w '
                           '           WHERE (l.railway LIKE \'rail\' OR l.railway LIKE \'subway\') '
                           '		    AND ST_DWithin(ST_SetSRID(ST_Point(%s, %s),4326), '
                           '						   ST_Transform(l.way,4326), '
                           '						   56::float*%s::float/6371000::float) '
                           '		    AND l.bridge IS NOT DISTINCT FROM %s '
                           '		    AND l.tunnel IS NOT DISTINCT FROM %s '
                           '		    AND (ST_Intersects(ST_Transform(l.way,4326), '
                           '							   ST_Transform(w.way,4326)) = \'t\' '
                           '				 OR ST_Touches(ST_Transform(l.way,4326), '
                           '							   ST_Transform(w.way,4326)) = \'t\')) '
                           'SELECT json_build_object( '
                           '    \'type\',       \'Feature\', '
                           '    \'geometry\',   geometry::json, '
                           '    \'properties\', json_build_object( '
                           '        \'name\', name, '
                           '        \'operator\', operator, '
                           '		 \'railway\', railway, '
                           '		 \'my_length\', my_length '
                           '     )'
                           ') '
                           'FROM my_res',
                           [request.GET['lon'], request.GET['lat'], request.GET['dist'],
                            request.GET['lon'], request.GET['lat'], request.GET['dist'],
                            bridge, tunnel])
            result = cursor.fetchall()
    else:
        with connection.cursor() as cursor:
            cursor.execute('WITH my_res AS (SELECT osm_id, name, operator, railway, ST_AsGeoJSON(ST_Transform(way,4326)) AS geometry, '
                           'ST_Length(ST_Transform(way,4326)::geography) AS my_length '
                           'FROM planet_osm_line '
                           'WHERE (railway LIKE \'rail\' OR railway LIKE \'subway\') '
                           'AND ST_DWithin(ST_SetSRID(ST_Point(%s, %s),4326), '
                           '   		        ST_Transform(way,4326), '
                           '               56::float*%s::float/6371000::float) '
                           'AND bridge IS NOT DISTINCT FROM %s '
                           'AND tunnel IS NOT DISTINCT FROM %s) '
                           'SELECT json_build_object( '
                           '    \'type\',       \'Feature\', '
                           '    \'geometry\',   geometry::json, '
                           '    \'properties\', json_build_object( '
                           '        \'name\', name, '
                           '        \'operator\', operator, '
                           '		 \'railway\', railway,'
                           '		 \'my_length\', my_length)'
                           ') '
                           'FROM my_res',
                           [request.GET['lon'], request.GET['lat'], request.GET['dist'], bridge, tunnel])
            result = cursor.fetchall()
    result = process_no_model_result(result)
    return HttpResponse(result)


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
