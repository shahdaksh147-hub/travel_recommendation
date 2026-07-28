import os
import pandas as pd


class DataPreprocessor:

    REQUIRED_COLUMNS = [
        "Destination_Name",
        "State",
        "Country",
        "Category",
        "Budget",
        "Best_Season",
        "Description",
        "Rating",
    ]

    def __init__(self):

        base_dir = os.path.dirname(os.path.abspath(__file__))

        project_root = os.path.dirname(base_dir)

        self.csv_path = os.path.join(
            project_root,
            "data",
            "destinations.csv"
        )

    #########################################################
    # Load Dataset
    #########################################################

    def load_data(self):

        if not os.path.exists(self.csv_path):

            raise FileNotFoundError(
                f"Dataset not found:\n{self.csv_path}"
            )

        df = pd.read_csv(self.csv_path)

        self.validate(df)

        df = self.clean(df)

        df = self.engineer_features(df)

        return df

    #########################################################
    # Validation
    #########################################################

    def validate(self, df):

        missing = []

        for col in self.REQUIRED_COLUMNS:

            if col not in df.columns:

                missing.append(col)

        if len(missing):

            raise ValueError(
                "Missing Columns : "
                + ", ".join(missing)
            )

    #########################################################
    # Cleaning
    #########################################################

    def clean(self, df):

        df = df.copy()

        object_columns = df.select_dtypes(include="object").columns

        for col in object_columns:

            df[col] = df[col].astype(str).str.strip()

        df["Budget"] = pd.to_numeric(
            df["Budget"],
            errors="coerce"
        )

        df["Rating"] = pd.to_numeric(
            df["Rating"],
            errors="coerce"
        )

        df = df.dropna()

        df = df.drop_duplicates()

        df.reset_index(drop=True, inplace=True)

        return df

    #########################################################
    # Feature Engineering
    #########################################################

    def engineer_features(self, df):

        df = df.copy()

        df["combined_features"] = (

            df["Category"] + " "

            + df["Category"] + " "

            + df["Best_Season"] + " "

            + df["Best_Season"] + " "

            + df["Description"]

        ).str.lower()

        return df

    #########################################################
    # Dashboard Stats
    #########################################################

    def dashboard_stats(self, df):

        budget_bins = [
            0,
            300,
            700,
            1500,
            999999
        ]

        labels = [
            "Budget",
            "Mid",
            "Premium",
            "Luxury"
        ]

        budget_distribution = pd.cut(
            df["Budget"],
            bins=budget_bins,
            labels=labels
        ).value_counts().to_dict()

        return {

            "total_destinations": len(df),

            "categories": df["Category"].nunique(),

            "countries": df["Country"].nunique(),

            "average_rating": round(
                df["Rating"].mean(),
                2
            ),

            "category_counts":
                df["Category"]
                .value_counts()
                .to_dict(),

            "budget_distribution":
                budget_distribution

        }


#########################################################
# Convenience Function
#########################################################

def load_destinations():

    return DataPreprocessor().load_data()
