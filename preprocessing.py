"""
utils/preprocessing.py
=======================
Loads, cleans, and engineers features from the destinations dataset.

This module is framework-agnostic (no Streamlit imports) so it can be
tested independently. Streamlit-specific caching (st.cache_data) is
applied where this module is called from app.py / pages, not here.
"""

import os
import pandas as pd
from typing import List, Tuple, Dict, Any


DEFAULT_CSV_PATH = os.path.join("data", "destinations.csv")

REQUIRED_COLUMNS = [
    "Destination_Name", "State", "Country", "Category",
    "Budget", "Best_Season", "Description", "Rating",
]


class DataPreprocessor:
    """
    Loads and prepares the travel destinations dataset for both the
    search/browse pages and the recommendation engine.
    """

    def __init__(self, csv_path: str = DEFAULT_CSV_PATH) -> None:
        """
        Args:
            csv_path: Path to the destinations CSV file.
        """
        self.csv_path = csv_path

    # ------------------------------------------------------------------
    # Loading & cleaning
    # ------------------------------------------------------------------

    def load_data(self) -> pd.DataFrame:
        """
        Load the destinations CSV, validate its schema, and clean it.

        Returns:
            A cleaned pandas DataFrame with an added 'combined_features'
            column ready for TF-IDF vectorization.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
            ValueError: If required columns are missing from the CSV.
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(
                f"Dataset not found at '{self.csv_path}'. "
                "Make sure data/destinations.csv exists."
            )

        df = pd.read_csv(self.csv_path)
        self._validate_columns(df)
        df = self._clean_data(df)
        df = self.engineer_features(df)
        return df

    def _validate_columns(self, df: pd.DataFrame) -> None:
        """Ensure the CSV has all columns the app depends on."""
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"Dataset is missing required columns: {missing}")

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean raw data: trim whitespace, enforce types, drop bad rows.

        Args:
            df: Raw DataFrame straight from pd.read_csv.

        Returns:
            A cleaned copy of the DataFrame.
        """
        df = df.copy()

        # Trim whitespace on all text/object columns.
        text_columns = df.select_dtypes(include="object").columns
        for col in text_columns:
            df[col] = df[col].astype(str).str.strip()

        # Enforce numeric types; coerce errors to NaN so they can be dropped.
        df["Budget"] = pd.to_numeric(df["Budget"], errors="coerce")
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

        # Drop rows with missing critical data, then remove exact duplicates.
        df = df.dropna(subset=REQUIRED_COLUMNS)
        df = df.drop_duplicates(subset=["Destination_Name", "State", "Country"])

        # Reset index after filtering so downstream positional indexing
        # (used by the cosine similarity matrix) stays aligned.
        df = df.reset_index(drop=True)
        return df

    # ------------------------------------------------------------------
    # Feature engineering
    # ------------------------------------------------------------------

    def engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Build a combined text column used as input to the TF-IDF vectorizer.

        The category and season are repeated to give them slightly more
        weight than the free-text description, since they map directly
        to the structured filters the user selects in the UI.

        Args:
            df: Cleaned DataFrame.

        Returns:
            DataFrame with an added 'combined_features' column.
        """
        df = df.copy()
        df["combined_features"] = (
            (df["Category"] + " ") * 2
            + (df["Best_Season"] + " ") * 2
            + df["Description"]
        ).str.lower()
        return df

    # ------------------------------------------------------------------
    # Convenience accessors for the UI layer
    # ------------------------------------------------------------------

    def get_categories(self, df: pd.DataFrame) -> List[str]:
        """Return a sorted list of unique destination categories."""
        return sorted(df["Category"].unique().tolist())

    def get_seasons(self, df: pd.DataFrame) -> List[str]:
        """Return a sorted list of unique best-season values."""
        return sorted(df["Best_Season"].unique().tolist())

    def get_budget_bounds(self, df: pd.DataFrame) -> Tuple[int, int]:
        """Return (min_budget, max_budget) rounded to whole numbers."""
        return int(df["Budget"].min()), int(df["Budget"].max())

    def get_dashboard_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Compute summary statistics used on the Dashboard page.

        Returns:
            A dictionary with total destination count, category count,
            average rating, category distribution, and budget distribution
            (binned into readable ranges).
        """
        budget_bins = [0, 300, 700, 1500, float("inf")]
        budget_labels = ["Budget (<$300)", "Mid-range ($300-700)", "Premium ($700-1500)", "Luxury ($1500+)"]
        budget_band = pd.cut(df["Budget"], bins=budget_bins, labels=budget_labels)

        return {
            "total_destinations": len(df),
            "total_categories": df["Category"].nunique(),
            "average_rating": round(df["Rating"].mean(), 2),
            "category_counts": df["Category"].value_counts().to_dict(),
            "budget_distribution": budget_band.value_counts().reindex(budget_labels).to_dict(),
        }


def load_destinations(csv_path: str = DEFAULT_CSV_PATH) -> pd.DataFrame:
    """
    Convenience function for callers that just want a ready DataFrame
    without instantiating DataPreprocessor directly.

    Args:
        csv_path: Path to the destinations CSV file.

    Returns:
        A cleaned, feature-engineered DataFrame.
    """
    return DataPreprocessor(csv_path).load_data()
