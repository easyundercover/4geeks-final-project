import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.express as px 
import streamlit as st
import streamlit as st
from wordcloud import WordCloud
import pickle
import numpy as np

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

@st.cache
def load_model():
    loaded_model = pickle.load(open('models/model_1.pkl', 'rb'))
    return loaded_model

users = {'Búsqueda':0, 'El País': 1, 'El Observador': 2, 'La República': 3, 'La diaria': 4, 'Brecha': 5}
personas = ['mujica', 'lacalle', 'vazquez', 'martinez', 'larranaga', 'sendic', 'sartori', 'manini', 'talvi']
persons = {nombre: idx+5 for idx,nombre in enumerate(personas)}

def predic(model, user, person):
    x_aux = np.zeros((1,14))
    #print(x_aux)
    if user != 'Brecha':
        x_aux[0][users[user]] = 1
    x_aux[0][persons[person]] = 1
    #print(user, person)
    #print(x_aux)
    output = model.predict(x_aux)
    if output[0] == 0:
        return 'negativo'
    if output[0] == 1:
        return 'neutral'
    if output[0] == 2:
        return 'positivo'
    return None

my_model = load_model()
df_ch = load_data()

neg = df_ch[df_ch['sentimiento'] == 'NEG']
pos = df_ch[df_ch['sentimiento'] == 'POS']

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title('Proyecto final: Análisis de tweets de la prensa escrita uruguaya')

st.subheader('Probá el modelo!')
users = {'Búsqueda':0, 'El País': 1, 'El Observador': 2, 'La República': 3, 'La diaria': 4, 'Brecha': 5}
personas = ['mujica', 'lacalle', 'vazquez', 'martinez', 'larranaga', 'sendic', 'sartori', 'manini', 'talvi']
persons = {nombre: idx+5 for idx,nombre in enumerate(personas)}

option_persona = st.selectbox(
'Elegí una persona',
personas)

st.write('Persona elegida:', option_persona)

option_medio = st.selectbox(
'Elegí un medio',
['Búsqueda', 'El País', 'El Observador', 'La República', 'La diaria', 'Brecha'])

st.write('Medio elegido:', option_medio)

output = predic(my_model, option_medio, option_persona)
st.subheader('Sentimiento: ' + output)

st.subheader('Datos')
st.dataframe(df_ch)

st.subheader('Palabras asociadas al sentimiento negativo')
st.write('En este gráfico se pueden ver las palabras más nombradas que se asocian con sentimientos negativos')
text = ' '.join(i for i in neg.tweets_clean)
wordcloud = WordCloud(max_words=100, background_color='White').generate(text)
plt.style.use('classic')
plt.figure(figsize = (12,12))
plt.imshow(wordcloud, interpolation='bilinear')
plt.show()
st.pyplot()

st.subheader('Palabras asociadas al sentimiento positivo')
st.write('En este gráfico se pueden ver las palabras más nombradas que se asocian con sentimientos positivos')
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