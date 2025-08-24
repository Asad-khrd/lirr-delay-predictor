import requests
from google.transit import gtfs_realtime_pb2
import time

# The official MTA GTFS-RT feed URL for the LIRR
LIRR_FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/lirr%2Fgtfs-lirr"

print("Fetching live LIRR data...")

try:
    # Fetch the data from the URL
    response = requests.get(LIRR_FEED_URL)
    response.raise_for_status() # Raise an exception for bad status codes

    # Parse the feed using the gtfs-realtime library
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    print("--- LIVE LIRR DELAY REPORT ---")
    
    found_delays = False
    # Iterate through each entity (a train update) in the feed
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            # Check for arrival or departure delay information
            for stop_time_update in entity.trip_update.stop_time_update:
                if stop_time_update.HasField('arrival') and stop_time_update.arrival.delay > 0:
                    delay_seconds = stop_time_update.arrival.delay
                    delay_minutes = round(delay_seconds / 60)
                    if delay_minutes > 0:
                        print(f"Train on route '{entity.trip_update.trip.route_id}' is delayed by {delay_minutes} minutes.")
                        found_delays = True

    if not found_delays:
        print("No significant delays reported at this moment.")

except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
except Exception as e:
    print(f"An error occurred: {e}")