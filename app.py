import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns


import helper
import preprocessor
# import sentiment

st.sidebar.title("WhatsApp chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)

    # st.dataframe(df)

    user_list = df['users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox('Show analysis wrt', user_list)

    if st.sidebar.button("Show analysis"):
        total_messages, total_words, total_media, total_links = helper.fetch_stats(selected_user,df)


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(total_messages)
        with col2:
            st.header("total words")
            st.title(total_words)
        with col3:
            st.header("total media")
            st.title(total_media)
        with col4:
            st.header("total links")
            st.title(total_links)

        #most active users on the group
        if selected_user == 'Overall':
            st.title("Most active users")
            x, new_df = helper.most_active_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                ax.barh(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(wc)
        st.pyplot(fig)

        #most common words
        common_words_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()
        ax.barh(common_words_df[0],common_words_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most Common Words')
        st.pyplot(fig)

        # st.dataframe(common_words_df)

        # monthly timeline of num of messages in group

        df_timeline = helper.monthly_timeline(selected_user,df)

        fig,ax = plt.subplots()
        ax.plot(df_timeline['time'],df_timeline['message'], color='teal')
        plt.xticks(rotation='vertical')

        st.title('montly timeline')
        st.pyplot(fig)

        # daily timeline of num of messages in group

        df_timeline_daily = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()
        ax.plot(df_timeline_daily['only_date'], df_timeline_daily['message'], color='teal')
        plt.xticks(rotation='vertical')

        st.title('daily timeline')
        st.pyplot(fig)

        #weekly activity of group

        st.title('weekly activity')

        col1,col2 = st.columns(2)

        with col1:
            st.header('Busy Day')
            busy_day = helper.weekly_ativity(selected_user,df)

            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='orange')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        with col2:
            st.header('Busy Month')
            busy_month = helper.monthly_ativity_map(selected_user,df)

            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        st.title("Sentiment of Messages Sent")
        sentiment = helper.analyz_sentiments(selected_user,df)
        st.title(sentiment)

