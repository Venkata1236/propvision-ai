import time
import uuid

import pandas as pd
from fastapi import APIRouter, HTTPException
from loguru import logger

from app.agents.crew import (
    MarketIntelligenceCrew,
)
from app.ml.explainer import (
    PropertySHAPExplainer,
)
from app.ml.predict import (
    PropertyValuationModel,
)
from app.models.schemas import (
    ComparableSale,
    ConfidenceRange,
    InvestmentRecommendation,
    MarketAnalysis,
    PropertyInput,
    SHAPExplanation,
    ValuationResponse,
)
from app.rag.retriever import (
    ComparableSalesRetriever,
)

router = APIRouter()

# =====================================
# LOAD GLOBAL SERVICES
# =====================================

logger.info(
    "Loading valuation services"
)

valuation_model = (
    PropertyValuationModel()
)

shap_explainer = (
    PropertySHAPExplainer()
)

comparable_retriever = (
    ComparableSalesRetriever()
)

market_crew = (
    MarketIntelligenceCrew()
)

logger.success(
    "All valuation services initialized"
)


@router.post(
    "/valuate",
    response_model=ValuationResponse,
)
async def valuate_property(
    property_input: PropertyInput,
):
    """
    Full property valuation pipeline.
    """

    start_time = time.time()

    logger.info(
        "Starting valuation request"
    )

    try:

        # =========================
        # CONVERT TO DATAFRAME
        # =========================

        input_df = pd.DataFrame(
            [
                {
                    "Neighborhood": (
                        property_input.neighborhood
                    ),
                    "GrLivArea": (
                        property_input.total_sqft
                    ),
                    "BedroomAbvGr": (
                        property_input.bedrooms
                    ),
                    "FullBath": (
                        property_input.bathrooms
                    ),
                    "OverallQual": (
                        property_input.overall_quality
                    ),
                    "house_age": (
                        property_input.house_age_years
                    ),
                    "is_remodeled": int(
                        property_input.is_remodeled
                    ),
                    "has_garage": int(
                        property_input.has_garage
                    ),
                    "has_pool": int(
                        property_input.has_pool
                    ),
                    "floor_number": (
                        property_input.floor_number
                    ),
                }
            ]
        )

        logger.success(
            "Input dataframe prepared"
        )

        # =========================
        # PROPERTY VALUATION
        # =========================

        prediction_result = (
            valuation_model.predict(
                input_df
            )
        )

        predicted_price = (
            prediction_result[
                "predicted_price_inr"
            ]
        )

        logger.success(
            f"Predicted price: "
            f"{predicted_price}"
        )

        # =========================
        # SHAP EXPLANATION
        # =========================

        shap_result = (
            shap_explainer.explain_prediction(
                input_df
            )
        )

        logger.success(
            "SHAP explanation generated"
        )

        # =========================
        # COMPARABLE SALES
        # =========================

        comparable_sales = (
            comparable_retriever
            .retrieve_comparable_sales(
                property_data={
                    "Neighborhood": (
                        property_input.neighborhood
                    ),
                    "GrLivArea": (
                        property_input.total_sqft
                    ),
                    "BedroomAbvGr": (
                        property_input.bedrooms
                    ),
                    "FullBath": (
                        property_input.bathrooms
                    ),
                    "OverallQual": (
                        property_input.overall_quality
                    ),
                }
            )
        )

        logger.success(
            "Comparable sales retrieved"
        )

        # =========================
        # CREWAI MARKET ANALYSIS
        # =========================

        crew_result = (
            market_crew.run_analysis(
                property_details=(
                    property_input.model_dump()
                ),
                predicted_price=(
                    predicted_price
                ),
                comparable_sales=(
                    comparable_sales
                ),
            )
        )

        logger.success(
            "CrewAI analysis completed"
        )

        # =========================
        # MOCK STRUCTURED OUTPUTS
        # =========================

        market_analysis = (
            MarketAnalysis(
                trend="APPRECIATING",
                yoy_change_pct=12.3,
                forecast=(
                    "Strong buyer demand and "
                    "limited inventory suggest "
                    "continued appreciation over "
                    "next 6-12 months."
                ),
                demand_level="HIGH",
            )
        )

        investment_recommendation = (
            InvestmentRecommendation(
                verdict="BUY",
                reasoning=(
                    crew_result[
                        "market_intelligence"
                    ]
                ),
                suggested_offer_inr=(
                    predicted_price - 300000
                ),
            )
        )

        # =========================
        # PROCESSING TIME
        # =========================

        processing_time = round(
            time.time() - start_time,
            2,
        )

        logger.success(
            f"Valuation completed in "
            f"{processing_time}s"
        )

        # =========================
        # FINAL RESPONSE
        # =========================

        return ValuationResponse(
            valuation_id=str(
                uuid.uuid4()
            ),
            predicted_price_inr=(
                predicted_price
            ),
            confidence_range=(
                ConfidenceRange(
                    **prediction_result[
                        "confidence_range"
                    ]
                )
            ),
            mape_estimate=(
                prediction_result[
                    "mape_estimate"
                ]
            ),
            shap_explanation=(
                SHAPExplanation(
                    **shap_result
                )
            ),
            comparable_sales=[
                ComparableSale(**sale)
                for sale in comparable_sales
            ],
            market_analysis=(
                market_analysis
            ),
            investment_recommendation=(
                investment_recommendation
            ),
            processing_time_seconds=(
                processing_time
            ),
        )

    except Exception as e:

        logger.exception(
            "Valuation pipeline failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )