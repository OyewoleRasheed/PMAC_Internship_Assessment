# weather_service.py
import requests
import json

class WeatherService:
    @staticmethod
    def get_weather(location):
        try:
            # 1. Geocode the location (turn city name into coordinates)
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1"
            geo_response = requests.get(geo_url)
            geo_data = geo_response.json()

            # Validate that the location exists
            if "results" not in geo_data or len(geo_data["results"]) == 0:
                return None

            lat = geo_data["results"][0]["latitude"]
            lon = geo_data["results"][0]["longitude"]

            # 2. Fetch the weather using the coordinates
            weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            weather_response = requests.get(weather_url)
            weather_data = weather_response.json().get("current_weather", {})

            # 3. BONUS (Section 2.2): Fetch Wikipedia Summary
            wiki_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{location}"
            wiki_response = requests.get(wiki_url)
            
            wiki_summary = "No additional info found."
            if wiki_response.status_code == 200:
                wiki_data = wiki_response.json()
                wiki_summary = wiki_data.get("extract", "No additional info found.")

            # Combine the weather and Wikipedia data
            combined_data = {
                "weather": weather_data,
                "location_info": wiki_summary
            }

            # Return the combined data as a JSON string to store in our database
            return json.dumps(combined_data)

        except Exception as e:
            print(f"Error fetching data: {e}")
            return None