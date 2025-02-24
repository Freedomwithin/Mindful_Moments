# helpers.py

import random
from textblob import TextBlob
import requests
import os
from collections import Counter
import logging

logger = logging.getLogger(__name__)

def mood_to_value(mood):
    mood_values = {
        'Very Happy': 5,
        'Happy': 4,
        'Neutral': 3,
        'Sad': 2,
        'Very Sad': 1
    }
    return mood_values.get(mood, 3)  # Default to Neutral if mood not found

def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        return blob.sentiment.polarity
    except Exception as e:
        logger.error(f"Error in sentiment analysis: {e}")
        return 0  # Default sentiment score

def get_gratitude_suggestions(prompt):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        logger.warning("OPENAI_API_KEY not set. Gratitude suggestions will not work.")
        return ["Please set the OpenAI API key to use this feature."]
    
    try:
        response = requests.post(
            "https://api.openai.com/v1/engines/text-davinci-002/completions",
            headers={"Authorization": f"Bearer {openai_api_key}"},
            json={
                "prompt": f"Generate 3 gratitude suggestions based on: {prompt}",
                "max_tokens": 100,
                "n": 1,
                "stop": None,
                "temperature": 0.7,
            }
        )
        response.raise_for_status()
        suggestions = response.json()['choices'][0]['text'].strip().split('\n')
        return [s.strip() for s in suggestions if s.strip()]
    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return ["Failed to get gratitude suggestions. Please try again later."]
    except (KeyError, IndexError) as e:
        logger.error(f"Error parsing OpenAI response: {e}")
        return ["Failed to parse suggestions from the API response."]
    except Exception as e:
        logger.exception("Unexpected error in get_gratitude_suggestions")
        return ["An unexpected error occurred while generating suggestions."]

def get_random_quote():
    quotes = [
        "Gratitude turns what we have into enough.",
        "Gratitude is the fairest blossom which springs from the soul.",
        "Gratitude is a powerful catalyst for happiness.",
        "Gratitude makes sense of our past, brings peace for today, and creates a vision for tomorrow.",
        "Gratitude is the healthiest of all human emotions.",
    ]
    return random.choice(quotes)

def generate_ai_insights(entries):
    if not entries:
        return ["Start your gratitude journey by adding your first entry!"]
    
    categories = Counter(entry.category for entry in entries if entry.category)
    
    insights = []
    for category, count in categories.most_common(3):
        insights.append(f"You often express gratitude for {category}. That's wonderful!")
    
    if len(entries) > 10:
        insights.append("Great job on maintaining a consistent gratitude practice!")
    elif len(entries) > 5:
        insights.append("You're building a good habit. Keep up the great work!")
    else:
        insights.append("Remember, consistency is key. Try to journal a little each day.")
    
    return insights
