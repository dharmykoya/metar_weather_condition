# Metar

API that returns the weather condition of a particular station passed as parameter to the API.

## Built With

- [Python 3 - version 3.6.8](https://www.python.org/)
- [DJango - version 2.2.6](https://www.djangoproject.com/)
- [Django-restframework - version 3.10.3](https://www.django-rest-framework.org/)
- [Redis - version 3.3.11](https://redis.io/)
- [django-redis - version 4.10.0 ](https://redis.io/)
- [Metar reports](https://tgftp.nws.noaa.gov/data/observations/metar/stations/)

## Features

- Can check weather condition for a station
- Saves the weather condition for 5 mins using redis
- Can reset redis cache if nocache is passed to the API

## Installation

1. Ensure you have Python3 and pip3 installed

2. Clone this repo

```bash
$ git clone https://github.com/dharmykoya/metar_weather_condition.git
```

3. Start and Activate Virtual environment make sure you have a venv installed or any other environment for python

```bash
$ python3 -m venv env
```

```bash
$ source env/bin/activate
```

4. Install Dependencies

```bash
pip3 install -r requirement.txt
```

5. Start server

```bash
python3 manage.py runserver
```

## API Routes

|                      DESCRIPTION                       | HTTP METHOD | ROUTES                           |
| :----------------------------------------------------: | ----------- | -------------------------------- |
| Get a station weather condition with redis caching set | GET         | /metar/info?scode=CWLP           |
|     Get a station weather condition from live data     | GET         | /metar/info?scode=CWLP&nocache=1 |

## Response Sample

```source-json
{
    "last observation": "2019/10/20 at 00:53 GMT",
    "station": "KHUL",
    "wind": "The wind is moving in the direction of 000 degree and a velocity of 00 knots",
    "visibility": "The visibility is 10 statute miles",
    "skyconditions": "The sky is Clear at 00 feet",
    "temperature/dew point": "The current temperature is (01)Celsius and the dew point is (-01)Celsius"
}
```

## References

- https://aerial-guide.com/article/how-to-read-a-metar-weather-report

## License

&copy; Damilola Adekoya
