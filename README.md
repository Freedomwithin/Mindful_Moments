# Mindful Moments

The Gratitude Journal is an innovative mobile application designed to enhance users' well-being by encouraging the practice of daily gratitude. At its core, the app utilizes advanced machine learning techniques to automatically categorize users' gratitude entries, providing insightful analytics about the areas of life for which they are most grateful.

## Key Features

- **Daily Gratitude Entries:** Users can easily input their daily gratitude statements through a clean, intuitive interface.

- **Automatic Categorization:** Leveraging machine learning, the app automatically categorizes each gratitude entry into predefined categories such as Family, Nature, Friends, Health, Food, Home, Pets, Opportunities, Happiness, Kindness, Work, Challenges, Relaxation, Love, Hobbies, Belief, Lessons, Positive Thinking, and Dreams.

- **Personalized Insights:** The app provides users with personalized analytics and visualizations of their gratitude patterns over time.

- **Reminder System:** Users can set customizable reminders to encourage consistent gratitude practice.

- **Offline Functionality:** The app works offline, syncing data when an internet connection is available.

- **Dark Mode Toggle:** Users can switch to dark mode for a more comfortable viewing experience in low-light environments.

## Tech Stack

### Frontend

- **React Native** for cross-platform mobile development
- **Redux** for state management
- **React Navigation** for routing and navigation

### Backend

- **Node.js** with **Express.js** for API development
- **MongoDB** for database management
- **Mongoose** as an ODM (Object Data Modeling) library

### Machine Learning

- **Python** for model development and training
- **scikit-learn** for implementing machine learning algorithms
- **Flask** for creating a lightweight API to serve the ML model

### DevOps

- **Docker** for containerization
- **GitHub Actions** for CI/CD pipeline
- **Heroku** for backend and ML model deployment

## Machine Learning Implementation

The core of the app's intelligent features is its machine learning model for text classification. Here's a breakdown of the ML implementation:

1. **Data Preparation:** We curated a diverse dataset of gratitude statements manually categorized into 20 different categories.

2. **Text Preprocessing:** Implemented using Python's NLTK library for tokenization, stopword removal, and lemmatization.

3. **Feature Extraction:** Utilized TF-IDF (Term Frequency-Inverse Document Frequency) vectorization to convert text data into numerical features.

4. **Model Selection:** Experimented with multiple algorithms including Multinomial Naive Bayes, Logistic Regression, and Linear Support Vector Machines.

5. **Hyperparameter Tuning:** Employed GridSearchCV for finding the optimal hyperparameters for each model.

6. **Model Evaluation:** Used metrics such as accuracy, precision, recall, and F1-score to assess model performance.

7. **Model Deployment:** The best-performing model (typically Logistic Regression or LinearSVC) is serialized using joblib and deployed as a Flask API.

8. **Real-time Prediction:** When a user submits a gratitude entry, the app sends the text to the ML API, which returns the predicted category in real-time.

This Gratitude Journal app represents a unique blend of user-centric design and cutting-edge machine learning technology aimed at promoting mental well-being through the power of gratitude.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Freedomwithin/Mindful_Moments
   cd mindful-moments

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate 
   # On Windows,
   # use venv\Scripts\activate

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
4. Set the Flask application
   ```bash
   export FLASK_APP=app.py  # On Windows, use: set FLASK_APP=app.py
5. Set up database:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
6. Run the application
   ```bash
   flask run
8. Open your web browser and navigate to `http://localhost:5000`

## Deployment on Render

1. Create a new Web Service on Render and connect your GitHub repository.

2. Use the following settings:
- Environment: Python 3
- Build Command: `pip install --upgrade pip && pip install -r requirements.txt`
- Start Command: `gunicorn wsgi:app`

3. Add the following environment variables:
- `PYTHON_VERSION`: 3.9.0 (or your preferred Python version)
- `SECRET_KEY`: Your secret key for Flask
- `DATABASE_URL`: Your database URL (if using a different database)

4. Click "Create Web Service"

5. Render will automatically deploy your application. Once the deployment is complete, you can access your app using the provided URL.

## Usage

1. Register a new account or log in to an existing one.
2. On the main page, you can add new gratitude entries, view past entries, and see your mood trend.
3. Use the dark mode toggle in the top right corner to switch between light and dark themes.

## Machine Learning Implementation

1. Our text classification model involves:
2. Data Preparation
3. Text Preprocessing (using NLTK)
4. Feature Extraction (TF-IDF vectorization)
5. Model Selection and Hyperparameter Tuning
6. Model evaluation
7. Deployment as a Flask API

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Support

If you find this app helpful, consider [making a donation](https://paypal.me/FreedomwithinMD?country.x=US&locale.x=en_US).
