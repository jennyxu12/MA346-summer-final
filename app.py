import pandas as pd
import streamlit as st
import altair as alt
import numpy as np

st.title('US Police Shootings')
st.write('link for repo: https://github.com/jennyxu12/MA346-summer-final')
st.sidebar.header('Welcome to My Dashboard')

dfShooting = pd.read_csv('shootings.csv')

st.subheader('Topic 1. Number of Shooting for Different States in Descending Order')
dfShooting = dfShooting[['date', 'state']]
dfShooting['date'] = pd.to_datetime(dfShooting['date'])
dfShooting['year'] = pd.DatetimeIndex(dfShooting['date']).year
year_list = list(dfShooting['year'].unique())
year = st.sidebar.selectbox('Select a year', year_list)
del dfShooting['date']
new_df = dfShooting[dfShooting.year == year]
new_df = new_df.groupby('state').count()
new_df['state'] = new_df.index
final_df = new_df.rename(columns={'year': 'counts'})
final_df = final_df[['state', 'counts']]
title = f"The Number of US Police Shootings in {year} for Different States in Descending Order"
sorted_df = final_df.sort_values('counts', ascending=False)
sorted_df.index = np.arange(len(sorted_df))
table = st.sidebar.checkbox('View Table')
if table is True:
    st.write(sorted_df)
st.write(title)
st.write(alt.Chart(sorted_df).mark_bar().encode(x=alt.X('state', sort=None), y='counts'))