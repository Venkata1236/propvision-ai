from crewai import Task
from loguru import logger


def create_comparable_sales_task(
    agent,
    property_details: dict,
    comparable_sales: list,
):
    """
    Analyze comparable sales and justify valuation.
    """

    logger.info(
        "Creating comparable sales analysis task"
    )

    return Task(
        description=f"""
Analyze the subject property and the retrieved
comparable sales below.

Subject Property:
{property_details}

Comparable Sales:
{comparable_sales}

Your responsibilities:
1. Compare the subject property against the
   retrieved sales.
2. Explain similarities and differences.
3. Identify why the property deserves premium
   or discounted pricing.
4. Justify whether the valuation appears fair.

Focus heavily on:
- square footage
- neighborhood quality
- bedrooms/bathrooms
- construction quality
- premium amenities

Return a detailed valuation justification.
""",
        expected_output="""
A professional comparable-sales analysis explaining:
- strongest comparable properties
- valuation justification
- premium or discount drivers
- pricing fairness assessment
""",
        agent=agent,
    )


def create_market_trend_task(
    agent,
    property_details: dict,
):
    """
    Analyze market conditions and future trends.
    """

    logger.info(
        "Creating market trend analysis task"
    )

    return Task(
        description=f"""
Analyze current market conditions for the
following property:

Property:
{property_details}

Your responsibilities:
1. Estimate current demand level.
2. Determine whether the market is:
   - APPRECIATING
   - STABLE
   - DECLINING
3. Analyze likely buyer demand.
4. Forecast price movement over next 6-12 months.
5. Assess whether current market conditions
   favor buyers or sellers.

Focus on:
- neighborhood attractiveness
- inventory pressure
- demand trends
- appreciation potential
- investment timing

Return a detailed market outlook.
""",
        expected_output="""
A market intelligence report containing:
- market trend classification
- demand assessment
- appreciation forecast
- investment timing insights
""",
        agent=agent,
    )


def create_investment_advice_task(
    agent,
    property_details: dict,
    predicted_price: int,
    comparable_analysis_task,
    market_trend_task,
):
    """
    Generate final investment recommendation.
    """

    logger.info(
        "Creating investment recommendation task"
    )

    return Task(
        description=f"""
You are making the FINAL investment decision
for the following property.

Property:
{property_details}

Predicted Valuation:
₹{predicted_price:,}

You will receive:
1. Comparable sales analysis
2. Market trend analysis

Your responsibilities:
1. Determine whether buyer should:
   - BUY
   - WAIT
   - NEGOTIATE

2. Explain reasoning clearly.
3. Assess investment risk.
4. Suggest negotiation strategy if appropriate.
5. Estimate a fair offer price if valuation
   appears inflated.

Decision rules:
- BUY:
  Property appears undervalued or market
  appreciation potential is strong.

- WAIT:
  Market conditions appear risky or prices
  likely to soften.

- NEGOTIATE:
  Property appears overpriced relative to
  comparable sales.

Be decisive and analytical.
Avoid generic advice.
Use evidence from previous analyses.
""",
        expected_output="""
A final investment recommendation containing:
- BUY / WAIT / NEGOTIATE verdict
- detailed reasoning
- investment risk assessment
- suggested negotiation price if needed
""",
        context=[
            comparable_analysis_task,
            market_trend_task,
        ],
        agent=agent,
    )