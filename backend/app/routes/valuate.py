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

        # =====================================
        # CREATE TRAINING-COMPATIBLE INPUT
        # =====================================

        estimated_year_built = (
            2010
            - property_input.house_age_years
        )

        estimated_remodel_year = (
            2010
            if property_input.is_remodeled
            else estimated_year_built
        )

        input_df = pd.DataFrame(
            [
                {
                    # =====================
                    # ORIGINAL KAGGLE FIELDS
                    # =====================

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
                    "GarageArea": (
                        500
                        if property_input.has_garage
                        else 0
                    ),
                    "PoolArea": (
                        1
                        if property_input.has_pool
                        else 0
                    ),
                    "YrSold": 2010,
                    "YearBuilt": (
                        estimated_year_built
                    ),
                    "YearRemodAdd": (
                        estimated_remodel_year
                    ),
                    "OverallCond": 5,
                    "TotalBsmtSF": (
                        int(
                            property_input.total_sqft
                            * 0.4
                        )
                    ),
                    "1stFlrSF": (
                        int(
                            property_input.total_sqft
                            * 0.6
                        )
                    ),
                    "2ndFlrSF": (
                        int(
                            property_input.total_sqft
                            * 0.4
                        )
                    ),

                    # =====================
                    # ENGINEERED FEATURES
                    # =====================

                    "house_age": (
                        property_input.house_age_years
                    ),
                    "remod_age": (
                        0
                        if property_input.is_remodeled
                        else property_input.house_age_years
                    ),
                    "is_remodeled": int(
                        property_input.is_remodeled
                    ),
                    "total_sf": (
                        property_input.total_sqft
                    ),
                    "overall_quality_score": (
                        property_input.overall_quality
                        * 5
                    ),
                    "has_pool": int(
                        property_input.has_pool
                    ),
                    "has_garage": int(
                        property_input.has_garage
                    ),
                    "has_basement": 1,
                    "floor_number": (
                        property_input.floor_number
                    ),
                }
            ]
        )

        logger.success(
            "Training-compatible input dataframe prepared"
        )

        # =====================================
        # PROPERTY VALUATION
        # =====================================

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
            f"Predicted property value: "
            f"{predicted_price}"
        )

        # =====================================
        # SHAP EXPLANATION
        # =====================================

        shap_result = (
            shap_explainer.explain_prediction(
                input_df
            )
        )

        logger.success(
            "SHAP explanation generated"
        )

        # =====================================
        # COMPARABLE SALES
        # =====================================

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
                    "GarageArea": (
                        500
                        if property_input.has_garage
                        else 0
                    ),
                }
            )
        )

        logger.success(
            "Comparable sales retrieved"
        )

        # =====================================
        # CREWAI MARKET ANALYSIS
        # =====================================

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
            "CrewAI market analysis completed"
        )

        # =====================================
        # MOCK MARKET ANALYSIS
        # =====================================

        market_analysis = (
            MarketAnalysis(
                trend="APPRECIATING",
                yoy_change_pct=12.3,
                forecast=(
                    "Strong buyer demand and "
                    "limited premium inventory "
                    "suggest continued property "
                    "appreciation over the next "
                    "6-12 months."
                ),
                demand_level="HIGH",
            )
        )

        # =====================================
        # INVESTMENT RECOMMENDATION
        # =====================================

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

        # =====================================
        # PROCESSING TIME
        # =====================================

        processing_time = round(
            time.time() - start_time,
            2,
        )

        logger.success(
            f"Full valuation pipeline "
            f"completed in "
            f"{processing_time}s"
        )

        # =====================================
        # FINAL RESPONSE
        # =====================================

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