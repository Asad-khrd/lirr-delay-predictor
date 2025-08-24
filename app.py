import streamlit as st
import pandas as pd
import joblib
import requests
from google.transit import gtfs_realtime_pb2
import time
import holidays
from datetime import datetime

# --- App Configuration ---
st.set_page_config(
    page_title="Live LIRR Predictive Dashboard",
    page_icon="🧠",
    layout="wide"
)

# --- Load Trained Model and Columns ---
try:
    model = joblib.load('lirr_delay_model.joblib')
    model_columns = joblib.load('model_columns.joblib')
except FileNotFoundError:
    st.error("Model files not found! Please ensure 'lirr_delay_model.joblib' and 'model_columns.joblib' are in the same folder.")
    st.stop()

# --- Mappings and Constants ---
LIRR_FEED_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/lirr%2Fgtfs-lirr"
BRANCH_MAP = {
    '1': 'Babylon', '2': 'Ronkonkoma', '3': 'Port Jefferson', '4': 'Hempstead',
    '5': 'West Hempstead', '6': 'Oyster Bay', '7': 'Montauk', '8': 'Port Washington',
    '9': 'Long Beach', '10': 'Far Rockaway', '12': 'Greenport'
}
STOP_MAP = {
    '101': 'Penn Station', '133': 'Atlantic Terminal', '125': 'Jamaica', '121': 'Woodside',
    '7': 'Amityville', '8': 'Babylon', '9': 'Baldwin', '13': 'Farmingdale',
    '17': 'Freeport', '21': 'Lindenhurst', '23': 'Lynbrook', '25': 'Massapequa',
    '26': 'Massapequa Park', '29': 'Merrick', '33': 'Rockville Centre', '35': 'Seaford',
    '37': 'Wantagh', '41': 'Huntington', '43': 'Port Jefferson', '45': 'Smithtown',
    '47': 'Stony Brook', '53': 'Ronkonkoma', '59': 'Oyster Bay', '61': 'Syosset',
    '63': 'West Hempstead', '65': 'Garden City', '67': 'Hempstead', '79': 'Long Beach',
    '81': 'Island Park', '93': 'Port Washington', '95': 'Plandome', '97': 'Manhasset',
    '99': 'Great Neck', '103': 'Little Neck', '105': 'Bayside', '107': 'Flushing-Main St',
    '113': 'Far Rockaway', '119': 'Hicksville', '129': 'Mineola', '135': 'New Hyde Park',
    '137': 'Merillon Avenue', '701': 'Grand Central Madison', '30': 'Montauk', '15': 'East Hampton',
    '19': 'Hampton Bays', '31': 'Patchogue', '32': 'Sayville', '36': 'Speonk', '38': 'Westhampton'
}
TOP_10_STATIONS = ['Jamaica', 'Penn Station', 'Atlantic Terminal', 'Hicksville', 'Babylon', 'Ronkonkoma', 'Huntington', 'Mineola', 'Freeport', 'Lynbrook']
US_HOLIDAYS = holidays.US()

# --- Feature Engineering Function ---
def create_features_for_prediction(live_data_df):
    df = live_data_df.copy()
    
    df['is_hub_station'] = df['Depart Station'].apply(lambda x: 1 if x in TOP_10_STATIONS else 0)
    df['is_holiday'] = df['Depart DateTime'].dt.date.apply(lambda x: 1 if x in US_HOLIDAYS else 0)
    
    def get_rush_hour(hour):
        if 6 <= hour <= 9: return 'AM_Rush'
        elif 16 <= hour <= 19: return 'PM_Rush'
        else: return 'Off_Peak'
    df['rush_hour'] = df['Depart DateTime'].dt.hour.apply(get_rush_hour)
    
    df['day_of_week'] = df['Depart DateTime'].dt.dayofweek
    df['hour'] = df['Depart DateTime'].dt.hour
    
    features_df = df[['Branch', 'rush_hour', 'is_holiday', 'is_hub_station', 'day_of_week', 'hour']]
    
    return features_df

# --- Live Data Fetching & Prediction ---
def get_live_predictions():
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(LIRR_FEED_URL)
        response.raise_for_status()
        feed.ParseFromString(response.content)
        
        live_incidents = []
        processed_trips = set()

        for entity in feed.entity:
            if entity.HasField('trip_update') and entity.trip_update.trip.trip_id not in processed_trips:
                processed_trips.add(entity.trip_update.trip.trip_id)
                
                route_id = entity.trip_update.trip.route_id
                
                if entity.trip_update.stop_time_update:
                    first_stop = entity.trip_update.stop_time_update[0]
                    stop_id = first_stop.stop_id
                    
                    timestamp = first_stop.departure.time if first_stop.HasField('departure') else first_stop.arrival.time
                    if timestamp > 0:
                        depart_datetime = datetime.fromtimestamp(timestamp)
                        
                        live_incidents.append({
                            'Branch': BRANCH_MAP.get(route_id, 'Unknown'),
                            'Depart Station': STOP_MAP.get(stop_id, 'Unknown'),
                            'Depart DateTime': depart_datetime
                        })

        if not live_incidents:
            return "No active trains found in the live feed."

        live_df = pd.DataFrame(live_incidents)
        features_to_predict = create_features_for_prediction(live_df)
        X_live_encoded = pd.get_dummies(features_to_predict)
        X_live_aligned = X_live_encoded.reindex(columns=model_columns, fill_value=0)
        probabilities = model.predict_proba(X_live_aligned)

        results = []
        for i, incident in enumerate(live_incidents):
            prob_series = pd.Series(probabilities[i], index=model.classes_).sort_values(ascending=False).head(3)
            results.append({
                'info': incident,
                'predictions': prob_series
            })
        return results

    except Exception as e:
        return f"An error occurred: {e}"

# --- Streamlit App Layout ---
st.title("🧠 Live LIRR Delay Cause Predictor")
st.write(f"**Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}**")

if st.button('🔄 Get Live Predictions'):
    with st.spinner("Fetching live data and running predictions..."):
        predictions = get_live_predictions()
        
        if isinstance(predictions, str):
            st.warning(predictions)
        else:
            st.success(f"Found {len(predictions)} active trains. Showing top predictions:")
            for result in predictions[:10]:
                info = result['info']
                preds = result['predictions']
                
                header = f"**{info['Branch']} Train** departing from **{info['Depart Station']}** at {info['Depart DateTime'].strftime('%H:%M')}"
                with st.expander(header):
                    st.write("Top 3 Likely Delay Causes:")
                    
                    # --- THIS IS THE CORRECTED SECTION ---
                    results_df = preds.reset_index().rename(columns={'index': 'Category', 0: 'Probability'})
                    
                    # 1. Convert the probability to a percentage value
                    results_df['Probability'] = results_df['Probability'] * 100
                    
                    # 2. Display the DataFrame, telling the progress bar the max value is now 100
                    st.dataframe(results_df,
                                 column_config={
                                     "Probability": st.column_config.ProgressColumn(
                                         "Likelihood (%)",
                                         format="%.1f%%",
                                         min_value=0,
                                         max_value=100, # Set max to 100
                                     ),
                                 },
                                 use_container_width=True, 
                                 hide_index=True)