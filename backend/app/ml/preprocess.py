from typing import Tuple

import joblib
import pandas as pd
from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def build_preprocessor(
    df: pd.DataFrame,
) -> Tuple[ColumnTransformer, list]:
    """
    Build preprocessing pipeline for numerical and categorical features.
    """

    logger.info("Building preprocessing pipeline")

    numeric_features = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_features = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    logger.info(
        f"Detected {len(numeric_features)} numeric features"
    )

    logger.info(
        f"Detected {len(categorical_features)} categorical features"
    )

    # =========================
    # NUMERICAL PIPELINE
    # =========================

    numeric_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median"),
            ),
        ]
    )

    # =========================
    # CATEGORICAL PIPELINE
    # =========================

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="constant",
                    fill_value="None",
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                ),
            ),
        ]
    )

    # =========================
    # COMBINED PREPROCESSOR
    # =========================

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "num",
                numeric_pipeline,
                numeric_features,
            ),
            (
                "cat",
                categorical_pipeline,
                categorical_features,
            ),
        ]
    )

    logger.success(
        "Preprocessing pipeline built successfully"
    )

    return (
        preprocessor,
        numeric_features + categorical_features,
    )


def save_preprocessor(
    preprocessor: ColumnTransformer,
    path: str,
) -> None:
    """
    Save fitted preprocessing pipeline.
    """

    logger.info(f"Saving preprocessor to {path}")

    joblib.dump(preprocessor, path)

    logger.success("Preprocessor saved successfully")


def load_preprocessor(
    path: str,
) -> ColumnTransformer:
    """
    Load saved preprocessing pipeline.
    """

    logger.info(f"Loading preprocessor from {path}")

    preprocessor = joblib.load(path)

    logger.success("Preprocessor loaded successfully")

    return preprocessor