from crewai import Crew, Process
from loguru import logger

from app.agents.agents import (
    create_comparable_analyst,
    create_investment_advisor,
    create_market_trend_analyst,
)
from app.agents.tasks import (
    create_comparable_sales_task,
    create_investment_advice_task,
    create_market_trend_task,
)


class MarketIntelligenceCrew:
    """
    Multi-agent real estate intelligence system.
    """

    def __init__(self):

        logger.info(
            "Initializing Market Intelligence Crew"
        )

        # =========================
        # AGENTS
        # =========================

        self.comparable_analyst = (
            create_comparable_analyst()
        )

        self.market_trend_analyst = (
            create_market_trend_analyst()
        )

        self.investment_advisor = (
            create_investment_advisor()
        )

        logger.success(
            "All CrewAI agents initialized"
        )

    def run_analysis(
        self,
        property_details: dict,
        predicted_price: int,
        comparable_sales: list,
    ) -> dict:
        """
        Execute sequential multi-agent analysis.
        """

        logger.info(
            "Starting market intelligence workflow"
        )

        # =========================
        # TASKS
        # =========================

        comparable_task = (
            create_comparable_sales_task(
                agent=self.comparable_analyst,
                property_details=property_details,
                comparable_sales=comparable_sales,
            )
        )

        market_trend_task = (
            create_market_trend_task(
                agent=self.market_trend_analyst,
                property_details=property_details,
            )
        )

        investment_task = (
            create_investment_advice_task(
                agent=self.investment_advisor,
                property_details=property_details,
                predicted_price=predicted_price,
                comparable_analysis_task=comparable_task,
                market_trend_task=market_trend_task,
            )
        )

        logger.success(
            "All market intelligence tasks created"
        )

        # =========================
        # CREW
        # =========================

        crew = Crew(
            agents=[
                self.comparable_analyst,
                self.market_trend_analyst,
                self.investment_advisor,
            ],
            tasks=[
                comparable_task,
                market_trend_task,
                investment_task,
            ],
            process=Process.sequential,
            verbose=True,
        )

        logger.info(
            "Executing CrewAI workflow"
        )

        result = crew.kickoff()

        logger.success(
            "Market intelligence workflow completed"
        )

        return {
            "market_intelligence": str(result)
        }


if __name__ == "__main__":

    sample_property = {
        "Neighborhood": "NoRidge",
        "GrLivArea": 2400,
        "BedroomAbvGr": 4,
        "FullBath": 3,
        "OverallQual": 8,
        "GarageArea": 500,
    }

    comparable_sales = [
        {
            "description": (
                "4BHK, 2448 sqft, NoRidge"
            ),
            "sale_price_inr": 402000,
            "similarity_score": 0.97,
        },
        {
            "description": (
                "4BHK, 2417 sqft, NoRidge"
            ),
            "sale_price_inr": 390000,
            "similarity_score": 0.96,
        },
    ]

    crew = MarketIntelligenceCrew()

    result = crew.run_analysis(
        property_details=sample_property,
        predicted_price=410000,
        comparable_sales=comparable_sales,
    )

    logger.success(
        f"CrewAI Result: {result}"
    )