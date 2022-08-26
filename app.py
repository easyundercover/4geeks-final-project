import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.express as px 
import streamlit as st

@st.cache
def load_data():
    url = 'https://raw.githubusercontent.com/easyundercover/4geeks-final-project/main/data/processed/df_sentimiento.csv' 
    df = pd.read_csv(url)
    df_interim = df.copy()
    df_interim = df_interim[['User',
                            'Tweet',
                            'sentimiento',
                            'ReplyCount',
                            'RetweetCount',
                            'LikeCount']]
    df = df_interim.copy()
    return df

df_ch = load_data()

st.title('Tweets de prensa escrita uruguaya')
st.subheader('Dataframe')
st.dataframe(df_ch)
st.subheader('Nube de palabras')
col1 = st.columns(1)
fig1 = px.histogram(df_ch, x='User')
col1.plotly_chart(fig1, use_container_width=True)

# Heroku uses the last version of python, but it conflicts with 
# some dependencies. Low your version by adding a runtime.txt file
# https://stackoverflow.com/questions/71712258/