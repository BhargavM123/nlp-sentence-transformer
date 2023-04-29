import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter

extracter = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    total_messages = df.shape[0]

    words = []
    for word in df['message']:
        words.extend(word.split())

    total_words = len(words)

    #no of media shared

    total_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    #no of links shared

    links = []
    for url in df['message']:
        links.extend(extracter.find_urls(url))

    total_links = len(links)




    return total_messages, total_words, total_media, total_links


def most_active_users(df):

    x = df['users'].value_counts().head(5)
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percentage'})

    return x,df

def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['users'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        new_words = []

        for word in message.lower().split():
            if word not in stop_words:
                new_words.append(word)
        return " ".join(new_words)


    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')

    temp['message'] = temp['message'].apply(remove_stop_words)
    wc_df = wc.generate(temp['message'].str.cat(sep=' '))

    return wc_df

def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()



    temp = df[df['users'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    new_words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                new_words.append(word)

    return_df = pd.DataFrame(Counter(new_words).most_common(20))

    return return_df


def monthly_timeline(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index().sort_values(by=['year','month_num'], ascending=True)
    new_tl = timeline.reset_index(drop=True)

    time = []
    for i in range(new_tl.shape[0]):
        time.append(new_tl['month'][i] + '-' + str(new_tl['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df["only_date"] = df['date'].dt.date

    daily_timeline = df.groupby('only_date').count().reset_index()

    return daily_timeline


def weekly_ativity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def monthly_ativity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def analyz_sentiments(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    x = sum(df["Positive"])
    y = sum(df["Negative"])
    z = sum(df["Neutral"])

    def sentiment_score(a, b, c):
        if (a > b) and (a > c):
            str1 = "Positive 😊 "
            return str1
        elif (b > a) and (b > c):
            str1 = "Negative 😠 "
            return str1
        else:
            str1 = "Neutral 🙂 "
            return str1

    u = sentiment_score(x, y, z)
    return u