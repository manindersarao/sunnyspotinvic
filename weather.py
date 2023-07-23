import os
import requests
from datetime import datetime

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
    api_key_weather = os.environ["API_KEY_WEATHER"]
    api_key_geocode = os.environ["API_KEY_GEOCODE"]
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
            if weather_data and weather_data.get('weather'):
                weather_description = weather_data['weather'][0]['description']
                if 'sun' in weather_description.lower():
                    sunny_places.append((place, weather_description))

    top_sunny_places = sorted(sunny_places, key=lambda x: x[1], reverse=True)[:num_places]
    return top_sunny_places

def generate_html_page():
    page_title = "Sunny Spot in VIC"
    sunny_places = find_sunny_places(3)
    sunny_places_list = ""
    if sunny_places:
        sunny_places_list = "<ul>" + "".join(f"<li>{place[0]}</li>" for place in sunny_places) + "</ul>"
    else:
        sunny_places_list = "<p>No sunny places found in Victoria.</p>"
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%d-%m-%Y %H:%M")
    
    template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{page_title}</title>
    </head>
     <body>
        <h1>{page_title}</h1>
        <p>Generated on: {formatted_datetime}</p>
        <h2>Top 3 Sunny Places in Victoria:</h2>
        {sunny_places_list}
    </body>
    </html>
    """
    return template

if __name__ == "__main__":
    # Generate the HTML content using the function
    html_content = generate_html_page()
    
    # Save the HTML content to a file
    with open("./page/index.html", "w", encoding="utf-8") as file:
        file.write(html_content)

    print("HTML page has been generated and saved to index.html.")