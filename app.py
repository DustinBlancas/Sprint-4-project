## Data Analysis On U.S Vehicles

#The data will demonstrate the differnces of the vehicles in the u.s. 
# Examing the graphs will show what makes them popular or unpopular. 
# Seeing details of the vehicles will help us understand why some vehicles are more desireable than others.

import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')

#Checking for duplicates and the df is clear of duplicates
df.duplicated().unique()

#Replace NaN values with descriptive values
df['model_year'] = df['model_year'].fillna(df.groupby('model')['model_year'].transform('median'))
df.info()

df['cylinders'] = df['cylinders'].fillna(df.groupby('model')['cylinders'].transform('median'))
df.info()

df['odometer'] = df['odometer'].fillna(df.groupby('model')['odometer'].transform('median'))
df.info()

df['paint_color'].fillna('Unknown', inplace=True)
df.info()

df['is_4wd'].fillna(0, inplace=True)
df.head()

#removing extra NaN values remaining
df.fillna(0, inplace=True)
df.info()

#Changing the type of columns
df = df.astype({'model_year': int, 'cylinders': int, 'odometer': int, 'is_4wd': int})
df.info()

#Header and description of app
st.header('Information On U.S Vehicles')
st.text('The data shown gives an insight on the characteristics of the vehicles in the u.s, and how each correspond with one another')

#Filtering data
filtered_df = df[(df['model_year'] != 0) & (df['odometer'] != 0)]
avg_lot_days = filtered_df.groupby(['price', 'model_year', 'model', 'condition', 'odometer'])['days_listed'].mean().reset_index()
avg_lot_days.head()

#Finding the min and max of model year and price
min_year = df['model_year'].min()
max_year = df['model_year'].max()
min_price = df['price'].min()
max_price = df['price'].max()
   

st.header('Vehicle Price Data Analysis')
#Define an arbitrary price threshold
price_threshold = 50000
#Create a checkbox
filter_prices = st.checkbox('Exclude very expensive vehicles')
#Filter data based on the checkbox
if filter_prices:
    filtered_df = df[df['price'] <= price_threshold]
else:
    filtered_df = df
#Create the plot
fig = px.scatter(filtered_df, x='model_year', y='price', title='Model Year vs. Price')
#Show the plot
st.plotly_chart(fig)

#Group data
avg_odometer = filtered_df.groupby('model_year')['odometer'].mean().reset_index()
#Create plot
fig = px.bar(avg_odometer, x='model_year', y='odometer', title='Average Odometer by Model Year')
#Show plot
st.plotly_chart(fig)

#Creating plot
model_vs_dayslisted = px.scatter(filtered_df, x='model', y='days_listed', title='Days Listed Depending On Model Type')
#Update layout
model_vs_dayslisted.update_xaxes(tickangle=-45)
model_vs_dayslisted.update_layout(
    xaxis_title='Model',
    yaxis_title='Days Listed'
)
model_vs_dayslisted.update_traces(marker=dict(size=5, opacity=0.7))
model_vs_dayslisted.update_layout(width=1000, height=600)
#plot Chart
st.plotly_chart(model_vs_dayslisted)

# The graphs give an insight on what the most epensive and cheapest vehicles are. 
# Also how long they stay on the lot for, showing the popularity of the vehicle. 
# We see key details that can affect this, such as the color of the vehicle,
# if it is four wheel drive, the odometer, the release year and the type of vehicle.

