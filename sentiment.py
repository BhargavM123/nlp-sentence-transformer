from nltk.sentiment.vader import SentimentIntensityAnalyzer
sentiments = SentimentIntensityAnalyzer()

def analyze_sentiment(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    df["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in df["message"]]
    df["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in df["message"]]
    df["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in df["message"]]


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


