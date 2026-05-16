import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import shap
from loguru import logger

from app.ml.preprocess import (
    create_engineered_features,
    load_preprocessor,
)


class PropertySHAPExplainer:

    def __init__(self):

        logger.info(
            "Loading XGBoost model"
        )

        model_dir = Path(
            "saved_models"
        )

        self.xgb_model = joblib.load(
            model_dir / "xgb_model.pkl"
        )

        logger.info(
            "Loading preprocessor"
        )

        self.preprocessor = (
            
            load_preprocessor(
                model_dir
                / "preprocessor.pkl"
            )
        )

        logger.info(
            "Initializing SHAP TreeExplainer"
        )

        self.explainer = (
            shap.TreeExplainer(
                self.xgb_model
            )
        )

        with open(
            model_dir
            / "feature_names.json",
            "r",
        ) as f:
            self.feature_names = (
                json.load(f)
            )

        logger.success(
            "SHAP explainer initialized"
        )

    def explain_prediction(
        self,
        input_df: pd.DataFrame,
    ):

        logger.info(
            "Generating SHAP explanation"
        )

        # ============================
        # ENGINEERED FEATURES
        # ============================

        processed_df = (
            create_engineered_features(
                input_df.copy()
            )
        )

        # ============================
        # TRANSFORM
        # ============================

        transformed_input = (
            self.preprocessor.transform(
                processed_df
            )
        )

        # ============================
        # SHAP VALUES
        # ============================

        shap_values = (
            self.explainer.shap_values(
                transformed_input
            )
        )

        transformed_feature_names = (
            self.preprocessor.get_feature_names_out()
        )

        shap_array = shap_values[0]

        feature_impacts = []

        for feature_name, impact in zip(
            transformed_feature_names,
            shap_array,
        ):

            feature_impacts.append(
                {
                    "feature": feature_name,
                    "impact": float(impact),
                }
            )

        # ============================
        # SORT
        # ============================

        feature_impacts = sorted(
            feature_impacts,
            key=lambda x: abs(
                x["impact"]
            ),
            reverse=True,
        )

        positive_factors = []
        negative_factors = []

        # ============================
        # TOP POSITIVE
        # ============================

        for item in feature_impacts:

            if (
                item["impact"] > 0
                and len(
                    positive_factors
                )
                < 5
            ):

                positive_factors.append(
                    {
                        "factor": item[
                            "feature"
                        ],
                        "impact_inr": int(
                            abs(
                                item[
                                    "impact"
                                ]
                            )
                            * 100000
                        ),
                        "plain_english":
                        (
                            "Positive contribution "
                            "to property value"
                        ),
                    }
                )

        # ============================
        # TOP NEGATIVE
        # ============================

        for item in feature_impacts:

            if (
                item["impact"] < 0
                and len(
                    negative_factors
                )
                < 5
            ):

                negative_factors.append(
                    {
                        "factor": item[
                            "feature"
                        ],
                        "impact_inr": int(
                            abs(
                                item[
                                    "impact"
                                ]
                            )
                            * 100000
                        ),
                        "plain_english":
                        (
                            "Negative contribution "
                            "to property value"
                        ),
                    }
                )

        logger.success(
            "SHAP explanation generated"
        )

        return {
            "positive_factors":
            positive_factors,
            "negative_factors":
            negative_factors,
            "base_value_inr":
            6500000,
        }