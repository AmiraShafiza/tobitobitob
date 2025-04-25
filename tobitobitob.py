import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="Water Consumption in Malaysia",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

st.title("💧Water Consumption in Malaysia")

df=pd.read_csv('Water_Usage.csv')

# === Filters ABOVE charts ===
st.subheader("🔍 Filter Options")

col1, col2 = st.columns(2)

with col1:
    year_list = sorted(df['Date'].unique())
    selected_years = st.multiselect("Select Year(s)", year_list)

with col2:
    state_list = sorted(df['State'].unique())
    selected_states = st.multiselect("Select State(s)", state_list)

# If no years selected, use all
if not selected_years:
    selected_years = year_list

# If no states selected, use all
if not selected_states:
    selected_states = state_list

# Apply Filters
filtered_df = df[(df['Date'].isin(selected_years)) & (df['State'].isin(selected_states))]

#create the column
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric(
    label="# Total Water Used",
    value=f"{filtered_df['Water Consumed'].sum():,.0f} MLD")
kpi2.metric(
    label="# Average per Year",
    value=f"{filtered_df['Water Consumed'].mean():,.0f} MLD")
kpi3.metric(
    label="# Max Consumption",
    value=f"{filtered_df['Water Consumed'].max():,.0f} MLD")

#create column for chart
fig_col1, fig_col2, fig_col3 = st.columns(3)

with fig_col1:
    st.markdown("# Water Consumption Over Year")

    # Group by Date and State to get total consumption
    state_year_grouped = filtered_df.groupby(['Date', 'State'])['Water Consumed'].sum().reset_index()

    # Line chart: one line per state
    fig = px.line(
        state_year_grouped,
        x='Date',
        y='Water Consumed',
        color='State',
        markers=True,
        labels={
            'Date': 'Year',
            'Water Consumed': 'Water Consumption (MLD)',
            'State': 'State'
        }
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with fig_col2:
    st.markdown("# Water Consumption by State")
    df_states_only = filtered_df[filtered_df['State'] != 'Malaysia']
    state_consumption = df_states_only.groupby('State', as_index=False)['Water Consumed'].sum()
    state_consumption = state_consumption.sort_values(by='Water Consumed', ascending=False)

    fig = px.pie(
        state_consumption,
        names='State',
        values='Water Consumed',
        title='Total Water Consumption by State (MLD)',
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    #fig.update_traces(textinfo='percent+label')
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig)

with fig_col3:
    st.markdown("# Domestic vs Non-Domestic")
    grouped_df = filtered_df.groupby(['Date', 'Sector'])['Water Consumed'].sum().reset_index()

    fig = px.bar(
        grouped_df,
        x='Date',
        y='Water Consumed',
        color='Sector',
        barmode='group',
        labels={
            'Date': 'Year',
            'Water Consumed': 'Water Consumed (MLD)',
            'Sector': 'Sector'
        },
        color_discrete_map={
            'Domestic': 'blue',
            'Non-Domestic': 'orange'
        }
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)
