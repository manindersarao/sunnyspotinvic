import requests
def get_weather_data(lat, lon, api_key):
    url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_coordinates(place, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={place}, Victoria, Australia&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            lat = data['results'][0]['geometry']['lat']
            lon = data['results'][0]['geometry']['lng']
            return lat, lon
    return None

def find_sunny_places(num_places):
    api_key_weather = 'f9c97b1dfd41faad47f6fba6739b71fe'
    api_key_geocode = 'bfd6702799fd49b5aff656001d5fb73d'

    places = [
        'Melbourne',
        'Geelong',
        'Bendigo',
        'Ballarat',
        'Shepparton',
        'Warrnambool',
        'Broadmeadows'
        # Add more places if needed
    ]

    sunny_places = []
    for place in places:
        coordinates = get_coordinates(place, api_key_geocode)
        if coordinates:
            lat, lon = coordinates
            weather_data = get_weather_data(lat, lon, api_key_weather)
            print(weather_data)
            if weather_data and weather_data.get('weather'):
                weather_description = weather_data['weather'][0]['description']
                print(f"weather description {weather_description}")
                if 'sun' in weather_description.lower():
                    sunny_places.append((place, weather_description))

    top_sunny_places = sorted(sunny_places, key=lambda x: x[1], reverse=True)[:num_places]
    return top_sunny_places


if __name__ == "__main__":
    num_places = 3
    top_sunny_places = find_sunny_places(num_places)
    print(f"Top {num_places} sunny places in Victoria, Australia:")
    for i, place in enumerate(top_sunny_places, start=1):
        print(f"{i}. {place[0]}")
