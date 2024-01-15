# services/services.py
# https://v6.exchangerate-api.com/v6/YOUR-API-KEY/codes



import requests

class CurrencyConverter:
    def __init__(self):
        self.api_key = 'ce5c7b1db80873b2748effa9'# your actual API key for https://www.exchangerate-api.com/
        self.base_url = 'https://v6.exchangerate-api.com/v6/'

    def get_currency_codes(self):
        url = f'https://v6.exchangerate-api.com/v6/{self.api_key}/codes'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return dict(data['supported_codes'])
        else:
            # Handle the error case, e.g., log an error or raise an exception
            return []


    def get_exchange_rate(self, from_currency, to_currency):
        url = f'{self.base_url}{self.api_key}/latest/{from_currency}'
        params = {'api_key': self.api_key, 'base': from_currency}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data['conversion_rates'].get(to_currency)
        else:
            return None

    def convert_currency(self, amount, from_currency, to_currency):
        exchange_rate = self.get_exchange_rate(from_currency, to_currency)
        if exchange_rate is not None:
            converted_amount = float(amount) * float(exchange_rate)
            return converted_amount
        return None


class SafetyService:
    def __init__(self):
        self.base_url = 'https://www.travel-advisory.info/api'

    def get_safety_information(self, country_code=None):
        if country_code:
            url = f'{self.base_url}?countrycode={country_code}/'
        else:
            url = f'{self.base_url}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None

class Countrycode_Service:
    def __init__(self):
        self.base_url = 'https://www.travel-advisory.info/api'

    def iso_countrycode(self):
        url = f'{self.base_url}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            codes=dict(map(lambda v: (v['name'],v['iso_alpha2']),data['data'].values()))
            return codes
        else:
            return None



# def get_coordinates(place_name):
#     api_key = '4f01ebd046984b8da794ce2ecd74a2ba'
#     base_url = f'https://api.opencagedata.com/geocode/v1/json?q={place_name}'
#     params = {
#         'key': api_key,
#     }
#
#     response = requests.get(base_url, params=params)
#     data = response.json()
#     print(data)
#     if response.status_code == 200:
#         return data
#     else:
#         return None


def get_coordinates(place_name):
    api_key = 'pk.f89febc4b2a6558c5b59086b284b2605'# your actual API key for https://locationiq.com/
    base_url = f'https://us1.locationiq.com/v1/search?q={place_name}&format=json'
    # https://us1.locationiq.com/v1/search?key=<Your_API_Access_Token>&q=kakkanad&format=json
    # api_key = '4f01ebd046984b8da794ce2ecd74a2ba'
    # base_url = f'https://api.opencagedata.com/geocode/v1/json?q={place_name}'
    params = {

        'key': api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    print(data)
    location = data[0]
    print(location)
    # if data['status'] == 'OK':
    if response.status_code == 200:
        #location = data['results'][0]['geometry']
        location=data[-1]
        print(location)
        return location['lat'], location['lon']
    else:
        return None

def get_emergency_services(lat, lng):
    api_key = 'pk.f89febc4b2a6558c5b59086b284b2605' # your actual API key for https://locationiq.com/
    # base_url = 'https://us1.locationiq.com/v1/nearby'
    #
    # params = {
    #     'location': f'{lat},{lng}',
    #     'radius': 5000,  # You can adjust the radius as needed
    #     'type': ['hospital','police station'],  # Adjust the type based on the emergency services you want
    #     'key': api_key,
    # }

    base_url = "https://us1.locationiq.com/v1/nearby"
    # base_url=f"https://us1.locationiq.com/v1/nearby?key={api_key}&lat={lat}&lon={lng}&tag={['hospital','police station']}&radius={500}&format=json"
    params = {
        'key': api_key,
        'lat': lat,
        'lon': lng,
        'tag': 'amenity:police,hospital',
        'radius': 3000,
        'format': 'json'
    }

    response = requests.get(base_url,params=params)
    data = response.json()
    print('ABCD')
    print(data)
    print('ABCD')
    # if data['status'] == 'OK':
    if response.status_code == 200:
        return data
    else:
        return None