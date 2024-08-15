import requests
import pandas as pd
import streamlit as st
import streamlit
# Api call https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}

lat = '50.0755'
lon = '14.4378'
ApiKey = '1e85e515955ab179f301c563b30d3233'
# 81cc154b084576286deecdfd6a027687
# 1e85e515955ab179f301c563b30d3233

url = f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={ApiKey}&units=metric'
#url = f'https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={ApiKey}&units=metric'
print(url)


response = requests.get(url)
print("Status Code:", response.status_code)
print("Response Content:", response.text)


data = response.json()
print(data)

df = pd.json_normalize(data)
weather = data['weather'][0]
city = data.get('name', 'Unknown City')
temperature = data['main']['temp']
description = weather['description']
icon_code = weather['icon']

icon_url = f'http://openweathermap.org/img/wn/{icon_code}.png'

print(weather)

st.title(f'Weather in {city}, have nice day')

# Display weather icon
st.image(icon_url, width=100, caption=description)

# Display weather details
st.write(f"Temperature: {temperature}°C")
st.write(f"Weather: {description.capitalize()}")

# Display full data frame
st.dataframe(df)


# To run the app type in terminal: streamlit run WeatherForecast.py