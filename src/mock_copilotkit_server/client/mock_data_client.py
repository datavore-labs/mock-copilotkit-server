"""Mock data client."""

import logging

logger = logging.getLogger(__name__)


class MockDataClient:
    """Mock data client.

    Uses the original Tintash mock data for integration with the frontend.
    """

    def get_brand_data(self, category: str) -> dict[str, list[dict[str, str | int | float]]]:
        category_data = {
            "cookies": [
                {"brand": "Oreo", "count": 182000, "percentage": 23.5},
                {"brand": "Chips Ahoy", "count": 78500, "percentage": 12.3},
                {"brand": "Pepperidge Farm", "count": 30000, "percentage": 8.5},
                {"brand": "Famous Amos", "count": 21500, "percentage": 7.0},
                {"brand": "Mrs Fields", "count": 44000, "percentage": 10.8},
                {"brand": "Nilla", "count": 27900, "percentage": 5.6},
                {"brand": "Nutter Butter", "count": 44800, "percentage": 8.1},
                {"brand": "Archway", "count": 45200, "percentage": 8.2},
                {"brand": "Grandma's", "count": 33400, "percentage": 6.3},
                {"brand": "Private Label", "count": 60000, "percentage": 9.7},
            ],
            "beer": [
                {"brand": "Heineken", "count": 160288, "percentage": 23.3},
                {"brand": "Corona", "count": 88751, "percentage": 12.8},
                {"brand": "Coors Light", "count": 36671, "percentage": 5.3},
                {"brand": "Miller Lite", "count": 41883, "percentage": 6.1},
                {"brand": "Budweiser", "count": 27697, "percentage": 4.0},
                {"brand": "Bud Lite", "count": 33001, "percentage": 4.8},
                {"brand": "Blue Moon", "count": 45034, "percentage": 6.5},
                {"brand": "Modelo Especial", "count": 46195, "percentage": 6.7},
                {"brand": "Michelob Ultra", "count": 28441, "percentage": 4.1},
                {"brand": "Pabst Blue Ribbon", "count": 41029, "percentage": 5.9},
                {"brand": "Sam Adams", "count": 38452, "percentage": 5.6},
                {"brand": "Guinness", "count": 47902, "percentage": 6.9},
                {"brand": "Stella Artois", "count": 55437, "percentage": 8.0},
            ],
            "cosmetics": [
                {"brand": "L'Oreal", "count": 175000, "percentage": 20.5},
                {"brand": "Maybelline", "count": 106250, "percentage": 12.5},
                {"brand": "E.L.F.", "count": 33900, "percentage": 4.0},
                {"brand": "Estée Lauder", "count": 39300, "percentage": 4.6},
                {"brand": "Rimmel", "count": 32100, "percentage": 3.8},
                {"brand": "Philosophy", "count": 27300, "percentage": 3.2},
                {"brand": "Nivea", "count": 52100, "percentage": 6.1},
                {"brand": "Dove", "count": 36800, "percentage": 4.3},
                {"brand": "NYX", "count": 31900, "percentage": 3.7},
                {"brand": "Olay", "count": 48200, "percentage": 5.6},
                {"brand": "Covergirl", "count": 40100, "percentage": 4.7},
                {"brand": "Charlotte Tilbury", "count": 61800, "percentage": 7.2},
                {"brand": "Private Label", "count": 66000, "percentage": 7.8},
            ],
            # Keep existing categories as fallback
            "snacks": [
                {"brand": "Lay's", "count": 18000, "percentage": 35},
                {"brand": "Pringles", "count": 14000, "percentage": 27},
                {"brand": "Cheetos", "count": 9000, "percentage": 17},
                {"brand": "Private Label", "count": 10000, "percentage": 19},
            ],
            "beverages": [
                {"brand": "Coca-Cola", "count": 22000, "percentage": 45},
                {"brand": "Pepsi", "count": 16000, "percentage": 32},
                {"brand": "Dr Pepper", "count": 6000, "percentage": 12},
                {"brand": "Private Label", "count": 5000, "percentage": 10},
            ],
        }

        return category_data.get(category.lower(), [])

    def get_spending_data(self, category: str) -> dict[str, list[dict[str, str | int | float]]]:
        base_data = [
            {"range": "$0-10", "count": 8000000, "percentage": 22.7},
            {"range": "$10-25", "count": 11000000, "percentage": 32.1},
            {"range": "$25-50", "count": 5000000, "percentage": 25.4},
            {"range": "$50+", "count": 7400, "percentage": 19.8},
        ]

        # Adjust ranges based on category
        if category.lower() in ["premium", "luxury"]:
            result = [
                {"range": "$25-50", "count": 5000, "percentage": 20},
                {"range": "$50-100", "count": 10000, "percentage": 40},
                {"range": "$100-200", "count": 7000, "percentage": 28},
                {"range": "$200+", "count": 3000, "percentage": 12},
            ]
        elif category.lower() in ["snacks", "beverages"]:
            result = [
                {"range": "$0-5", "count": 12000, "percentage": 35},
                {"range": "$5-15", "count": 15000, "percentage": 44},
                {"range": "$15-30", "count": 6000, "percentage": 17},
                {"range": "$30+", "count": 1000, "percentage": 3},
            ]
        elif category.lower() in ["beer"] or category.lower() in ["cosmetics"]:
            result = [
                {"range": "$0-10", "count": 15000000, "percentage": 22.7},
                {"range": "$10-25", "count": 10000000, "percentage": 32.1},
                {"range": "$25-50", "count": 6000000, "percentage": 25.4},
                {"range": "$50+", "count": 3000000, "percentage": 19.8},
            ]
        else:
            result = base_data

        return result

    def get_purchase_recency_data(self) -> list[dict[str, str | int | float]]:
        return [
            {"period": "0-30 Days", "count": 710000, "percentage": 26.5},
            {"period": "30-60 Days", "count": 830000, "percentage": 17.6},
            {"period": "60-90 Days", "count": 690000, "percentage": 14.6},
            {"period": "90-180 Days", "count": 1450000, "percentage": 9.5},
        ]


# Mock data functions for different categories
def get_mock_purchase_recency_data(category: str) -> list[dict[str, str | int | float]]:
    """Get purchase recency data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating purchase recency data for {category=}")

    # Updated purchase recency data with new periods and counts
    base_data = MockDataClient().get_purchase_recency_data()

    # Adjust data based on category
    # TODO - update to only do this for the mock data.
    multiplier: float = 1.0
    if category.lower() in ["premium", "luxury"]:
        multiplier = 0.6
    elif category.lower() in ["snacks", "beverages", "beer"]:
        multiplier = 1.4

    result: list[dict[str, str | int | float]] = [
        {
            "period": item["period"],
            "count": int(float(item["count"]) * multiplier),
            "percentage": item["percentage"],
        }
        for item in base_data
    ]

    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} periods for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample data: {result[0] if result else 'None'}")

    return result


def get_mock_spending_data(category: str) -> list[dict[str, str | int | float]]:
    """Get spending data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating spending data for {category=}")

    result = MockDataClient().get_spending_data(category)

    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} spending ranges for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample spending data: {result[0] if result else 'None'}")

    return result


def get_mock_brand_data(
    category: str = "cookies",
) -> list[dict[str, str | int | float]]:
    """Get brand data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating brand data for {category=}")

    brand_mapping = MockDataClient().get_brand_data(category)

    result = brand_mapping.get(category.lower())

    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} brands for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample brand data: {result[0] if result else 'None'}")

    return result
