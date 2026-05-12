import numpy as np
import pandas as pd
from loguru import logger


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create engineered real estate features for valuation modeling.
    """

    logger.info("Starting feature engineering pipeline")

    engineered_df = df.copy()

    # =========================
    # TARGET LOG TRANSFORM
    # =========================

    if "SalePrice" in engineered_df.columns:
        logger.info("Applying log transform to SalePrice")

        engineered_df["SalePrice"] = np.log1p(
            engineered_df["SalePrice"]
        )

    # =========================
    # HOUSE AGE FEATURES
    # =========================

    logger.info("Creating age-based features")

    engineered_df["house_age"] = (
        engineered_df["YrSold"]
        - engineered_df["YearBuilt"]
    )

    engineered_df["remod_age"] = (
        engineered_df["YrSold"]
        - engineered_df["YearRemodAdd"]
    )

    engineered_df["is_remodeled"] = (
        engineered_df["YearBuilt"]
        != engineered_df["YearRemodAdd"]
    ).astype(int)

    # =========================
    # TOTAL AREA FEATURES
    # =========================

    logger.info("Creating total square footage feature")

    engineered_df["total_sf"] = (
        engineered_df["TotalBsmtSF"]
        + engineered_df["1stFlrSF"]
        + engineered_df["2ndFlrSF"]
    )

    # =========================
    # QUALITY SCORE
    # =========================

    logger.info("Creating overall quality score")

    engineered_df["overall_quality_score"] = (
        engineered_df["OverallQual"]
        * engineered_df["OverallCond"]
    )

    # =========================
    # PREMIUM FEATURE FLAGS
    # =========================

    logger.info("Creating premium feature flags")

    engineered_df["has_pool"] = (
        engineered_df["PoolArea"] > 0
    ).astype(int)

    engineered_df["has_garage"] = (
        engineered_df["GarageArea"] > 0
    ).astype(int)

    engineered_df["has_basement"] = (
        engineered_df["TotalBsmtSF"] > 0
    ).astype(int)

    logger.success(
        "Feature engineering completed successfully"
    )

    return engineered_df


def reverse_log_transform(
    predictions: np.ndarray,
) -> np.ndarray:
    """
    Reverse log-transformed predictions back to price scale.
    """

    logger.info("Reversing log transformation")

    return np.expm1(predictions)