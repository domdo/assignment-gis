import json


def process_no_model_result(result):
    final = {'type': 'FeatureCollection', 'features':  []}
    for row in result:
        if row[0]['geometry']['type'] == 'LineString':
            if row[0]['properties']['railway'] == 'subway':
                rail_type = 'metro'
            elif row[0]['properties']['railway'] == 'rail':
                rail_type = 'železnica'
            length = str(round(row[0]['properties']['my_length'], 2))
            row[0]['properties']['popupContent'] = '<p>Meno: ' + (row[0]['properties']['name'] or 'none') + \
                                                '<br>Operátor: ' + (row[0]['properties']['operator'] or 'none') + \
                                                '<br>Typ: ' + (rail_type or 'none') + \
                                                '<br>Dĺžka: ' + (length or 'none') + ' m' + '</p>'
        final['features'].append(row[0])
    return json.dumps(final)


def process_no_model_no_length_result(result):
    final = {'type': 'FeatureCollection', 'features':  []}
    for row in result:
        if row[0]['geometry']['type'] == 'LineString':
            if row[0]['properties']['railway'] == 'subway':
                rail_type = 'metro'
            elif row[0]['properties']['railway'] == 'rail':
                rail_type = 'železnica'
            row[0]['properties']['popupContent'] = '<p>Meno: ' + (row[0]['properties']['name'] or 'none') + \
                                                '<br>Operátor: ' + (row[0]['properties']['operator'] or 'none') + \
                                                '<br>Typ: ' + (rail_type or 'none') + '</p>'
        final['features'].append(row[0])
    return json.dumps(final)


def append_no_model_no_length_result(final, result):
    for row in result:
        if row[0]['geometry']['type'] == 'LineString':
            if row[0]['properties']['railway'] == 'subway':
                rail_type = 'metro'
            elif row[0]['properties']['railway'] == 'rail':
                rail_type = 'železnica'
            row[0]['properties']['popupContent'] = '<p>Meno: ' + (row[0]['properties']['name'] or 'none') + \
                                                '<br>Operátor: ' + (row[0]['properties']['operator'] or 'none') + \
                                                '<br>Typ: ' + (rail_type or 'none') + '</p>'
        final['features'].append(row[0])
    return json.dumps(final)