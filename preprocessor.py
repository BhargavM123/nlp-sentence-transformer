import re
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import nltk
# nltk.download('vader_lexicon')

sentiments = SentimentIntensityAnalyzer()

def preprocess(data):
    pattern = '\d{1,2}\/\d{1,2}\/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'

    messages = re.split(pattern, data)[2:]

    dates = re.findall(pattern, data)[1:]

    df = pd.DataFrame({'user_messages': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)

        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages

    df.drop(columns=['user_messages'], inplace=True)

    df['year'] = df['date'].dt.year
    df['minute'] = df['date'].dt.minute
    df['hour'] = df['date'].dt.hour
    df['day'] = df['date'].dt.day
    df['month'] = df['date'].dt.month_name()
    df['day_name'] = df['date'].dt.day_name()

    df = df.dropna(how='all')

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    df["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in df["message"]]
    df["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in df["message"]]
    df["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in df["message"]]

    return df