# 🌍 Wherever Next – AI Travel Recommendation System

An AI-powered travel recommendation web application built with **Streamlit**, **SQLite**, and **Scikit-learn**.

The system recommends travel destinations based on:

- Destination Type
- Travel Season
- Budget
- Trip Duration

It uses **TF-IDF Vectorization** and **Cosine Similarity** to recommend destinations that best match user preferences.

---

## Features

- User Registration & Login
- Secure Password Hashing (bcrypt)
- SQLite Database
- AI Recommendation Engine
- Destination Search
- Dashboard Analytics
- Responsive Streamlit Interface
- Streamlit Community Cloud Ready

---

## Technology Stack

| Component | Technology |
|----------|------------|
| Frontend | Streamlit |
| Database | SQLite |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly |
| Authentication | bcrypt |

---

## Project Structure

travel_recommendation/

```
app.py
auth.py
database.py
requirements.txt
README.md

data/
    destinations.csv

database/
    users.db

models/
    recommender.py

pages/
    login.py
    register.py
    home.py
    recommendation.py
    search.py
    dashboard.py

utils/
    preprocessing.py
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/travel_recommendation.git
```

Go to project folder

```bash
cd travel_recommendation
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

## AI Recommendation Algorithm

The recommendation engine uses:

- TF-IDF Vectorizer
- Cosine Similarity
- Budget Matching Score
- Weighted Ranking Algorithm

Final Score

```
70% Text Similarity
30% Budget Similarity
```

---

## Future Improvements

- Hotel Recommendations
- Flight Integration
- Weather API
- Google Maps Integration
- User Reviews
- Image Gallery
- Favorites
- Booking Integration

---

## Author

Developed using Python, Streamlit and Machine Learning.
