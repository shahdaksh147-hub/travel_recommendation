"""
models/recommender.py
======================
Content-based travel recommendation engine.

Uses:
    - TfidfVectorizer to turn each destination's combined text
      (category + season + description) into a vector.
    - Cosine similarity to compare a user's preference "query" against
      every destination's vector.
    - A numeric budget-closeness score, blended with the text similarity,
      so numeric fields (budget, duration) meaningfully affect ranking
      alongside the free-text fields.

This module has no Streamlit imports and only depends on the DataFrame
it's given, so it can be unit tested independently of the UI.
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional


# Relative weight given to text similarity vs. numeric budget closeness
# when computing the final match score.
TEXT_SIMILARITY_WEIGHT = 0.6
BUDGET_SIMILARITY_WEIGHT = 0.4


class TravelRecommender:
    """
    Content-based recommender that ranks destinations against a user's
    stated preferences (destination type, season, budget, trip duration).
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Fit the TF-IDF vectorizer on the destinations dataset.

        Args:
            df: A cleaned DataFrame (from utils.preprocessing) that
                already contains a 'combined_features' text column.
        """
        if "combined_features" not in df.columns:
            raise ValueError(
                "DataFrame must contain a 'combined_features' column. "
                "Did you run it through DataPreprocessor first?"
            )

        self.df = df.reset_index(drop=True)
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["combined_features"])

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_query_text(self, destination_type: str, season: str) -> str:
        """
        Build the free-text query representing the user's preferences,
        in the same "shape" as the combined_features column so TF-IDF
        can compare them meaningfully.

        Args:
            destination_type: Selected category (e.g. "Beach").
            season: Selected best season (e.g. "Summer").

        Returns:
            A lowercase text string ready for vectorization.
        """
        return f"{destination_type} {destination_type} {season} {season}".lower()

    def _budget_similarity(self, daily_budget_series: pd.Series, implied_daily_budget: float) -> pd.Series:
        """
        Compute a 0-1 closeness score between each destination's daily
        cost and the user's implied daily budget.

        A destination priced exactly at the user's budget scores 1.0;
        the score decays the further away the price is, reaching 0
        once the difference is as large as the budget itself.

        Args:
            daily_budget_series: The 'Budget' column (per-day cost).
            implied_daily_budget: user_total_budget / trip_duration_days.

        Returns:
            A pandas Series of similarity scores between 0 and 1.
        """
        if implied_daily_budget <= 0:
            return pd.Series(0.0, index=daily_budget_series.index)

        relative_diff = (daily_budget_series - implied_daily_budget).abs() / implied_daily_budget
        similarity = 1 - relative_diff
        return similarity.clip(lower=0, upper=1)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def recommend(
        self,
        destination_type: str,
        season: str,
        budget: float,
        trip_duration_days: int,
        top_n: int = 5,
    ) -> pd.DataFrame:
        """
        Recommend the top-N destinations matching the user's preferences.

        Args:
            destination_type: Preferred category (Beach, Hill Station, etc.)
            season: Preferred travel season (Summer, Winter, Monsoon).
            budget: The user's TOTAL budget for the whole trip.
            trip_duration_days: Length of the trip in days.
            top_n: Number of recommendations to return (default 5).

        Returns:
            A DataFrame with columns: Destination_Name, State, Country,
            Category, Match_Score, Estimated_Budget, Best_Season,
            Description, Rating — sorted by Match_Score descending.
        """
        trip_duration_days = max(1, int(trip_duration_days))
        implied_daily_budget = budget / trip_duration_days

        # --- Text similarity (category + season vs. description text) ---
        query_text = self._build_query_text(destination_type, season)
        query_vector = self.vectorizer.transform([query_text])
        text_scores = cosine_similarity(query_vector, self.tfidf_matrix).flatten()

        # --- Numeric budget closeness ---
        budget_scores = self._budget_similarity(self.df["Budget"], implied_daily_budget)

        # --- Blend into a final match score (0-100 scale) ---
        combined = (
            TEXT_SIMILARITY_WEIGHT * text_scores
            + BUDGET_SIMILARITY_WEIGHT * budget_scores.to_numpy()
        )

        results = self.df.copy()
        results["Match_Score"] = np.round(combined * 100, 1)
        results["Estimated_Budget"] = np.round(self.df["Budget"] * trip_duration_days, 0).astype(int)

        results = results.sort_values("Match_Score", ascending=False).head(top_n)

        display_columns = [
            "Destination_Name", "State", "Country", "Category",
            "Match_Score", "Estimated_Budget", "Best_Season",
            "Description", "Rating",
        ]
        return results[display_columns].reset_index(drop=True)


def get_recommender(df: pd.DataFrame) -> TravelRecommender:
    """
    Convenience factory function for building a TravelRecommender.

    Args:
        df: A cleaned, feature-engineered destinations DataFrame.

    Returns:
        A ready-to-use TravelRecommender instance.
    """
    return TravelRecommender(df)
