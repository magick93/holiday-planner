# Import necessary libraries
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import typing
import requests
import json
from functools import cache
from .supabase import SupabaseClientSingleton

supabase = SupabaseClientSingleton.get_instance()

class GeoCodingAPIView(APIView):

    @cache
    def get(self, city_name:str, format=None):
        # Get the city name from the request parameters
        # city_name = args.get('name')

        # You could also get other parameters from the request, e.g.,
        # count = request.query_params.get('count', 10)  # Default to 10 if not provided
        # language = request.query_params.get('language', 'en')  # Default to 'en' if not provided

        # Construct the URL
        url = f'https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=10&language=en&format=json'

        # Make the request to the external API
        response = requests.get(url)

        # Check for a successful response
        if response.status_code == 200:
            # Parse the JSON response
            geo_data = response.json()

            results_array = geo_data.get('results', [])

            places = str(json.dumps(results_array))

            print(places)


            try:
                # upsert_places = supabase.rpc('upsert_places', {"data":places}).execute()
                upsert_places = supabase.rpc('upsert_places', {"data":json.loads(places)}).execute()
            except Exception as e:
                print(e)
                print("Error with upsert_places")
            


            return Response(geo_data, status=status.HTTP_200_OK)
        else:
            # Handle the error (you could also log the error, retry the request, etc.)
            return Response({'error': 'Unable to retrieve geocoding data'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

