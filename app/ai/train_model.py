import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from collections import Counter
import joblib
import re

# Enhanced Data (even more examples)
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
        "Spending time with my family is the best part of my day.",
        "I am grateful for the traditions and values my family upholds.",
        "My family has taught me resilience and perseverance.",
        "I am grateful for the unconditional love I receive from my family.",
        "My family is my safe haven, a place where I can always be myself.",

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
        "The gentle breeze whispers through the trees, calming my soul.",
        "The vibrant colors of wildflowers brighten my day.",
        "I am grateful for the peace and serenity I find in nature.",
        "The vastness of the ocean reminds me of the infinite possibilities.",
        "The starry night sky fills me with wonder and inspiration.",

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
        "My friends are my chosen family, providing love and laughter.",
        "I am grateful for the trust and loyalty I share with my friends.",
        "My friends inspire me to be a better person.",
        "I am grateful for the shared experiences and inside jokes with my friends.",
        "My friends make me feel like I belong and am never alone.",

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
        "I am grateful for my senses, which allow me to experience the world fully.",
        "I am grateful for the restorative power of sleep.",
        "I am grateful for the ability to nourish my body with healthy food.",
        "I am grateful for my body's resilience and ability to heal.",
        "I am grateful for my mind's capacity for learning and growth.",

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
        "I am grateful for the smells that arise while cooking a meal.",
        "I am grateful for the creativity involved in cooking.",
        "I am grateful for the experience of sharing meals with loved ones.",
        "I am grateful for the nutritional value of fruits and vegetables.",
        "I am grateful for the abundance of fresh produce during the harvest season.",

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
        "I am grateful for my cozy blanket on a cold night.",
        "I am grateful for the sunlight streaming through my windows.",
        "I am grateful for the sense of belonging I feel in my home.",
        "I am grateful for the memories created within these walls.",
        "I am grateful for my family and pets that fill my home with love and laughter.",

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
        "I am grateful for the soft fur of my pet.",
        "I am grateful for the loyalty and devotion of my pet.",
        "I am grateful for the way my pet always knows how to cheer me up.",
        "I am grateful for the exercise I get from walking my pet.",
        "I am grateful for the connection I share with my pet.",

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
        "I am grateful for the opportunities to connect with new people.",
        "I am grateful for the opportunities to express my creativity.",
        "I am grateful for the opportunities to contribute to my community.",
        "I am grateful for the opportunities to learn from my mistakes.",
        "I am grateful for the abundance of opportunities that come my way.",

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
        "I am grateful for the smiles I share with others.",
        "I am grateful for the feeling of sunshine on my skin.",
        "I am grateful for the laughter of children.",
        "I am grateful for the joy of giving.",
        "I am grateful for the ability to find happiness within myself.",

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
        "I am grateful for the opportunity to make someone's day a little brighter.",
        "I am grateful for the feeling of helping others.",
        "I am grateful for the way kindness can transform lives.",
        "I am grateful for the ripple effect that kindness creates.",
        "I am grateful for the people who inspire me to be kinder.",

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
        "I am grateful for the sunrise, painting the sky with vibrant colors.",
        "I am grateful for the fresh start that each new day brings.",
        "I am grateful for the opportunity to learn and grow with each new day.",
        "I am grateful for the potential that lies within each new day.",
        "I am grateful for the anticipation of what each new day will bring.",

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
        "I am grateful for the opportunity to learn new skills at work.",
        "I am grateful for the chance to solve problems at work.",
        "I am grateful for the creative outlet that work provides.",
        "I am grateful for the challenges that make me a better professional.",
        "I am grateful for the opportunity to mentor and guide others at work.",

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
        "I am grateful for the challenges that push me outside of my comfort zone.",
        "I am grateful for the lessons learned during difficult times.",
        "I am grateful for the resilience I develop in the face of adversity.",
        "I am grateful for the opportunity to grow stronger and wiser through challenges.",
        "I am grateful for the perspective I gain from overcoming obstacles.",

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
        "I am grateful for the warmth of a relaxing bath.",
        "I am grateful for the soothing sounds of nature.",
        "I am grateful for the feeling of complete peace and tranquility.",
        "I am grateful for the opportunity to disconnect from technology and reconnect with myself.",
        "I am grateful for the ability to slow down and appreciate the present moment.",

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
        "I am grateful for the unconditional love I receive from my family.",
        "I am grateful for the deep connection I share with my friends.",
        "I am grateful for the joy and laughter that love brings into my life.",
        "I am grateful for the way love makes me feel valued and appreciated.",
        "I am grateful for the ability to give and receive love freely.",

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
        "I am grateful for the opportunity to express myself through my hobbies.",
        "I am grateful for the sense of community that my hobbies provide.",
        "I am grateful for the challenges that help me improve my skills.",
        "I am grateful for the relaxation and joy that my hobbies bring.",
        "I am grateful for the escape that my hobbies offer.",

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
        "I am grateful for the sense of purpose that my beliefs provide.",
        "I am grateful for the hope that my beliefs give me.",
        "I am grateful for the comfort that my beliefs offer.",
        "I am grateful for the guidance that my beliefs provide.",
        "I am grateful for the community of support I find through my beliefs.",

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
        "I am grateful for the opportunity to share my knowledge with others.",
        "I am grateful for the way lessons help me make better decisions.",
        "I am grateful for the perspective that lessons provide.",
        "I am grateful for the resilience I develop through learning from my mistakes.",
        "I am grateful for the opportunity to help others learn and grow.",

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
        "I am grateful for the ability to create a positive mindset.",
        "I am grateful for the way positive thinking helps me attract positive experiences.",
        "I am grateful for the strength and resilience that positive thinking provides.",
        "I am grateful for the ability to see challenges as opportunities for growth.",
        "I am grateful for the joy and happiness that positive thinking brings into my life.",

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
        "I am grateful for the clarity and focus that dreams provide.",
        "I am grateful for the motivation and drive that dreams instill.",
        "I am grateful for the feeling of excitement and anticipation when pursuing my dreams.",
        "I am grateful for the people who encourage me to pursue my dreams.",
        "I am grateful for the sense of purpose that dreams give me.",

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
        "I am grateful for the opportunity to reflect on my growth and progress.",
        "I am grateful for the support system that encourages my growth.",
        "I am grateful for the small steps I take towards my goals each day.",
        "I am grateful for the challenges that push me to grow and evolve.",
        "I am grateful for the feeling of accomplishment that comes with personal growth.",

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
        "I am grateful for the access to information and knowledge that technology provides.",
        "I am grateful for the ability to connect with loved ones through technology.",
        "I am grateful for the advancements in transportation technology.",
        "I am grateful for the entertainment and creative outlets that technology offers.",
        "I am grateful for the efficiency and convenience that technology brings to my daily life.",

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
        "I am grateful for the opportunity to support causes that are important to me.",
        "I am grateful for the ability to provide for my family's needs.",
        "I am grateful for the opportunities that financial freedom can provide.",
        "I am grateful for the ability to use money to create positive change in the world.",
        "I am grateful for the abundance and prosperity in my life.",

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
        "I am grateful for the beauty of a snow-covered landscape.",
        "I am grateful for the cool breeze on a hot day.",
        "I am grateful for the warmth of the sun on a cold day.",
        "I am grateful for the way weather can create a unique atmosphere and ambiance.",
        "I am grateful for the way weather can remind me of the beauty and power of nature.",

        # Animals
        "I'm grateful for the animals that share our planet.",
        "Animals bring joy and companionship to our lives.",
        "I appreciate the diversity and beauty of the animal kingdom.",
        "I'm thankful for the role animals play in our ecosystem.",
        "I love watching animals in their natural habitat.",
        "Animals teach us about love, loyalty, and survival.",
        "I'm grateful for the organizations that protect and care for animals.",
        "Animals inspire me with their strength, resilience, and beauty.",
        "I am grateful for the unconditional love of my pet.",
        "I am grateful for the beauty of a soaring bird.",
        "I am grateful for the playful nature of dolphins.",
        "I am grateful for the strength and grace of a lion.",
        "I am grateful for the quiet companionship of a cat.",
        "I am grateful for the important role that animals play in our ecosystem."
    ],
    'category': [
        # Family
        'Family', 'Family', 'Family', 'Family', 'Family',
        'Family', 'Family', 'Family', 'Family', 'Family',
        'Family', 'Family', 'Family', 'Family', 'Family',

        # Nature
        'Nature', 'Nature', 'Nature', 'Nature', 'Nature',
        'Nature', 'Nature', 'Nature', 'Nature', 'Nature',
        'Nature', 'Nature', 'Nature', 'Nature', 'Nature',

        # Friends
        'Friends', 'Friends', 'Friends', 'Friends', 'Friends',
        'Friends', 'Friends', 'Friends', 'Friends', 'Friends',
        'Friends', 'Friends', 'Friends', 'Friends', 'Friends',

        # Health
        'Health', 'Health', 'Health', 'Health', 'Health',
        'Health', 'Health', 'Health', 'Health', 'Health',
        'Health', 'Health', 'Health', 'Health', 'Health',

        # Food
        'Food', 'Food', 'Food', 'Food', 'Food',
        'Food', 'Food', 'Food', 'Food', 'Food',
        'Food', 'Food', 'Food', 'Food', 'Food',

        # Home
        'Home', 'Home', 'Home', 'Home', 'Home',
        'Home', 'Home', 'Home', 'Home', 'Home',
        'Home', 'Home', 'Home', 'Home', 'Home',

        # Pets
        'Pets', 'Pets', 'Pets', 'Pets', 'Pets',
        'Pets', 'Pets', 'Pets', 'Pets', 'Pets',
        'Pets', 'Pets', 'Pets', 'Pets', 'Pets',

        # Opportunities
        'Opportunities', 'Opportunities', 'Opportunities', 'Opportunities', 'Opportunities',
        'Opportunities', 'Opportunities', 'Opportunities', 'Opportunities', 'Opportunities',
        'Opportunities', 'Opportunities', 'Opportunities', 'Opportunities', 'Opportunities',

        # Happiness
        'Happiness', 'Happiness', 'Happiness', 'Happiness', 'Happiness',
        'Happiness', 'Happiness', 'Happiness', 'Happiness', 'Happiness',
        'Happiness', 'Happiness', 'Happiness', 'Happiness', 'Happiness',

        # Kindness
        'Kindness', 'Kindness', 'Kindness', 'Kindness', 'Kindness',
        'Kindness', 'Kindness', 'Kindness', 'Kindness', 'Kindness',
        'Kindness', 'Kindness', 'Kindness', 'Kindness', 'Kindness',

        # New Day
        'New Day', 'New Day', 'New Day', 'New Day', 'New Day',
        'New Day', 'New Day', 'New Day', 'New Day', 'New Day',
        'New Day', 'New Day', 'New Day', 'New Day', 'New Day',

        # Work
        'Work', 'Work', 'Work', 'Work', 'Work',
        'Work', 'Work', 'Work', 'Work', 'Work',
        'Work', 'Work', 'Work', 'Work', 'Work',

        # Challenges
        'Challenges', 'Challenges', 'Challenges', 'Challenges', 'Challenges',
        'Challenges', 'Challenges', 'Challenges', 'Challenges', 'Challenges',
        'Challenges', 'Challenges', 'Challenges', 'Challenges', 'Challenges',

        # Relaxation
        'Relaxation', 'Relaxation', 'Relaxation', 'Relaxation', 'Relaxation',
        'Relaxation', 'Relaxation', 'Relaxation', 'Relaxation', 'Relaxation',
        'Relaxation', 'Relaxation', 'Relaxation', 'Relaxation', 'Relaxation',

        # Love
        'Love', 'Love', 'Love', 'Love', 'Love',
        'Love', 'Love', 'Love', 'Love', 'Love',
        'Love', 'Love', 'Love', 'Love', 'Love',

        # Hobbies
        'Hobbies', 'Hobbies', 'Hobbies', 'Hobbies', 'Hobbies',
        'Hobbies', 'Hobbies', 'Hobbies', 'Hobbies', 'Hobbies',
        'Hobbies', 'Hobbies', 'Hobbies', 'Hobbies', 'Hobbies',

        # Belief
        'Belief', 'Belief', 'Belief', 'Belief', 'Belief',
        'Belief', 'Belief', 'Belief', 'Belief', 'Belief',
        'Belief', 'Belief', 'Belief', 'Belief', 'Belief',

        # Lessons
        'Lessons', 'Lessons', 'Lessons', 'Lessons', 'Lessons',
        'Lessons', 'Lessons', 'Lessons', 'Lessons', 'Lessons',
        'Lessons', 'Lessons', 'Lessons', 'Lessons', 'Lessons',

        # Positive Thinking
        'Positive Thinking', 'Positive Thinking', 'Positive Thinking', 'Positive Thinking', 'Positive Thinking',
        'Positive Thinking', 'Positive Thinking', 'Positive Thinking', 'Positive Thinking', 'Positive Thinking',
        'Positive Thinking', 'Positive Thinking', 'Positive Thinking', 'Positive Thinking', 'Positive Thinking',

        # Dreams
        'Dreams', 'Dreams', 'Dreams', 'Dreams', 'Dreams',
        'Dreams', 'Dreams', 'Dreams', 'Dreams', 'Dreams',
        'Dreams', 'Dreams', 'Dreams', 'Dreams', 'Dreams',

        # Growth
        'Growth', 'Growth', 'Growth', 'Growth', 'Growth',
        'Growth', 'Growth', 'Growth', 'Growth', 'Growth',
        'Growth', 'Growth', 'Growth', 'Growth', 'Growth',

        # Technology
        'Technology', 'Technology', 'Technology', 'Technology', 'Technology',
        'Technology', 'Technology', 'Technology', 'Technology', 'Technology',
        'Technology', 'Technology', 'Technology', 'Technology', 'Technology',

        # Money
        'Money', 'Money', 'Money', 'Money', 'Money',
        'Money', 'Money', 'Money', 'Money', 'Money',
        'Money', 'Money', 'Money', 'Money', 'Money',

        # Weather
        'Weather', 'Weather', 'Weather', 'Weather', 'Weather',
        'Weather', 'Weather', 'Weather', 'Weather', 'Weather',
        'Weather', 'Weather', 'Weather', 'Weather', 'Weather',

        # Animals
        'Animals', 'Animals', 'Animals', 'Animals', 'Animals',
        'Animals', 'Animals', 'Animals', 'Animals', 'Animals',
        'Animals', 'Animals', 'Animals', 'Animals',
    ]
}
print("Length of 'text' list:", len(data['text']))
print("Length of 'category' list:", len(data['category']))

category_counts = Counter(data['category'])
print("Category counts:")
for category, count in category_counts.items():
    print(f"{category}: {count}")

print("\nCategories with unexpected counts:")
for category, count in category_counts.items():
    if count != 15:
        print(f"{category}: {count}")

for category, count in category_counts.items():
    if count != 15:
        print(f"\nEntries for {category}:")
        for i, (text, cat) in enumerate(zip(data['text'], data['category'])):
            if cat == category:
                print(f"{i}: {text}")

if len(data['text']) != len(data['category']):
    print("Error: 'text' and 'category' lists have different lengths.")
    print("'text' length:", len(data['text']))
    print("'category' length:", len(data['category']))
    # Removed exit(1) to allow script to continue
print("\nChecking for mismatches between text and category:")
for i, (text, category) in enumerate(zip(data['text'], data['category'])):
    if i >= len(data['text']):
        print(f"Extra category at index {i}: {category}")
    elif i >= len(data['category']):
        print(f"Extra text at index {i}: {text}")
    elif data['category'][i] != category:
        print(f"Mismatch at index {i}:")
        print(f"Text: {text}")
        print(f"Category: {category}")
        print(f"Expected category: {data['category'][i]}")

if len(data['category']) > len(data['text']):
    print(f"Extra category at the end: {data['category'][-1]}")
elif len(data['text']) > len(data['category']):
    print(f"Extra text at the end: {data['text'][-1]}")

# Create DataFrame
df = pd.DataFrame(data)

# Clean Text
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text, re.I|re.A)
    text = text.lower()
    return text

df['cleaned_text'] = df['text'].apply(clean_text)

# Split data
X_train, X_test, y_train, y_test = train_test_split(df['cleaned_text'], df['category'], test_size=0.2, random_state=42)

# Create Pipeline
text_classifier = Pipeline([
    ('tfidf', TfidfVectorizer(stop_words='english')),
    ('classifier', MultinomialNB())
])

# Train model
text_classifier.fit(X_train, y_train)

# Evaluate model
predictions = text_classifier.predict(X_test)

print(classification_report(y_test, predictions))
print("Accuracy:", accuracy_score(y_test, predictions))

# Save model
joblib.dump(text_classifier, 'gratitude_model.joblib')

print("Model trained and saved as gratitude_model.joblib")