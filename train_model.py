import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib
import re

# Enhanced Data (more examples)
data = {
    'text': [
        # Family
        "I'm grateful for my family's love and support.",
        "My family is my rock and my support system.",
        "I am grateful for the laughter I share with my family.",
        "My children fill my heart with joy.",
        "I love and appreciate my parents.",
        "I'm thankful for my siblings and the bond we share.",
        "Family gatherings always make me happy.",
        "I cherish the memories I create with my family.",
        "I'm grateful for the support my family gives me.",
        "My family makes me feel loved and accepted.",

        # Nature
        "I appreciate the warm sunshine on my face.",
        "I appreciate the beauty of nature around me.",
        "The sunshine makes me feel happy and optimistic.",
        "I love spending time in nature.",
        "I appreciate the beauty of a sunset.",
        "I enjoyed a walk in the park.",
        "The sound of rain is soothing to me.",
        "I'm grateful for the fresh air and blue skies.",
        "Nature's beauty fills me with awe and wonder.",
        "I love the feeling of the earth beneath my feet.",

        # Friends
        "My friends make me laugh and feel connected.",
        "My friends are like family to me.",
        "I enjoyed a wonderful conversation with a friend.",
        "I am grateful for the friendships I have.",
        "Friends make life more fun and meaningful.",
        "I appreciate the support and encouragement from my friends.",
        "I'm thankful for friends who are always there for me.",
        "I cherish the memories I make with my friends.",
        "I'm grateful for friends who accept me for who I am.",
        "I love spending time with my friends.",

        # Health
        "I'm thankful for my good health and energy.",
        "I'm thankful for my ability to learn and grow.",
        "I'm thankful for the strength I have inside.",
        "I appreciate having a healthy body and mind.",
        "I'm grateful for the ability to overcome challenges.",
        "I'm thankful for every day I feel healthy and strong.",
        "I appreciate the ability to move my body freely.",
        "I'm grateful for the healthcare professionals who keep me healthy.",
        "I appreciate the ability to take care of my body.",
        "I'm thankful for the vitality and energy I have.",

        # Food
        "I enjoyed a delicious and satisfying meal.",
        "I am thankful for the food on my table.",
        "I appreciate the variety of foods I have access to.",
        "Cooking and sharing meals with loved ones brings me joy.",
        "I'm grateful for the farmers who grow our food.",
        "I enjoy trying new and different foods.",
        "I'm thankful for the abundance of food in my life.",
        "Food is a source of pleasure and nourishment.",
        "I appreciate the cultural significance of food.",
        "I'm grateful for the ability to enjoy food with all my senses.",

        # Home
        "I'm grateful for the roof over my head.",
        "I enjoyed a relaxing evening at home.",
        "I am grateful for my comfortable bed.",
        "I appreciate having a safe and comfortable home.",
        "My home is my sanctuary, a place of peace and comfort.",
        "I'm thankful for the space I have to live and grow.",
        "I enjoy decorating and making my home my own.",
        "My home is a place where I feel safe and secure.",
        "I appreciate the warmth and comfort of my home.",
        "I'm grateful for the memories I create in my home.",

        # Pets
        "My pet brings me so much joy and comfort.",
        "I enjoy spending time with my pets.",
        "Pets are a source of unconditional love.",
        "I'm grateful for the companionship of my pet.",
        "I appreciate the way my pet makes me laugh.",
        "I'm thankful for the responsibility of caring for a pet.",
        "Animals enrich our lives in so many ways.",
        "I love the unconditional love of my pet.",
        "I appreciate the way my pet makes me feel loved.",
        "Pets teach us so much about life and love.",

        # Opportunities
        "I'm thankful for the opportunities I have.",
        "I feel grateful for the opportunity to travel.",
        "I am thankful for the opportunity to make a difference.",
        "I appreciate the opportunity to grow and evolve.",
        "I'm grateful for the chance to learn and expand my knowledge.",
        "I'm thankful for the opportunities to help others.",
        "I appreciate the opportunity to live my life to the fullest.",
        "I'm grateful for the opportunities that come my way.",
        "I appreciate the chance to try new things.",
        "Opportunities help me grow and learn.",

        # Happiness
        "I'm grateful for the small moments of happiness.",
        "I appreciate the simple things in life.",
        "Happiness is a choice and I choose to be happy.",
        "I'm grateful for the laughter and joy in my life.",
        "I appreciate the moments of peace and contentment.",
        "I'm thankful for the ability to find happiness in everyday life.",
        "I enjoy the feeling of happiness and gratitude.",
        "Happiness is a feeling of contentment and joy.",
        "I appreciate the people who bring happiness into my life.",
        "I'm grateful for the things that make me happy.",

        # Kindness
        "I appreciate the kindness of strangers.",
        "Kindness is contagious and makes the world a better place.",
        "I'm grateful for the acts of kindness I receive and give.",
        "I appreciate the people who show me kindness and compassion.",
        "I'm thankful for the opportunity to be kind to others.",
        "Kindness is a strength, not a weakness.",
        "I enjoy spreading kindness wherever I go.",
        "Kindness makes me feel good about myself.",
        "I appreciate the kindness and generosity of others.",
        "I'm grateful for the people who have shown me kindness.",

        # New Day
        "I appreciate the gift of each new day.",
        "Every day is a new opportunity to make a positive impact.",
        "I'm grateful for the chance to start fresh each morning.",
        "I appreciate the beauty and potential of a new day.",
        "I'm thankful for the gift of life and each new day it brings.",
        "I enjoy waking up to a new day full of possibilities.",
        "Every day is a gift, that's why it's called the present.",
        "I appreciate the chance to learn and grow each day.",
        "I'm grateful for the new day and all it brings.",
        "Each day is a new beginning.",

        # Work
        "My work gives me a sense of purpose.",
        "I appreciate the support from my colleagues.",
        "I'm grateful for the opportunity to use my skills and talents.",
        "I'm thankful for a job that challenges and rewards me.",
        "I appreciate the people I work with.",
        "I'm grateful for the opportunity to contribute to something meaningful.",
        "Work allows me to learn, grow, and make a difference.",
        "I appreciate the sense of accomplishment I get from my work.",
        "I'm grateful for the opportunity to work with a great team.",
        "My work allows me to provide for myself and my family.",

        # Challenges
        "I'm thankful for the challenges that make me stronger.",
        "Challenges help me learn and grow as a person.",
        "I appreciate the opportunity to overcome obstacles.",
        "I'm grateful for the resilience I've developed through challenges.",
        "Challenges make life more interesting and rewarding.",
        "I'm thankful for the lessons I've learned from challenges.",
        "Overcoming challenges gives me a sense of accomplishment.",
        "Challenges help me discover my inner strength.",
        "I appreciate the opportunity to test my limits.",
        "Challenges make me a better person.",

        # Relaxation
        "I enjoyed a good book and a cup of tea.",
        "I enjoyed a moment of quiet reflection.",
        "I appreciate the ability to relax and recharge.",
        "I'm grateful for the time I have to unwind and de-stress.",
        "Relaxation is essential for my well-being.",
        "I enjoy activities that help me relax and find inner peace.",
        "I'm thankful for the moments of calm and tranquility.",
        "Relaxation helps me clear my mind and focus.",
        "I appreciate the ability to let go of stress.",
        "I'm grateful for the time I have to myself.",

        # Love
        "I'm grateful for the love in my life.",
        "My partner makes me feel loved and cherished.",
        "I am grateful for the love and acceptance I receive.",
        "I am grateful for the love and happiness in my life.",
        "Love is the most powerful force in the universe.",
        "I appreciate the people who love and support me.",
        "I'm thankful for the ability to love and be loved.",
        "Love makes life worth living.",
        "I appreciate the people who show me love.",
        "I'm grateful for the feeling of love.",

        # Hobbies
        "My hobbies bring me joy and relaxation.",
        "I love listening to music.",
        "I enjoy learning new things.",
        "I appreciate the beauty of art and music.",
        "Hobbies enrich my life and make me a more well-rounded person.",
        "I'm grateful for the time I have to pursue my passions.",
        "I enjoy the creative outlet that my hobbies provide.",
        "Hobbies give me a sense of accomplishment.",
        "I appreciate the opportunity to learn new skills through my hobbies.",
        "My hobbies help me connect with others.",

        # Belief
        "I'm thankful for the people who believe in me.",
        "My faith gives me hope and comfort.",
        "I believe in the goodness of people.",
        "I'm grateful for the support of my community.",
        "I have faith in a higher power.",
        "I believe in myself and my ability to achieve my goals.",
        "I'm thankful for the people who inspire and uplift me.",
        "Belief gives me strength and courage.",
        "I appreciate the power of faith.",
        "I'm grateful for the people who share my beliefs.",

        # Lessons
        "I'm grateful for the lessons I've learned.",
        "Lessons help me grow and become a better person.",
        "I appreciate the opportunity to learn from my mistakes.",
        "I'm thankful for the wisdom I've gained through experience.",
        "Life is a journey of learning and growth.",
        "I enjoy the process of learning and discovering new things.",
        "I'm grateful for the teachers and mentors who have guided me.",
        "Lessons make me wiser and more resilient.",
        "I appreciate the opportunity to learn from others.",
        "I'm grateful for the knowledge I've gained.",

        # Positive Thinking
        "I appreciate the power of positive thinking.",
        "Positive thinking helps me overcome challenges and achieve my goals.",
        "I'm grateful for the ability to focus on the good.",
        "I believe in the power of positive affirmations.",
        "I'm thankful for the people who bring positivity into my life.",
        "I enjoy the feeling of optimism and hope.",
        "Positive thinking makes me more resilient and happy.",
        "I appreciate the ability to see the good in every situation.",
        "Positive thinking attracts positive experiences.",
        "I'm grateful for the power of my thoughts.",

        # Dreams
        "My dreams inspire me to achieve great things.",
        "I'm grateful for the ability to dream and imagine.",
        "Dreams give me a sense of purpose and direction.",
        "I appreciate the power of visualization and goal setting.",
        "I'm thankful for the people who support my dreams.",
        "I enjoy the process of pursuing my dreams and aspirations.",
        "Dreams make life more exciting and fulfilling.",
        "I appreciate the ability to set goals and achieve them.",
        "Dreams motivate me to become a better version of myself.",
        "I'm grateful for the power of imagination.",

        # Growth
        "I'm grateful for the opportunity to grow and learn.",
        "Personal growth is a journey, not a destination.",
        "I appreciate the challenges that help me grow.",
        "I'm thankful for the people who support my growth.",
        "Growth is essential for a fulfilling life.",
        "I enjoy the process of learning and evolving.",
        "I'm grateful for the experiences that shape who I am.",
        "Growth makes me a stronger and more resilient person.",
        "I appreciate the opportunity to become the best version of myself.",
        "I'm thankful for the lessons that help me grow.",

        # Technology
        "I'm grateful for the technology that makes my life easier.",
        "Technology connects me with people all over the world.",
        "I appreciate the convenience of online shopping.",
        "I'm thankful for the ability to learn new things online.",
        "Technology helps me stay organized and productive.",
        "I enjoy the entertainment that technology provides.",
        "I'm grateful for the advancements in healthcare technology.",
        "Technology allows me to work remotely and have more flexibility.",
        "I appreciate the creativity and innovation in the tech world.",
        "Technology empowers me to do more.",

        # Money
        "I'm grateful for the financial abundance in my life.",
        "Money allows me to provide for myself and my loved ones.",
        "I appreciate the freedom and security that money provides.",
        "I'm thankful for the opportunity to earn a good living.",
        "Money allows me to pursue my passions and dreams.",
        "I enjoy the experiences and opportunities that money can buy.",
        "I'm grateful for the ability to manage my finances responsibly.",
        "Money is a tool that can be used for good.",
        "I appreciate the value and importance of financial literacy.",
        "I'm thankful for the ability to save and invest for the future.",

        # Weather
        "I appreciate the beauty of a sunny day.",
        "I enjoy the cozy feeling of a rainy day.",
        "The changing seasons remind me of the beauty of nature.",
        "I'm grateful for the fresh air and sunshine.",
        "I love the feeling of the warm sun on my skin.",
        "The sound of rain is calming and relaxing.",
        "I appreciate the variety and beauty of different weather patterns.",
        "Weather can be a source of awe and wonder.",
        "I'm grateful for the weather that allows me to enjoy outdoor activities.",
        "I appreciate the way weather affects my mood and energy.",

        # Animals
        "I'm grateful for the animals that share our planet.",
        "Animals bring joy and companionship to our lives.",
        "I appreciate the diversity and beauty of the animal kingdom.",
        "I'm thankful for the role animals play in our ecosystem.",
        "I love watching animals in their natural habitat.",
        "Animals teach us about love, loyalty, and survival.",
        "I'm grateful for the organizations that protect and care for animals.",
        "Animals inspire me with their strength, resilience, and beauty.",
        "I appreciate the connection I feel with animals.",
        "Animals make the world a more interesting and vibrant place.",

        # Karma
        "I believe in the power of karma.",
        "Good deeds come back to you.",
        "I appreciate the opportunity to make a positive impact on the world.",
        "I'm grateful for the good karma I've created.",
        "Karma is a reminder to treat others with kindness and respect.",
        "I believe in the law of cause and effect.",
        "I'm thankful for the positive energy I attract into my life.",
        "Karma teaches me to be mindful of my actions and their consequences.",
        "I appreciate the balance and justice that karma brings.",
        "I'm grateful for the opportunity to learn and grow from my experiences.",
    ],
    'category': [
        "Family", "Family", "Family", "Family", "Family", "Family", "Family", "Family", "Family", "Family",
        "Nature", "Nature", "Nature", "Nature", "Nature", "Nature", "Nature", "Nature", "Nature", "Nature",
        "Friends", "Friends", "Friends", "Friends", "Friends", "Friends", "Friends", "Friends", "Friends", "Friends",
        "Health", "Health", "Health", "Health", "Health", "Health", "Health", "Health", "Health", "Health",
        "Food", "Food", "Food", "Food", "Food", "Food", "Food", "Food", "Food", "Food",
        "Home", "Home", "Home", "Home", "Home", "Home", "Home", "Home", "Home", "Home",
        "Pets", "Pets", "Pets", "Pets", "Pets", "Pets", "Pets", "Pets", "Pets", "Pets",
        "Opportunities", "Opportunities", "Opportunities", "Opportunities", "Opportunities", "Opportunities", "Opportunities", "Opportunities", "Opportunities", "Opportunities",
        "Happiness", "Happiness", "Happiness", "Happiness", "Happiness", "Happiness", "Happiness", "Happiness", "Happiness", "Happiness",
        "Kindness", "Kindness", "Kindness", "Kindness", "Kindness", "Kindness", "Kindness", "Kindness", "Kindness", "Kindness",
        "New Day", "New Day", "New Day", "New Day", "New Day", "New Day", "New Day", "New Day", "New Day", "New Day",
        "Work", "Work", "Work", "Work", "Work", "Work", "Work", "Work", "Work", "Work",
        "Challenges", "Challenges", "Challenges", "Challenges", "Challenges", "Challenges", "Challenges", "Challenges", "Challenges", "Challenges",
        "Relaxation", "Relaxation", "Relaxation", "Relaxation", "Relaxation", "Relaxation", "Relaxation", "Relaxation", "Relaxation", "Relaxation",
        "Love", "Love", "Love", "Love", "Love", "Love", "Love", "Love", "Love", "Love",
        "Hobbies", "Hobbies", "Hobbies", "Hobbies", "Hobbies", "Hobbies", "Hobbies", "Hobbies", "Hobbies", "Hobbies",
        "Belief", "Belief", "Belief", "Belief", "Belief", "Belief", "Belief", "Belief", "Belief", "Belief",
        "Lessons", "Lessons", "Lessons", "Lessons", "Lessons", "Lessons", "Lessons", "Lessons", "Lessons", "Lessons",
        "Positive Thinking", "Positive Thinking", "Positive Thinking", "Positive Thinking", "Positive Thinking", "Positive Thinking", "Positive Thinking", "Positive Thinking", "Positive Thinking", "Positive Thinking",
        "Dreams", "Dreams", "Dreams", "Dreams", "Dreams", "Dreams", "Dreams", "Dreams", "Dreams", "Dreams",
        "Growth", "Growth", "Growth", "Growth", "Growth", "Growth", "Growth", "Growth", "Growth", "Growth",
        "Technology", "Technology", "Technology", "Technology", "Technology", "Technology", "Technology", "Technology", "Technology", "Technology",
        "Money", "Money", "Money", "Money", "Money", "Money", "Money", "Money", "Money", "Money",
        "Weather", "Weather", "Weather", "Weather", "Weather", "Weather", "Weather", "Weather", "Weather", "Weather",
        "Animals", "Animals", "Animals", "Animals", "Animals", "Animals", "Animals", "Animals", "Animals", "Animals",
        "Karma", "Karma", "Karma", "Karma", "Karma", "Karma", "Karma", "Karma", "Karma", "Karma"
    ]
}

df = pd.DataFrame(data)

# Preprocessing: Handle missing values and non-string data
df['text'] = df['text'].apply(lambda x: str(x) if not isinstance(x, str) else x)

# Text cleaning (remove special characters, extra spaces, etc.)
def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text, re.UNICODE)  # Remove punctuation
    text = text.lower()  # Lowercase
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

df['text'] = df['text'].apply(clean_text)


X = df['text']
y = df['category']

# Split data for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) # Added test split

model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred)) # Added classification report
print("Accuracy:", accuracy_score(y_test, y_pred)) # Added accuracy score

joblib.dump(model, 'gratitude_model.joblib')

# Example of making a prediction:
new_gratitude = "I am thankful for my warm bed and cozy blanket."
predicted_category = model.predict([new_gratitude])[0]
print(f"Predicted category for '{new_gratitude}': {predicted_category}")

# Function to get gratitude suggestions
def get_gratitude_suggestion(text):
    predicted_category = model.predict([text])[0]
    # (Enhancement) You could add logic here to suggest gratitudes 
    # based on the predicted category.  This would require a 
    # larger database of example gratitudes.  For now, just return
    # the predicted category.
    return predicted_category

# Example usage:
user_input = "I had a great day at work."
suggestion = get_gratitude_suggestion(user_input)
print(f"Gratitude suggestion based on '{user_input}': {suggestion}")