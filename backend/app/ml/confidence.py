from typing import Dict

from loguru import logger


class ConfidenceIntervalCalculator:
    """
    Confidence interval generator for property valuations.
    """

    def __init__(
        self,
        mape: float = 0.0934,
    ):
        """
        Initialize calculator with model MAPE.
        """

        self.mape = mape

        logger.info(
            f"Confidence calculator initialized "
            f"with MAPE={self.mape}"
        )

    def calculate(
        self,
        prediction: int,
    ) -> Dict:
        """
        Generate valuation confidence range.
        """

        logger.info(
            "Calculating confidence interval"
        )

        margin = int(
            prediction * self.mape
        )

        low_value = prediction - margin

        high_value = prediction + margin

        logger.success(
            f"Confidence interval generated: "
            f"{low_value} - {high_value}"
        )

        return {
            "low_inr": low_value,
            "high_inr": high_value,
            "margin_inr": margin,
            "confidence_level": "approx_90_percent",
        }

    def calculate_percentage_margin(
        self,
    ) -> float:
        """
        Return confidence percentage margin.
        """

        return round(
            self.mape * 100,
            2,
        )
        
        