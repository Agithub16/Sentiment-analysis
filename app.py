import streamlit as st
from newsapi import NewsApiClient
from textblob import TextBlob
import pandas as pd

newsapi = NewsApiClient(api_key='5e295b0d7160431c9d4021cc76152d72')

st.set_page_config(page_title="Pulse Sentiment", page_icon="📊")

st.title("📊 Pulse: Real-Time News Sentiment")
st.markdown("Track the 'vibe' of any topic across global in second and hit **Enter** to analyze.")

topic = st.text_input("Enter Topic (e.g. , Bitcoin, AI =,  Google):","Technology")

if topic:
    with st.spinner(f'Analyzing news for "{topic}"...'):

     all_articles = newsapi.get_everything(q=topic, language='en', sort_by='relevancy', page_size=20)

     # Fetch news

     if all_articles['totalResults'] > 0:
        data = []
        pos, neg, neu =0, 0, 0

        for article in all_articles['articles']:
           text = article['title']
           analysis = TextBlob(text)
           polarity = analysis.sentiment.polarity

           if polarity > 0:
                sentiment = "Positive"
                pos += 1
           elif polarity < 0:
                sentiment = "Negative"
                neg += 1
           else:
                sentiment = "Neutral"
                neu += 1

           data.append([article['publishedAt'][:10], text , sentiment])
           
           df = pd.DataFrame(data, columns = ['Date', 'Headline', 'Sentiment'])


           col1, col2, col3 = st.columns(3)
           col1.metric("positive", pos)
           col2.metric("Neutral", neg)
           col3.metric("Negative", neg)

           st.subheader(f"Sentiment Distribution for '{topic}'")
           st.bar_chart(df['Sentiment'].value_counts())

           st.subheader("Recent Headlines")
           st.table(df)

     else:
           st.error("No articles found for this topic.")
    

st.info("Built with Python, Streamlit, TextBlob for placement Portfolio")

           
