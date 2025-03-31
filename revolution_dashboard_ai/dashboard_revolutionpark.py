
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob

st.title("Oznaczenia na Instagramie – Revolution Park")
uploaded_file = st.file_uploader("Wgraj plik CSV z oznaczeniami", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Data'] = pd.to_datetime(df['Data'])

    # ANALIZA SENTYMENTU
    st.subheader("Analiza sentymentu opisów")
    df['Opis'] = df['Opis'].fillna("")
    df['Sentyment'] = df['Opis'].apply(lambda x: TextBlob(x).sentiment.polarity)
    df['Nastrój'] = df['Sentyment'].apply(lambda x: "Pozytywny" if x > 0.1 else ("Negatywny" if x < -0.1 else "Neutralny"))

    # Filtry
    st.sidebar.header("Filtry")
    autorzy = st.sidebar.multiselect("Autorzy", df['Autor'].unique(), default=df['Autor'].unique())
    min_lajki = st.sidebar.slider("Minimalna liczba lajków", 0, int(df['Lajki'].max()), 0)
    nastrój_filter = st.sidebar.multiselect("Nastrój", df['Nastrój'].unique(), default=df['Nastrój'].unique())

    df_filtered = df[
        (df['Autor'].isin(autorzy)) &
        (df['Lajki'] >= min_lajki) &
        (df['Nastrój'].isin(nastrój_filter))
    ]

    # Tabela
    st.subheader("Tabela postów")
    st.dataframe(df_filtered)

    # Statystyki
    st.subheader("Statystyki")
    st.write(f"Liczba postów: {len(df_filtered)}")
    st.write(f"Średnia liczba lajków: {df_filtered['Lajki'].mean():.1f}")

    # Wykres lajków w czasie
    st.subheader("Liczba lajków w czasie")
    likes_by_date = df_filtered.groupby(df_filtered['Data'].dt.date)['Lajki'].sum()
    fig, ax = plt.subplots()
    likes_by_date.plot(kind='line', ax=ax)
    st.pyplot(fig)

    # Wykres nastroju
    st.subheader("Rozkład nastrojów")
    st.bar_chart(df_filtered['Nastrój'].value_counts())

    # Linki do postów
    st.subheader("Linki do postów")
    for _, row in df_filtered.iterrows():
        st.markdown(f"[{row['Autor']}]({row['Link']}) – {row['Data'].strftime('%Y-%m-%d')} ({row['Lajki']} lajków) | *{row['Nastrój']}*")

else:
    st.info("Wgraj plik CSV z wynikami scrappera, aby zobaczyć dane.")
