from crewai import Agent, LLM
from loguru import logger

from app.core.config import settings


logger.info(
    "Initializing CrewAI language model"
)

llm = LLM(
    model=f"openai/{settings.openai_model}",
    temperature=0.2,
    api_key=settings.openai_api_key,
)

logger.success(
    "CrewAI LLM initialized"
)


def create_comparable_analyst():
    """
    Agent responsible for analyzing comparable sales.
    """

    logger.info(
        "Creating Comparable Sales Analyst"
    )

    return Agent(
        role=(
            "Real Estate Comparable Sales Analyst"
        ),
        goal=(
            "Analyze comparable property sales and "
            "justify the predicted property valuation "
            "using retrieved market evidence."
        ),
        backstory=(
            "You are a senior real estate valuation "
            "expert with 15 years of experience in "
            "property pricing, comparative market "
            "analysis, and valuation justification. "
            "You specialize in identifying why "
            "properties command premium or discounted "
            "pricing."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_market_trend_analyst():
    """
    Agent responsible for market trend analysis.
    """

    logger.info(
        "Creating Market Trend Analyst"
    )

    return Agent(
        role=(
            "Real Estate Market Trend Specialist"
        ),
        goal=(
            "Analyze neighborhood-level real estate "
            "market trends, demand patterns, price "
            "movements, and future outlook."
        ),
        backstory=(
            "You are a housing market economist "
            "specializing in residential property "
            "markets, buyer demand cycles, "
            "interest-rate impacts, and investment "
            "timing strategies. You help buyers "
            "understand whether market conditions "
            "favor buying now or waiting."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )


def create_investment_advisor():
    """
    Agent responsible for final investment recommendation.
    """

    logger.info(
        "Creating Investment Advisor"
    )

    return Agent(
        role=(
            "Property Investment Advisor"
        ),
        goal=(
            "Provide a final investment recommendation "
            "based on valuation, comparable sales, "
            "market trends, and investment risk."
        ),
        backstory=(
            "You are a strategic property investment "
            "advisor helping buyers make intelligent "
            "real estate decisions. You combine "
            "valuation analysis, comparable sales, "
            "market trends, and negotiation strategy "
            "to determine whether a buyer should "
            "BUY, WAIT, or NEGOTIATE."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
    )