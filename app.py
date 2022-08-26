import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.express as px 
import streamlit as st
import streamlit as st
from wordcloud import WordCloud

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
                            'LikeCount',
                            'tweets_clean']]
    df = df_interim.copy()
    return df

df_ch = load_data()

neg = df_ch[df_ch['sentimiento'] == 'NEG']
pos = df_ch[df_ch['sentimiento'] == 'POS']

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Tweets de prensa escrita uruguaya')
st.subheader('Dataframe')
st.dataframe(df_ch)
st.subheader('Palabras asociadas al sentimiento negativo')
text = ' '.join(i for i in neg.tweets_clean)
wordcloud = WordCloud(max_words=100, background_color='White').generate(text)
plt.style.use('classic')
plt.figure(figsize = (12,12))
plt.imshow(wordcloud, interpolation='bilinear')
plt.show()
st.pyplot()

st.subheader('Palabras asociadas al sentimiento positivo')
text = ' '.join(i for i in pos.tweets_clean)
wordcloud = WordCloud(max_words=100, background_color='White').generate(text)
plt.style.use('classic')
plt.figure(figsize = (12,12))
plt.imshow(wordcloud, interpolation='bilinear')
plt.show()
st.pyplot()

#st.subheader('Cantidad de tweest por User y por sentimiento')

# Heroku uses the last version of python, but it conflicts with 
# some dependencies. Low your version by adding a runtime.txt file
# https://stackoverflow.com/questions/71712258/