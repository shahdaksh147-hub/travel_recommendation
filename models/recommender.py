import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


TEXT_WEIGHT = 0.70
BUDGET_WEIGHT = 0.30


class TravelRecommender:

    def __init__(self, dataframe):

        self.df = dataframe.copy().reset_index(drop=True)

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.matrix = self.vectorizer.fit_transform(
            self.df["combined_features"]
        )

    #####################################################
    # Budget Similarity
    #####################################################

    def budget_similarity(
        self,
        budget_column,
        user_budget
    ):

        difference = (
            budget_column - user_budget
        ).abs()

        similarity = 1 - (
            difference / user_budget
        )

        similarity = similarity.clip(
            lower=0,
            upper=1
        )

        return similarity

    #####################################################
    # Recommendation
    #####################################################

    def recommend(

        self,

        destination_type,

        season,

        budget,

        duration,

        top_n=5

    ):

        duration = max(
            int(duration),
            1
        )

        daily_budget = budget / duration

        query = (

            destination_type + " "

            + destination_type + " "

            + season + " "

            + season

        ).lower()

        query_vector = self.vectorizer.transform(
            [query]
        )

        text_score = cosine_similarity(

            query_vector,

            self.matrix

        ).flatten()

        budget_score = self.budget_similarity(

            self.df["Budget"],

            daily_budget

        )

        final_score = (

            TEXT_WEIGHT * text_score

            +

            BUDGET_WEIGHT * budget_score

        )

        results = self.df.copy()

        results["Match Score"] = np.round(
            final_score * 100,
            1
        )

        results["Estimated Budget"] = (

            results["Budget"]

            *

            duration

        ).astype(int)

        results = results.sort_values(

            by="Match Score",

            ascending=False

        ).head(top_n)

        return results[

            [

                "Destination_Name",

                "State",

                "Country",

                "Category",

                "Best_Season",

                "Rating",

                "Estimated Budget",

                "Match Score",

                "Description"

            ]

        ].reset_index(drop=True)
