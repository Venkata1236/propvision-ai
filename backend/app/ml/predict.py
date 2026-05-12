import json

import joblib
import numpy as np
import pandas as pd
from loguru import logger

from app.core.config import settings
from app.ml.feature_engineering import (
    add_engineered_features,
)


class PropertyValuationModel:
    """
    Runtime inference engine for property valuation.
    """

    def __init__(self):
        logger.info("Loading trained models")

        self.xgb_model = joblib.load(
            settings.xgb_model_path
        )

        self.lgbm_model = joblib.load(
            settings.lgbm_model_path
        )

        self.meta_model = joblib.load(
            settings.meta_model_path
        )

        logger.info("Loading preprocessor")

        self.preprocessor = joblib.load(
            settings.preprocessor_path
        )

        logger.info("Loading feature names")

        with open(
            settings.feature_names_path,
            "r",
        ) as f:
            self.feature_names = json.load(f)

        logger.success(
            "All valuation artifacts loaded"
        )

    def predict(
        self,
        input_df: pd.DataFrame,
    ) -> dict:
        """
        Generate stacked ensemble prediction.
        """

        logger.info(
            "Starting property valuation inference"
        )

        # =========================
        # FEATURE ENGINEERING
        # =========================

        engineered_df = (
            add_engineered_features(
                input_df
            )
        )

        # =========================
        # REMOVE TARGET IF EXISTS
        # =========================

        engineered_df = engineered_df.drop(
            columns=["SalePrice"],
            errors="ignore",
        )

        # =========================
        # PREPROCESS
        # =========================

        processed_input = (
            self.preprocessor.transform(
                engineered_df
            )
        )

        logger.info(
            "Preprocessing completed"
        )

        # =========================
        # BASE MODEL PREDICTIONS
        # =========================

        xgb_prediction = (
            self.xgb_model.predict(
                processed_input
            )
        )

        lgbm_prediction = (
            self.lgbm_model.predict(
                processed_input
            )
        )

        logger.info(
            "Base model predictions generated"
        )

        # =========================
        # STACKING META INPUT
        # =========================

        meta_input = np.column_stack(
            [
                xgb_prediction,
                lgbm_prediction,
            ]
        )

        # =========================
        # FINAL PREDICTION
        # =========================

        final_prediction_log = (
            self.meta_model.predict(
                meta_input
            )
        )

        final_prediction = int(
            np.expm1(
                final_prediction_log[0]
            )
        )

        logger.success(
            f"Final valuation generated: "
            f"{final_prediction}"
        )

        # =========================
        # CONFIDENCE RANGE
        # =========================

        from app.ml.confidence import (
            ConfidenceIntervalCalculator
        )

        calculator = (
            ConfidenceIntervalCalculator()
        )

        confidence_range = (
            calculator.calculate(
                final_prediction
            )
        )

        return {
            "predicted_price_inr": (
                final_prediction
            ),
            "confidence_range": (
                confidence_range
            ),
            "mape_estimate": 0.0934,
            "base_model_predictions": {
                "xgboost_prediction": int(
                    np.expm1(
                        xgb_prediction[0]
                    )
                ),
                "lightgbm_prediction": int(
                    np.expm1(
                        lgbm_prediction[0]
                    )
                ),
            },
        }

    def _calculate_confidence_range(
        self,
        prediction: int,
    ) -> dict:
        """
        Generate confidence interval using model MAPE.
        """

        logger.info(
            "Calculating confidence range"
        )

        margin = int(
            prediction * 0.0934
        )

        low = prediction - margin

        high = prediction + margin

        return {
            "low_inr": low,
            "high_inr": high,
        }