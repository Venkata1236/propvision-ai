from typing import List, Optional

from pydantic import BaseModel, Field


# =====================================
# REQUEST SCHEMA
# =====================================

class PropertyInput(BaseModel):
    """
    Incoming property valuation request.
    """

    neighborhood: str = Field(
        ...,
        example="NoRidge",
    )

    total_sqft: int = Field(
        ...,
        gt=100,
        example=2400,
    )

    bedrooms: int = Field(
        ...,
        ge=1,
        le=10,
        example=4,
    )

    bathrooms: int = Field(
        ...,
        ge=1,
        le=10,
        example=3,
    )

    overall_quality: int = Field(
        ...,
        ge=1,
        le=10,
        example=8,
    )

    house_age_years: int = Field(
        ...,
        ge=0,
        example=5,
    )

    is_remodeled: bool = Field(
        ...,
        example=True,
    )

    has_garage: bool = Field(
        ...,
        example=True,
    )

    has_pool: bool = Field(
        ...,
        example=False,
    )

    floor_number: int = Field(
        ...,
        ge=0,
        example=2,
    )


# =====================================
# SHAP FACTOR
# =====================================

class SHAPFactor(BaseModel):
    """
    Individual SHAP factor explanation.
    """

    factor: str

    impact_inr: int

    plain_english: str


# =====================================
# SHAP EXPLANATION
# =====================================

class SHAPExplanation(BaseModel):
    """
    Full SHAP explainability payload.
    """

    positive_factors: List[
        SHAPFactor
    ]

    negative_factors: List[
        SHAPFactor
    ]

    base_value_inr: int


# =====================================
# COMPARABLE SALE
# =====================================

class ComparableSale(BaseModel):
    """
    Comparable property sale result.
    """

    property_id: int

    description: str

    sale_price_inr: int

    sale_date: str

    similarity_score: float

    neighborhood: str


# =====================================
# MARKET ANALYSIS
# =====================================

class MarketAnalysis(BaseModel):
    """
    Market trend intelligence output.
    """

    trend: str

    yoy_change_pct: float

    forecast: str

    demand_level: str


# =====================================
# INVESTMENT RECOMMENDATION
# =====================================

class InvestmentRecommendation(BaseModel):
    """
    Final AI investment verdict.
    """

    verdict: str

    reasoning: str

    suggested_offer_inr: Optional[
        int
    ] = None


# =====================================
# CONFIDENCE RANGE
# =====================================

class ConfidenceRange(BaseModel):
    """
    Valuation confidence interval.
    """

    low_inr: int

    high_inr: int

    margin_inr: int

    confidence_level: str


# =====================================
# FULL RESPONSE
# =====================================

class ValuationResponse(BaseModel):
    """
    Full property valuation response.
    """

    valuation_id: str

    predicted_price_inr: int

    confidence_range: (
        ConfidenceRange
    )

    mape_estimate: float

    shap_explanation: (
        SHAPExplanation
    )

    comparable_sales: List[
        ComparableSale
    ]

    market_analysis: (
        MarketAnalysis
    )

    investment_recommendation: (
        InvestmentRecommendation
    )

    processing_time_seconds: float