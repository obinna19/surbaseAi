import pandas as pd
import plotly.express as px
import streamlit as st
from datetime import date
#import geopy.geocoders import Nominatim
#from streamlit_folium import folium_static


###############################################3######################
####### LOAD DATA
#####################################################################
YEAR = 2023

@st.cache_data(max_entries=5)
def load_data():
    data = pd.read_csv('./app/Cybercrime_data.csv')
    return data

df = load_data()
attack_loc = df['location'].unique()




###############################################3######################
####### UI
#####################################################################

st.title('Cybercrime World Report✔📊')

#with st.sidebar:
#    st.header("Configuration")

with st.expander("Configuration", icon="🎎"):
    left_filter, right_filter = st.columns(2, gap="medium")


with left_filter:
    selected_country = st.selectbox(
        "Select Country", 
        attack_loc,
        None
    )
with right_filter:
    attack_typ = st.selectbox(
        'Select Attack type', 
        df['attack_type'].unique(),
        None

    )
#st.title(selected_country)

if selected_country:
    df = df[df['location'] == selected_country]

if attack_typ:
    df = df[df['attack_type'] == attack_typ]


total_outcome = len(df['attack_severity'])
success_attack = len(df[df["outcome"]=="Success"])
percen_rating = round(total_outcome - success_attack) / 100
aver_data = round(df['data_compromised_GB'].mean(), 2)



count_outcome = df.groupby(by=["target_system", "attack_type"] )[["attack_severity"]].sum().reset_index().sort_values(by="attack_severity")
#st.write(count_outcome)
st.subheader("Attack Level")
st.line_chart(
    count_outcome, 
    x ="target_system",
    y ="attack_type",
    color = ["#ffaa00"] 
)


st.subheader("Table Summary")
row_metrics = st.columns(2)

#st.write(country_attack)

with row_metrics[0]:
    with st.container(border=True):
        st.metric(
            "Total No. of Attacks", 
            total_outcome,
            delta= f"{aver_data:.2f} % Data Breach",
            help="% Data breach",
        )
with row_metrics[1]:
    with st.container(border=True):
        st.metric(
            "Total Success Attack", 
            success_attack,
            delta=f"{percen_rating/100:.2f} % Loss",
             help="% failed attack",
        )

fig_outcome = px.bar(
    count_outcome,
    x = "target_system",
    y = "attack_type",
    orientation = "h",
    title = "<b>Cybercrime Attack levels</b>",
    color_discrete_sequence = ["#0083B8"] * len(count_outcome),
    template = "plotly_white",

)
fig_outcome.update_layout(
    plot_bgcolor = "rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

data_breach = df.groupby(by=["target_system", "security_tools_used"] )[["data_compromised_GB"]].sum().reset_index().sort_values(by="data_compromised_GB")
fig_data = px.bar(
    data_breach,
    x ="target_system",
    y= "security_tools_used",
    title = "<b>Cybercrime Data breach levels</b>",
    color_discrete_sequence = ["#0083B8"] * len(data_breach),
    template = "plotly_white",
)
fig_data.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)
st.subheader("Target Distribution")
left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_outcome, use_container_width=True)
right_column.plotly_chart(fig_data, use_container_width=True)

# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#st.write(df)
st.subheader("Cybercrime Table Data")
st.dataframe(df, hide_index=True)


