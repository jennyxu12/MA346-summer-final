import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import plotly.express as px

st.title('US Police Shootings')
st.write('link for repo: ')
st.sidebar.header('Welcome to My Dashboard')
st.sidebar.write('Select Your Interested Topic')
topic = st.sidebar.selectbox('Selections', ['States vs Counts based on year', 'Race'])

dfShooting = pd.read_csv('shootings.csv')

if topic == 'States vs Counts based on year':
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
else:
    filtered_df = dfShooting[['state', 'race']]
    sum_df = filtered_df['state'].value_counts()
    filtered_df['combined'] = filtered_df['state'] + ', ' + filtered_df['race']
    filtered_df['counts'] = 0
    filtered_df = filtered_df[['combined', 'counts']]
    count_df = filtered_df.groupby('combined').count()
    count_df['combined'] = count_df.index
    count_df.index = np.arange(len(count_df))
    count_df[['state', 'race']] = count_df['combined'].str.split(pat=", ", expand=True)
    count_df = count_df.merge(sum_df, left_on='state', right_on=sum_df.index, how='left')
    count_df.rename(columns={'state_y': 'sum'}, inplace=True)
    count_df['percentage'] = count_df['counts'] / count_df['sum']
    dfPercentage = pd.read_csv('US population by race.csv')
    final_df = count_df.merge(dfPercentage, left_on='race', right_on='self-identified race', how='left')
    final_df = final_df[['state', 'race', 'counts', 'percentage', 'percentage of the population']]
    fig = px.sunburst(final_df, path=['state', 'race'], values='percentage',
                      color='percentage of the population', color_continuous_scale='Rdbu_r')
    fig.update_layout(autosize=False, width=900, height=680, )
    st.write(fig.show())