from typing import Dict, List

import joblib
import numpy as np
import pandas as pd
import shap
from loguru import logger

from app.core.config import settings


class PropertySHAPExplainer:
    """
    SHAP explainability engine for property valuation.
    """

    def __init__(self):
        logger.info("Loading XGBoost model")

        self.model = joblib.load(
            settings.xgb_model_path
        )

        logger.info("Loading preprocessor")

        self.preprocessor = joblib.load(
            settings.preprocessor_path
        )

        logger.info("Initializing SHAP TreeExplainer")

        self.explainer = shap.TreeExplainer(
            self.model
        )

        logger.success(
            "SHAP explainer initialized successfully"
        )

    def explain_prediction(
        self,
        input_df: pd.DataFrame,
    ) -> Dict:
        """
        Generate SHAP explanation for a single property.
        """

        logger.info(
            "Generating SHAP explanation"
        )

        # =========================
        # PREPROCESS INPUT
        # =========================

        processed_input = (
            self.preprocessor.transform(input_df)
        )

        # =========================
        # SHAP VALUES
        # =========================

        shap_values = self.explainer.shap_values(
            processed_input
        )

        shap_array = shap_values[0]

        # =========================
        # FEATURE NAMES
        # =========================

        feature_names = (
            self.preprocessor.get_feature_names_out()
        )

        # =========================
        # CREATE FACTOR TABLE
        # =========================

        explanation_df = pd.DataFrame(
            {
                "feature": feature_names,
                "shap_value": shap_array,
            }
        )

        explanation_df["abs_value"] = (
            explanation_df["shap_value"].abs()
        )

        explanation_df = explanation_df.sort_values(
            by="abs_value",
            ascending=False,
        )

        # =========================
        # POSITIVE FACTORS
        # =========================

        positive_factors = (
            explanation_df[
                explanation_df["shap_value"] > 0
            ]
            .head(5)
        )

        # =========================
        # NEGATIVE FACTORS
        # =========================

        negative_factors = (
            explanation_df[
                explanation_df["shap_value"] < 0
            ]
            .head(5)
        )

        # =========================
        # FORMAT OUTPUT
        # =========================

        positive_results = (
            self._format_factors(
                positive_factors,
                positive=True,
            )
        )

        negative_results = (
            self._format_factors(
                negative_factors,
                positive=False,
            )
        )

        # =========================
        # BASE VALUE
        # =========================

        base_value = (
            np.expm1(
                self.explainer.expected_value
            )
        )

        logger.success(
            "SHAP explanation generated successfully"
        )

        return {
            "positive_factors": positive_results,
            "negative_factors": negative_results,
            "base_value_inr": int(base_value),
        }

    def _format_factors(
        self,
        factors_df: pd.DataFrame,
        positive: bool,
    ) -> List[Dict]:
        """
        Convert SHAP factors into frontend-friendly format.
        """

        results = []

        for _, row in factors_df.iterrows():

            impact_inr = int(
                abs(np.expm1(row["shap_value"]))
            )

            results.append(
                {
                    "factor": self._clean_feature_name(
                        row["feature"]
                    ),
                    "impact_inr": impact_inr,
                    "plain_english": (
                        self._generate_explanation(
                            row["feature"],
                            positive,
                        )
                    ),
                }
            )

        return results

    def _clean_feature_name(
        self,
        feature_name: str,
    ) -> str:
        """
        Convert encoded feature names into readable labels.
        """

        feature_name = feature_name.replace(
            "num__",
            "",
        )

        feature_name = feature_name.replace(
            "cat__",
            "",
        )

        feature_name = feature_name.replace(
            "_",
            " ",
        )

        return feature_name.title()

    def _generate_explanation(
        self,
        feature_name: str,
        positive: bool,
    ) -> str:
        """
        Generate plain-English explanation.
        """

        explanations = {
            "overallqual": (
                "High construction quality"
            ),
            "garagearea": (
                "Spacious garage increases value"
            ),
            "total_sf": (
                "Large living area premium"
            ),
            "neighborhood": (
                "Premium neighborhood location"
            ),
            "house_age": (
                "Property age impacts valuation"
            ),
            "has_pool": (
                "Luxury pool amenity premium"
            ),
        }

        feature_name_lower = (
            feature_name.lower()
        )

        for key, explanation in (
            explanations.items()
        ):
            if key in feature_name_lower:
                return explanation

        if positive:
            return (
                "Feature positively impacts valuation"
            )

        return (
            "Feature reduces property valuation"
        )