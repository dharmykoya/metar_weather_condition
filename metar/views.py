from django.shortcuts import render
import requests
from django.http import JsonResponse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django_redis import get_redis_connection
from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


def serialize_temperature(temperature_dewpoint):
    temp = temperature_dewpoint.split('/')
    temperature = ''
    dewpoint = ''
    if 'M' in temp[0]:
        temperature = temp[0].replace('M', '-')
    else:
        temperature = temp[0]

    if 'M' in temp[1]:
        dewpoint = temp[1].replace('M', '-')

    else:
        dewpoint = temp[1]

    result = f'The current temperature is ({temperature})Celsius and the dew point is ({dewpoint})Celsius'

    return result


def serialize_wind(wind_param):
    knot = ''
    result = ''
    direction = wind_param[:3]
    if 'G' in wind_param[3:]:
        gust = wind_param[3:6].replace('G', '')
        knot = wind_param[6:].replace('KT', '')
        result = f'The wind is moving in the direction of {direction} degree at {gust} gusting and a velocity of {knot} knots'
    else:
        knot = wind_param[3:].replace('KT', '')
        result = f'The wind is moving in the direction of {direction} degree and a velocity of {knot} knots'

    return result


def serialize_statute_miles(statute_param):
    statute_miles = statute_param.replace('SM', '')
    result = f'The visibility is {statute_miles} statute miles'
    return result


def serialize_sky_condition(sky_param):
    if 'CLR' in sky_param:
        feet = sky_param.replace('CLR', '')
        result = f'The sky is Clear at {feet}00 feet'
        return result
    elif 'SKC' in sky_param:
        feet = sky_param.replace('SKC', '')
        result = f'The sky is Clear at {feet}00 feet'
        return result
    elif 'OVC' in sky_param:
        feet = sky_param.replace('OVC', '')
        result = f'The sky is Overcast at {feet}00 feet'
        return result
    elif 'FEW' in sky_param:
        feet = sky_param.replace('FEW', '')
        result = f'The sky is Few at {feet}00 feet'
        return result
    elif 'SCT' in sky_param:
        feet = sky_param.replace('SCT', '')
        result = f'The sky is Scattered at {feet}00 feet'
        return result
    elif 'BKN' in sky_param:
        feet = sky_param.replace('OVC', '')
        result = f'The sky is Broken at {feet}00 feet'
        return result


def metar(request):

    # getting the station code from the request and if it's empty by default it takes KHUL station
    station_code = request.GET.get('scode', 'KHUL')
    nocache = request.GET.get('nocache', '')

    # flushing the cache if nocache is 1
    if nocache == '1':
        get_redis_connection("default").flushall()

    if station_code in cache:
        data = cache.get(station_code)
        return JsonResponse(data, safe=False)
    else:
        url = f'http://tgftp.nws.noaa.gov/data/observations/metar/stations/{station_code}.TXT'

        data = {}

        response = requests.get(url)

        if response.status_code == 200:
            result = response.text.split('\n')
            date_time = result[0].split(' ')
            features = result[1].split(' ')
            date = date_time[0]
            time = date_time[1]

            data['last observation'] = f'{date} at {time} GMT'

            for feature in features:
                if station_code == feature:
                    data['station'] = feature
                if 'KT' in feature:
                    data['wind'] = serialize_wind(feature)
                if 'SM' in feature:
                    data['visibility'] = serialize_statute_miles(feature)
                if '/' in feature and len(feature) < 8:
                    data['temperature/dew point'] = serialize_temperature(
                        feature)
                if 'CLR' in feature:
                    data['skyconditions'] = serialize_sky_condition(feature)
                if 'OVC' in feature:
                    data['skyconditions'] = serialize_sky_condition(feature)
                if 'FEW'in feature:
                    data['skyconditions'] = serialize_sky_condition(feature)
                if 'SKC'in feature:
                    data['skyconditions'] = serialize_sky_condition(feature)
                if 'BKN'in feature:
                    data['skyconditions'] = serialize_sky_condition(feature)
                if 'SCT'in feature:
                    data['skyconditions'] = serialize_sky_condition(feature)

            # setting the cache for staion checked
            cache.set(station_code, data, timeout=CACHE_TTL)
        else:
            data['error'] = 'request not found on the server'

        return JsonResponse(data)


def ping(request):
    return JsonResponse({'data': 'pong'})
