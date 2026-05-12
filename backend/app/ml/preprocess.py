import joblib
import pandas as pd
from loguru import logger
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler


# =========================================
# PRODUCTION FEATURE CONTRACT
# =========================================

NUMERICAL_FEATURES = [
    "GrLivArea",
    "BedroomAbvGr",
    "FullBath",
    "OverallQual",
    "house_age",
    "is_remodeled",
    "has_garage",
    "has_pool",
    "floor_number",
    "total_sf",
    "overall_quality_score",
]

CATEGORICAL_FEATURES = [
    "Neighborhood",
]


def create_engineered_features(
    df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create production-safe engineered features.
    """

    logger.info(
        "Creating engineered features"
    )

    df = df.copy()

    # =============================
    # TOTAL AREA FEATURE
    # =============================

    df["total_sf"] = (
        df["GrLivArea"]
    )

    # =============================
    # QUALITY SCORE
    # =============================

    df["overall_quality_score"] = (
        df["OverallQual"] * 5
    )

    logger.success(
        "Engineered features created"
    )

    return df


def create_preprocessor():
    """
    Create ML preprocessing pipeline.
    """

    logger.info(
        "Creating preprocessing pipeline"
    )

    # =============================
    # NUMERICAL PIPELINE
    # =============================

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            ),
            (
                "scaler",
                StandardScaler(),
            ),
        ]
    )

    # =============================
    # CATEGORICAL PIPELINE
    # =============================

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
                    handle_unknown="ignore"
                ),
            ),
        ]
    )

    # =============================
    # COLUMN TRANSFORMER
    # =============================

    preprocessor = (
        ColumnTransformer(
            transformers=[
                (
                    "num",
                    numerical_pipeline,
                    NUMERICAL_FEATURES,
                ),
                (
                    "cat",
                    categorical_pipeline,
                    CATEGORICAL_FEATURES,
                ),
            ]
        )
    )

    logger.success(
        "Preprocessing pipeline created"
    )

    return preprocessor


def save_preprocessor(
    preprocessor,
    save_path: str,
):
    """
    Save fitted preprocessor.
    """

    logger.info(
        f"Saving preprocessor to "
        f"{save_path}"
    )

    joblib.dump(
        preprocessor,
        save_path,
    )

    logger.success(
        "Preprocessor saved successfully"
    )


def load_preprocessor(
    load_path: str,
):
    """
    Load fitted preprocessor.
    """

    logger.info(
        f"Loading preprocessor from "
        f"{load_path}"
    )

    preprocessor = joblib.load(
        load_path
    )

    logger.success(
        "Preprocessor loaded successfully"
    )

    return preprocessor