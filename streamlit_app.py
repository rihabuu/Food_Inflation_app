import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource

data = pd.read_csv("food_inflation.csv")

st.title('Monthly Food Price Inflation Estimates by Country')
st.write('Explore the trends, comparisons, and impacts of food price inflation across countries.')
st.set_option('deprecation.showPyplotGlobalUse', False)
st.sidebar.header('Student Information')
st.sidebar.write('Student ID: ZOUITINA Rihab- BIA2')
st.sidebar.write('Class: #datavz2023efrei')
st.sidebar.write('GitHub: [Your GitHub link here](https://github.com/rihabuu)') 

# viz1:
st.write('Let\'s take a look at the monthly Inflation by Country')
pivot_table = data.pivot(index='country', columns='date', values='Inflation')
plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap="YlGnBu")
st.pyplot()

# viz2:
st.write('Let\'s take a look at the average Monthly Food Price Inflation Over Time')
avg_inflation = data.groupby('date')['Inflation'].mean()
fig = px.line(avg_inflation, x=avg_inflation.index, y='Inflation', title='Average Monthly Food Price Inflation Over Time')
st.plotly_chart(fig)

# viz3:
st.write('Let\'s take a look at the monthly food price Inflation by country for the Latest Month')
latest_month_data = data[data['date'] == data['date'].max()]
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
top_5_countries = data.groupby('country')['Inflation'].mean().nlargest(5).index
bottom_5_countries = data.groupby('country')['Inflation'].mean().nsmallest(5).index
selected_countries = top_5_countries.union(bottom_5_countries)
country_data = data[data['country'].isin(selected_countries)]
fig = px.line(country_data, x='date', y='Inflation', color='country', title='Trend of Inflation for Top and Bottom 5 Countries')
st.plotly_chart(fig)

# viz5:
st.write('Let\'s take a look at the Monthly Food Price Inflation for Selected Countries')
countries = st.multiselect("Select countries to compare:", data['country'].unique())

if not countries: 
    st.write("Please select at least one country to visualize.")
else:
    country_comparison_data = data[data['country'].isin(countries)]
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
    volatility_data = data[data['country'].isin(countries_volatility)]
    if volatility_data.empty:  
        st.write("No data available for the selected countries' volatility.")
    else:
        volatility_data = volatility_data.copy()
        volatility_data['Volatility'] = volatility_data['High'] - volatility_data['Low']
        fig = px.line(volatility_data, x='date', y='Volatility', color='country', title='Food Price Volatility Over Time')
        st.plotly_chart(fig)

st.caption('ZOUITINA Rihab')


