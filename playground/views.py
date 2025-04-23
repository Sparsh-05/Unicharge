from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import charger_collection
from geopy.distance import geodesic
import pandas as pd
from django.conf import settings

API_key = settings.GOOGLE_MAPS_API_KEY

def say_hello(request):
    context = {
        "variable1" : "this is sent"
    }
    return render(request, 'home.html',context)

# Create your views here.
def about(request):
    return HttpResponse("This is about page")

def home(request):
    # Pass the Google Maps API key to the template
    context = {
        'google_maps_api_key': API_key,
        'city_lat' : 28.7041,
        'city_long' : 77.1025,
        'city' : "your city"
    }
    return render(request, 'base.html', context)

def delhi(request):
    # Pass the Google Maps API key to the template
    context = {
        'google_maps_api_key': API_key,
        'city_lat' : 28.7041,
        'city_long' : 77.1025,
        'city' : "Delhi"
    }
    return render(request, 'home.html', context)

def mumbai(request):
    # Pass the Google Maps API key to the template
    context = {
        'google_maps_api_key': API_key,
        'city_lat' : 19.0760,
        'city_long' : 72.8777,
        'city' : "Mumbai"
    }
    return render(request, 'home.html', context)

def bangalore(request):
    # Pass the Google Maps API key to the template
    context = {
        'google_maps_api_key': API_key,
        'city_lat' : 12.9716,
        'city_long' : 77.5946,
        'city' : "Bangalore"
    }
    return render(request, 'home.html', context)

def showchargers(request):
    #chargers = charger_collection.find()
    chargers = charger_collection.find({},{"_id":0,"latitude":1,"longitude":1})
    chargers_list = list(chargers)

    context = {
        'google_maps_api_key': API_key,
        'city_lat' : 28.7041,
        'city_long' : 77.1025,
        'city' : "Delhi",
        "chargers": chargers_list
    }
    return render (request,'home.html',context)

def survey(request):
    #chargers = charger_collection.find()
    

    context = {
        'google_maps_api_key': API_key,
        'city_lat' : 28.7041,
        'city_long' : 77.1025,
        'city' : "Delhi",
    }
    return render (request,'survey.html',context)




def parse_capacity(cap_str):
    try:
        return float(str(cap_str).replace("kW", "").strip())
    except:
        return 0.0

def is_vehicle_supported(vehicle_list, selected_type):
    if not isinstance(vehicle_list, (list, tuple)):
        return False
    return selected_type in vehicle_list


def filterchargers(request):
    if request.method == "GET":
        # Check if form was submitted with required fields
        
        # Default values if no filters are passed
        vehicle_type = request.GET.get("vehicleType", "Electric Car")
        connector = request.GET.get("connector", "Type2")
        power_type = request.GET.get("powerType", "AC")
        min_speed = float(request.GET.get("chargingSpeed", 0))
        max_range_km = float(request.GET.get("range", 20))  # default range = 20km

        try:
            user_lat = float(request.GET.get("userLat")) if request.GET.get("userLat") else 28.7041
            user_lng = float(request.GET.get("userLng")) if request.GET.get("userLng") else 77.1025
        except (TypeError, ValueError):
            user_lat, user_lng = 28.7041, 77.1025  # fallback to Delhi


        # Collect form values with fallback
        vehicle_type = request.GET.get("vehicleType")
        connector = request.GET.get("connector")
        power_type = request.GET.get("powerType")

        try:
            min_speed = float(request.GET.get("chargingSpeed", 0))
            max_range_km = float(request.GET.get("range", 0))
        except (TypeError, ValueError):
            return HttpResponse("Invalid input for charging speed or range.", status=400)

        # Get user location with fallback to Delhi center
        try:
            user_lat = float(request.GET.get("userLat") or 28.7041)
            user_lng = float(request.GET.get("userLng") or 77.1025)
        except (TypeError, ValueError):
            user_lat, user_lng = 28.7041, 77.1025

        user_location = (user_lat, user_lng)

        # Fetch charger data from MongoDB
        raw_data = list(charger_collection.find({}, {"_id": 0}))
        df = pd.DataFrame(raw_data)

        # Clean and preprocess
        df['capacity_kw'] = df['capacity'].apply(parse_capacity)
        df['vehicle_type_clean'] = df['vehicle_type'].apply(lambda x: eval(x) if isinstance(x, str) else x)

        filtered_df = df[
            (df['power_type'] == power_type) &
            (df['type'] == connector) &
            (df['capacity_kw'] >= min_speed) &
            (df['vehicle_type_clean'].apply(lambda v: is_vehicle_supported(v, vehicle_type)))
        ].copy()

        # Compute distance
        filtered_df['latitude'] = pd.to_numeric(filtered_df['latitude'], errors='coerce')
        filtered_df['longitude'] = pd.to_numeric(filtered_df['longitude'], errors='coerce')
        filtered_df = filtered_df.dropna(subset=['latitude', 'longitude'])

        def compute_distance(row):
            try:
                return geodesic(user_location, (float(row['latitude']), float(row['longitude']))).km
            except:
                return float('inf')

        filtered_df['distance_km'] = filtered_df.apply(compute_distance, axis=1)


        nearby_df = filtered_df[filtered_df['distance_km'] <= max_range_km]

        # Prepare context
        result = nearby_df.sort_values('distance_km').to_dict(orient="records")
        context = {
            'google_maps_api_key': API_key,
            'city_lat': user_lat,
            'city_long': user_lng,
            'city': "Your Location",
            'chargers': result
        }

        return render(request, 'markers.html', context)

    return HttpResponse("Invalid request method.", status=405)


from sklearn.cluster import KMeans
import numpy as np

def filterchargers_clustered(request):
    if request.method == "GET":
        # Defaults
        vehicle_type = request.GET.get("vehicleType", "Electric Car")
        connector = request.GET.get("connector", "Type2")
        power_type = request.GET.get("powerType", "AC")

        try:
            min_speed = float(request.GET.get("chargingSpeed", 0))
            max_range_km = float(request.GET.get("range", 20))
        except (TypeError, ValueError):
            return HttpResponse("Invalid charging speed or range", status=400)

        try:
            user_lat = float(request.GET.get("userLat") or 28.7041)
            user_lng = float(request.GET.get("userLng") or 77.1025)
        except (TypeError, ValueError):
            user_lat, user_lng = 28.7041, 77.1025

        user_location = (user_lat, user_lng)

        # Get data
        raw_data = list(charger_collection.find({}, {"_id": 0}))
        df = pd.DataFrame(raw_data)

        # Clean
        df['capacity_kw'] = df['capacity'].apply(parse_capacity)
        df['vehicle_type_clean'] = df['vehicle_type'].apply(lambda x: eval(x) if isinstance(x, str) else x)
        df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
        df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
        df = df.dropna(subset=['latitude', 'longitude'])

        # Filter
        filtered_df = df[
            (df['power_type'] == power_type) &
            (df['type'] == connector) &
            (df['capacity_kw'] >= min_speed) &
            (df['vehicle_type_clean'].apply(lambda v: is_vehicle_supported(v, vehicle_type)))
        ].copy()

        if filtered_df.empty:
            return render(request, 'markers.html', {
                'chargers': [],
                'city': "Your Location",
                'city_lat': user_lat,
                'city_long': user_lng,
                'google_maps_api_key': API_key,
                'message': "No chargers match your criteria."
            })

        # Apply KMeans clustering
        coords = filtered_df[['latitude', 'longitude']].values
        kmeans = KMeans(n_clusters=min(5, len(filtered_df)), random_state=42)
        filtered_df['cluster'] = kmeans.fit_predict(coords)

        #  Get user's nearest cluster
        user_coords = np.array([[user_lat, user_lng]])
        user_cluster = kmeans.predict(user_coords)[0]

        clustered_df = filtered_df[filtered_df['cluster'] == user_cluster]

        # Distance
        def compute_distance(row):
            try:
                return geodesic(user_location, (row['latitude'], row['longitude'])).km
            except:
                return float('inf')

        clustered_df['distance_km'] = clustered_df.apply(compute_distance, axis=1)
        nearby_df = clustered_df[clustered_df['distance_km'] <= max_range_km]

        result = nearby_df.sort_values('distance_km').to_dict(orient="records")

        context = {
            'google_maps_api_key': API_key,
            'city_lat': user_lat,
            'city_long': user_lng,
            'city': "Your Location",
            'chargers': result
        }

        return render(request, 'markers.html', context)

    return HttpResponse("Invalid request method.", status=405)
