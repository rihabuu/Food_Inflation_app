import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

data = pd.read_csv("data_FI.csv")
st.write(data.head())

st.title('Monthly Food Price Inflation Estimates by Country')
st.write('Explore the trends, comparisons, and impacts of food price inflation across countries.')

# Date range filter
start_date = st.sidebar.date_input('Start date', data['date'].min())
end_date = st.sidebar.date_input('End date', data['date'].max())
filtered_data = data[(data['date'] >= start_date) & (data['date'] <= end_date)]
if filtered_data.empty:
    st.write("No data available for the selected date range.")
else:
    # viz1:
    st.write('Let\'s take a look at the monthly Inflation by Country')
    pivot_table = filtered_data.pivot('country', 'date', 'Inflation')
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_table, cmap="YlGnBu")
    st.pyplot()

    # viz2:
    st.write('Let\'s take a look at the average Monthly Food Price Inflation Over Time')
    avg_inflation = filtered_data.groupby('date')['Inflation'].mean()
    fig = px.line(avg_inflation, x=avg_inflation.index, y='Inflation', title='Average Monthly Food Price Inflation Over Time')
    st.plotly_chart(fig)

    # viz3:
    st.write('Let\'s take a look at the monthly food price Inflation by country for the Latest Month')
    latest_month_data = filtered_data[filtered_data['date'] == filtered_data['date'].max()]
    fig = px.choropleth(latest_month_data, 
                        locations="country",         
                        locationmode='country names', 
                        color="Inflation",           
                        hover_name="country",        
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title="Monthly Food Price Inflation by Country for the Latest Month")
    st.plotly_chart(fig)

    # viz4:
    st.write('Let\'s take a look at the trend of Monthly Inflation for Top 5 and Bottom 5 Countries')
    top_5_countries = filtered_data.groupby('country')['Inflation'].mean().nlargest(5).index
    bottom_5_countries = filtered_data.groupby('country')['Inflation'].mean().nsmallest(5).index
    selected_countries = top_5_countries.union(bottom_5_countries)
    country_filtered_data = filtered_data[filtered_data['country'].isin(selected_countries)]
    fig = px.line(country_filtered_data, x='date', y='Inflation', color='country', title='Trend of Inflation for Top and Bottom 5 Countries')
    st.plotly_chart(fig)

    # viz5:
    st.write('Let\'s take a look at the Monthly Food Price Inflation for Selected Countries')
    countries = st.sidebar.multiselect("Select countries to compare:", data['country'].unique())

    if not countries: 
        st.write("Please select at least one country to visualize.")
    else:
        country_comparison_data = filtered_data[filtered_data['country'].isin(countries)]
        if country_comparison_data.empty:  
            st.write("No data available for the selected countries.")
        else:
            fig = px.bar(country_comparison_data, x='date', y='Inflation', color='country', barmode='group', title='Comparative Monthly Food Price Inflation')
            st.plotly_chart(fig)

    # viz6:
    st.write('Let\'s take a look at the  Food Price Volatility Over Time for Selected Countries')
    countries_volatility = st.multiselect("Select countries to view volatility:", data['country'].unique())

    if not countries_volatility:  
        st.write("Please select at least one country to view volatility.")
    else:
        filtered_volatility_data = data[data['country'].isin(countries_volatility)]
        if filtered_volatility_data.empty:  
            st.write("No data available for the selected countries' volatility.")
        else:
            filtered_volatility_data = filtered_volatility_data.copy()
            filtered_volatility_data['Volatility'] = filtered_volatility_data['High'] - filtered_volatility_data['Low']
            fig = px.line(filtered_volatility_data, x='date', y='Volatility', color='country', title='Food Price Volatility Over Time')
            st.plotly_chart(fig)

st.caption('ZOUITINA Rihab')
# Invalidate cache for Streamlit Cloud deployment

