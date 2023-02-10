import streamlit as st
import numpy as np
import pandas as pd
from streamlit_option_menu import option_menu
import snscrape.modules.twitter as sntwitter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.express as px 

st.title('Twitter sentiment anslyser')

selected = option_menu(menu_title=None,options= ["Topic/hashtag analysis", 'user analysis'], 
        icons=['bar-chart', 'info-circle'], menu_icon="cast", default_index=0,orientation="horizontal")

if (selected=='Topic/hashtag analysis'):
    st.subheader('Topic/hashtag analyser')
    sentence=st.text_input('Enter any Hashtag or Topic','War in ukraine')
    
    tweets=[]
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(sentence).get_items()):
        if i ==50:
            break
        tweets.append([tweet.date,tweet.likeCount,tweet.rawContent,tweet.user])
    tweets_df=pd.DataFrame(tweets,columns=['Date','Likes','Tweet content','User'])
    print(tweets_df)
    def sentiment(sentence):
        scores=SentimentIntensityAnalyzer()
        sentiment_dict=scores.polarity_scores(sentence)
        if sentiment_dict['compound']>=0.05:
            st.write('😁 positive')
        elif sentiment_dict['compound']<=-0.05:
            st.write('😠 Negative')
        else :
            st.write('🙂 Neutral')
    sentiment(sentence)
    
    sentiments=tweets_df['Tweet content']
    tweets_sentiment=[]
    analyser=SentimentIntensityAnalyzer()
    for i in range(50):
        if i==50:
            break
        text=(sentiments[i])
        ps= analyser.polarity_scores(text)
        if ps['compound']>=0.05:
            senti='😁 positive'
            count=1
        elif ps['compound']<=-0.05:
            senti='😠 Negative'
            count=1
        else:
            senti='🙂 Neutral'
            count=1
        tweets_sentiment.append([text,senti,count])
    sentiments_df=pd.DataFrame(tweets_sentiment,columns=['Tweets','sentiment','count'])
        
    print(sentiments_df)
    if st.button('Visualization'):
        fig=px.bar(sentiments_df,x='sentiment',y='count',color='sentiment')
        st.plotly_chart(fig,use_container_width=True)
        st.dataframe(sentiments_df.head(10))
    
        
    
    
    
