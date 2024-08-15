import requests
import pandas as pd
import streamlit as st

# Constants
API_KEY = '1e85e515955ab179f301c563b30d3233'
CSV_FILE = 'worldcities.csv'

# Load city data
df_lat_long = pd.read_csv(CSV_FILE, delimiter=',')

# Streamlit input
title = st.text_input("Type city you want to search")

if title:
    # Filter DataFrame for the selected city
    df_city = df_lat_long[df_lat_long['city'].str.lower() == title.strip().lower()]

    if not df_city.empty:
        # Extract latitude and longitude
        lat = df_city['lat'].values[0]
        lng = df_city['lng'].values[0]

        # Construct API URL
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}&units=metric'

        # Make API request
        response = requests.get(url)

        # Check API response
        if response.status_code == 200:
            data = response.json()

            # Extract weather data
            weather = data['weather'][0]
            city = data.get('name', 'Unknown City')
            temperature = data['main']['temp']
            description = weather['description']
            icon_code = weather['icon']
            icon_url = f'http://openweathermap.org/img/wn/{icon_code}.png'

            # Display results
            st.title(f'Weather in {city}')
            st.image(icon_url, width=100, caption=description)
            st.write(f"Temperature: {temperature}°C")
            st.write(f"Weather: {description.capitalize()}")

            # Create and display DataFrame
            weather_df = pd.DataFrame({
                'City': [city],
                'Temperature (°C)': [temperature],
                'Weather Description': [description.capitalize()],
                'Weather Icon': [icon_url],
            })
            st.dataframe(weather_df)
        else:
            st.error("Failed to retrieve weather data. Please check the city name or try again later.")
    else:
        st.error("City not found. Please check the city name and try again.")
# To run the app type in terminal: streamlit run WeatherForecast.py