import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv('vehicles_us.csv')

df['model_year'].fillna(0, inplace=True)
df.info()

df['cylinders'].fillna(0, inplace=True)
df.info()

df['odometer'].fillna(0, inplace=True)
df.info()

df['paint_color'].fillna('Not Recorded', inplace=True)
df.info()

df['is_4wd'].fillna(0, inplace=True)
df.head()

df = df.astype({'model_year': int, 'cylinders': int, 'odometer': int, 'is_4wd': int})
df.info()

st.header('Information On U.S Vehicles')
st.text('The data shown gives an insight on the characteristics of the vehicles in the u.s, and how each correspond with one another')


filtered_df = df[(df['model_year'] != 0) & (df['odometer'] != 0)]
avg_lot_days = filtered_df.groupby(['price', 'model_year', 'model', 'condition', 'odometer'])['days_listed'].mean().reset_index()
avg_lot_days.head()

min_year = df['model_year'].min()
max_year = df['model_year'].max()
min_price = df['price'].min()
max_price = df['price'].max()
   

st.header('Vehicle Data Analysis')
show_plot = st.checkbox('Show Scatter Plot of Model Year vs. Price')
if show_plot:
    fig = px.scatter(df, x='model_year', y='price', title='Model Year vs. Price')
    fig.update_xaxes(range=[min_year, max_year])
    fig.update_yaxes(range=[min_price, max_price])
    fig.update_traces(marker=dict(size=4, opacity=0.6))
    st.plotly_chart(fig)

avg_odometer = filtered_df.groupby('model_year')['odometer'].mean().reset_index()
fig = px.bar(avg_odometer, x='model_year', y='odometer', title='Average Odometer by Model Year')
st.plotly_chart(fig)

model_vs_dayslisted = px.scatter(filtered_df, x='model', y='days_listed', title='Days Listed Depending On Model Type')
model_vs_dayslisted.update_xaxes(tickangle=-45)
model_vs_dayslisted.update_layout(
    xaxis_title='Model',
    yaxis_title='Days Listed'
)
model_vs_dayslisted.update_traces(marker=dict(size=5, opacity=0.7))
model_vs_dayslisted.update_layout(width=1000, height=600)
st.plotly_chart(model_vs_dayslisted)


