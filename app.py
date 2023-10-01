import matplotlib.pyplot as plt
import streamlit as st
import preprocessor,helper
import seaborn as sns

st.sidebar.title('WA')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode('utf-8')
    # st.text(data) # this will show the byte data as text
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique user
    user_list =df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('show analysis wrt',user_list)

    if st.sidebar.button('show analysis'):
       num_messages,words,media,links=helper.fetch_stats(selected_user,df)
       col1,col2,col3,col4 = st.columns(4)
       with col1:
            st.header('total message')
            st.title(num_messages)
       with col2:
            st.header('total words')
            st.title(words)
       with col3:
            st.header('total media')
            st.title(media)
       with col4:
            st.header('total shared link')
            st.title(links)

       # monthly_time line
       st.title('Monthly Timeline')
       time_line = helper.monthly_timeline(selected_user,df)
       fig,ax=plt.subplots()
       ax.plot(time_line['time'],time_line['message'],color='green')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)

       # daily_timeline
       st.title('Daily Timeline')
       daily_timeline = helper.daily_timeline(selected_user,df)
       fig,ax=plt.subplots()
       ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='black')
       plt.xticks(rotation='vertical')
       st.pyplot(fig)


       # activity map

       st.title('Activity map')
       col1,col2=st.columns(2)
       with col1:
           st.header('most busy day')
           busy_day=helper.week_activity_map(selected_user,df)
           fig,ax=plt.subplots()
           ax.bar(busy_day.index,busy_day.values)
           st.pyplot(fig)
       with col2:
           st.header('most busy month')
           busy_month=helper.month_activity_map(selected_user,df)
           fig,ax=plt.subplots()
           ax.bar(busy_month.index,busy_month.values,color='orange')
           plt.xticks(rotation='vertical')
           st.pyplot(fig)

       st.title('Weekly activity map')
       user_heatmap = helper.activity_heatmap(selected_user,df)
       fig,ax=plt.subplots()
       ax=sns.heatmap(user_heatmap)
       st.pyplot(fig)

       # finding the busiest user in the group(group level)


       if selected_user=='Overall':
           st.title('most busy user')
           x,new_df=helper.most_busy_user(df)
           fig,ax = plt.subplots()
           col4,col5=st.columns(2)
           with col4:
               ax.bar(x.index,x.values,color='red')
               st.pyplot(fig)
           with col5:
               st.dataframe(new_df)
       # word cloud
       st.title('WordCloud')
       df_wc = helper.create_wordcloud(selected_user,df)
       fig,ax = plt.subplots()
       ax.imshow(df_wc)
       st.pyplot(fig)

       # most common word
       most_common_df = helper.most_common_words(selected_user,df)
       fig,ax = plt.subplots()
       st.title('Most common words')
       ax.barh(most_common_df[0],most_common_df[1])
       plt.xticks(rotation='vertical')
       st.pyplot(fig)
       st.dataframe(most_common_df)

       # emoji analysis
       emoji_df = helper.emoji_helper(selected_user,df)
       st.title('Emoji Analysis')
       col1,col2 = st.columns(2)

       with col1:
           st.dataframe(emoji_df)
       with col2:
           fig,ax=plt.subplots()
           ax.pie(emoji_df[1],labels=emoji_df[0],autopct='%0.2f')
           st.pyplot(fig)





