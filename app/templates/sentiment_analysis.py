from textblob import TextBlob

def analyze_sentiment(text):
    analysis = TextBlob(text)
    # Returns a value between -1 (very negative) and 1 (very positive)
    return analysis.sentiment.polarity
