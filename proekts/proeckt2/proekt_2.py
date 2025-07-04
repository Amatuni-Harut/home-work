import argparse
import requests
import json
API_KEY = '0a2fb6badec24771909113419253006'  
OPTIONS = {
    'temperature': 'Temperature (°C)',
    'humidity': 'Humidity (%)',
    'pressure': 'Pressure (mBar)',
    'wind': 'Wind speed (km/h)',
    'condition': 'Weather description'
}
def weather_info_input(city):
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        print("Failed to get weather data.")
        return None
def weather_info(data, option=None):
    try:
        current = data['current']
        location = data['location']
        print(f"Weather in {location['name']}, {location['country']}")
        if option:
            if option == 'temperature':
                print("temperature --", current['temp_c'], "°C")
            elif option == 'humidity':
                print("humidity --", current['humidity'], "%")
            elif option == 'pressure':
                print("pressure --", current['pressure_mb'], "mBar")
            elif option == 'wind':
                print("wind speed --", current['wind_kph'], "km/h")
            elif option == 'condition':
                print("condition --", current['condition']['text'])
            else:
                print("Use --options to see available options.")
        else:
            print(json.dumps(current, indent=4))
    except:
        print("Error while showing weather.")
def option_info():
    print("Available options:")
    for key, desc in OPTIONS.items():
        print(f"  {key}: {desc}")
def main():
    parser = argparse.ArgumentParser(description="This is a weather program")
    parser.add_argument('city', help="City name")
    parser.add_argument('--option', help="Specific weather info to show")
    parser.add_argument('--options', action='store_true', help="Show available options")
    args = parser.parse_args()
    if args.options:
        option_info()
        return
    data = weather_info_input(args.city)
    if data:
        weather_info(data, args.option)
if __name__ == '__main__':
    main()













