import argparse
import requests
import json

API_KEY = "0a2fb6badec24771909113419253006"
BASE_URL = "http://api.weatherapi.com/v1/current.json"

def get_weather_data(city):
    """Fetch weather data from WeatherAPI.com"""
    params = {
        'key': API_KEY,
        'q': city,
        'aqi': 'no'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
def display_weather_data(data, filter_param=None):
    if not data:
        print("No data")
        return
    if "error" in data:
        print(f"Error: {data['error'].get('message', 'Unknown error')}")
        return

    weather_info = {
        'City': data['location']['name'],
        'Country': data['location']['country'],
        'Temperature': f"{data['current']['temp_c']} °C",
        'Feels like': f"{data['current']['feelslike_c']} °C",
    }
    if filter_param:
        if filter_param in weather_info:
            print(f"\n{filter_param}: {weather_info[filter_param]}")
        else:
            print(f"\nParameter '{filter_param}' not found. Available parameters:")
            list_available_parameters()
    else:
        print("\nFull weather information:")
        for key, value in weather_info.items():
            print(f"{key}: {value}")
def list_available_parameters():
    print("\nAvailable parameters for filtering:")
    print("- Temperature")
    print("- Feels like")
def main():
    parser = argparse.ArgumentParser(description='Weather forecast program (WeatherAPI.com)')
    parser.add_argument('city', type=str, help='City name')
    parser.add_argument('--filter', type=str, help='Filter parameter')
    parser.add_argument('--list', action='store_true', help='Show available parameters')
    args = parser.parse_args()
    if args.list:
        list_available_parameters()
        return
    weather_data = get_weather_data(args.city)
    if weather_data:
        display_weather_data(weather_data, args.filter)
if __name__ == "__main__":
    main()
