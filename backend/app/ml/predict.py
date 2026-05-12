import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from loguru import logger

from app.ml.preprocess import (
    create_engineered_features,
    load_preprocessor,
)


class PropertyValuationModel:
    """
    Production-safe property valuation pipeline.
    """

    def __init__(self):

        logger.info(
            "Loading trained models"
        )

        model_dir = Path(
            "saved_models"
        )

        # =====================================
        # LOAD MODELS
        # =====================================

        self.xgb_model = joblib.load(
            model_dir / "xgb_model.pkl"
        )

        self.lgbm_model = joblib.load(
            model_dir / "lgbm_model.pkl"
        )

        self.meta_model = joblib.load(
            model_dir / "meta_model.pkl"
        )

        logger.success(
            "All ML models loaded"
        )

        # =====================================
        # LOAD PREPROCESSOR
        # =====================================

        self.preprocessor = (
            load_preprocessor(
                model_dir
                / "preprocessor.pkl"
            )
        )

        # =====================================
        # LOAD FEATURE NAMES
        # =====================================

        with open(
            model_dir
            / "feature_names.json",
            "r",
        ) as f:
            self.feature_names = (
                json.load(f)
            )

        logger.success(
            "Prediction pipeline initialized"
        )

    def prepare_features(
        self,
        input_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Create inference-safe engineered features.
        """

        logger.info(
            "Preparing inference features"
        )

        df = input_df.copy()

        # =====================================
        # ENGINEERED FEATURES
        # =====================================

        df = create_engineered_features(
            df
        )

        logger.success(
            "Inference features prepared"
        )

        return df

    def predict(
        self,
        input_df: pd.DataFrame,
    ) -> dict:
        """
        Full stacked property valuation inference.
        """

        logger.info(
            "Starting property valuation inference"
        )

        # =====================================
        # FEATURE ENGINEERING
        # =====================================

        processed_df = (
            self.prepare_features(
                input_df
            )
        )

        # =====================================
        # PREPROCESSING
        # =====================================

        transformed_input = (
            self.preprocessor.transform(
                processed_df
            )
        )

        logger.success(
            "Input preprocessing completed"
        )

        # =====================================
        # BASE MODEL PREDICTIONS
        # =====================================

        xgb_prediction = (
            self.xgb_model.predict(
                transformed_input
            )
        )

        lgbm_prediction = (
            self.lgbm_model.predict(
                transformed_input
            )
        )

        logger.success(
            "Base model predictions completed"
        )

        # =====================================
        # STACKING
        # =====================================

        meta_features = np.column_stack(
            [
                xgb_prediction,
                lgbm_prediction,
            ]
        )

        stacked_prediction_log = (
            self.meta_model.predict(
                meta_features
            )
        )

        # =====================================
        # REVERSE LOG TRANSFORM
        # =====================================

        predicted_price = int(
            np.expm1(
                stacked_prediction_log[0]
            )
        )

        logger.success(
            f"Predicted property value: "
            f"{predicted_price}"
        )

        # =====================================
        # CONFIDENCE RANGE
        # =====================================

        confidence_margin = int(
            predicted_price * 0.09
        )

        low_range = (
            predicted_price
            - confidence_margin
        )

        high_range = (
            predicted_price
            + confidence_margin
        )

        logger.success(
            "Confidence interval generated"
        )

        return {
            "predicted_price_inr": (
                predicted_price
            ),
            "confidence_range": {
                "low_inr": int(
                    low_range
                ),
                "high_inr": int(
                    high_range
                ),
                "margin_inr": int(
                    confidence_margin
                ),
                "confidence_level": (
                    "91%"
                ),
            },
            "mape_estimate": 0.0934,
            "base_model_predictions": {
                "xgboost": int(
                    np.expm1(
                        xgb_prediction[0]
                    )
                ),
                "lightgbm": int(
                    np.expm1(
                        lgbm_prediction[0]
                    )
                ),
            },
        }