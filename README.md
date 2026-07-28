# ✈️ Wherever Next — AI-Powered Travel Recommendation System

A production-quality, **Python-only** travel recommendation system built with
Streamlit, SQLite, and a content-based (TF-IDF + cosine similarity)
recommendation engine.

No JavaScript, React, or any frontend framework is used — the entire UI is
built and served with Streamlit.

---

## Features

- **User Authentication** — registration, login, logout, session management,
  bcrypt password hashing, duplicate-email prevention.
- **Home Page** — personalized welcome, live dataset snapshot, quick
  navigation to every feature.
- **AI Recommendation Engine** — TF-IDF + cosine similarity content-based
  matching, blended with numeric budget-closeness scoring, ranked by a
  single Match Score.
- **Search** — find destinations by name and/or category.
- **Dashboard** — dataset-wide stats and interactive Plotly charts.
- **110-destination dataset** across 6 categories (Beach, Hill Station, City,
  Adventure, Wildlife, Religious), spanning both Indian and international
  destinations.

---

## Tech Stack

| Layer            | Technology                     |
|-------------------|--------------------------------|
| Frontend          | Streamlit                     |
| Database          | SQLite                        |
| Data handling     | Pandas, NumPy                 |
| ML / Recommender  | Scikit-learn (TF-IDF, cosine similarity) |
| Password security | bcrypt                         |
| Charts            | Plotly                        |

---

## Project Structure

```
travel_recommendation/
│── app.py                     # Main entry point — session state + navigation
│── database.py                # SQLite connection manager + users table
│── auth.py                    # Registration/login logic, password hashing
│── requirements.txt
│── README.md
│
├── data/
│     └── destinations.csv     # 110-destination dataset
│
├── models/
│     └── recommender.py       # TF-IDF + cosine similarity recommender
│
├── utils/
│     └── preprocessing.py     # Data loading, cleaning, feature engineering
│
├── pages/
│     ├── Login.py
│     ├── Register.py
│     ├── Home.py
│     ├── Recommendation.py
│     ├── Search.py
│     └── Dashboard.py
│
└── database/
      └── users.db             # Created automatically on first run
```

---

## Setup & Installation

**1. Clone or download the project, then navigate into it:**
```bash
cd travel_recommendation
```

**2. (Recommended) Create a virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Run the app:**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.
The SQLite database (`database/users.db`) and its `users` table are created
automatically the first time the app runs — no manual setup required.

---

## How the Recommendation Engine Works

1. Every destination's `Category`, `Best_Season`, and `Description` are
   combined into a single text field (`combined_features`), with category
   and season repeated to weight them more heavily than free text.
2. A `TfidfVectorizer` (scikit-learn) fits on this text across all 110
   destinations.
3. When a user submits preferences, their selected type + season are turned
   into a query string in the same "shape," vectorized with the same fitted
   vocabulary, and compared to every destination via **cosine similarity**.
4. Separately, the `Budget` column is treated as **cost per day**. The
   user's *total* budget divided by trip duration gives an implied daily
   budget, which is compared numerically against each destination's daily
   cost — closer prices score higher.
5. The final **Match Score** blends both signals (60% text similarity, 40%
   budget closeness), and the top 5 destinations are returned with an
   **Estimated Budget** for the whole trip (`daily cost × duration`).

This means all four user inputs — destination type, season, budget, *and*
trip duration — genuinely influence the ranking, rather than duration being
collected but unused.

---

## Security Notes

- Passwords are hashed with **bcrypt** (salted, industry-standard) before
  being stored — plaintext passwords are never persisted.
- Duplicate email registration is blocked at the database layer.
- Session state (`st.session_state`) gates access: unauthenticated users can
  only ever see the Login/Register pages — the rest of the app's navigation
  entries don't exist for them until they log in.

---

## Notes for Further Development

- Swap `data/destinations.csv` for a larger or live dataset (e.g. a travel
  API) without touching `models/recommender.py` — it only depends on the
  `combined_features` column existing.
- The TF-IDF/budget blend weights (`TEXT_SIMILARITY_WEIGHT`,
  `BUDGET_SIMILARITY_WEIGHT` in `models/recommender.py`) are easy to tune or
  expose as an "advanced settings" UI control.
- `utils/preprocessing.py` and `auth.py` have no Streamlit imports, so both
  can be unit tested independently of the UI.
