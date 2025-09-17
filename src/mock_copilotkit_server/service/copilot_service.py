import logging
from datetime import datetime

from copilotkit import Action as CopilotAction
from copilotkit import CopilotKitRemoteEndpoint

from mock_copilotkit_server.handler.get_brand_data import (
    BrandData,
    handle_get_brand_data,
)
from mock_copilotkit_server.handler.get_purchase_recency_data import (
    PurchaseRecencyData,
    handle_get_purchase_recency_data,
)
from mock_copilotkit_server.handler.get_spending_data import (
    SpendingData,
    handle_get_spending_data,
)

logger = logging.getLogger(__name__)


# Action 1: Get Purchase Recency Data
get_purchase_recency_data_action: CopilotAction = CopilotAction(
    name="getPurchaseRecencyData",
    description="Get purchase recency distribution data for a specific product category",
    parameters=[
        {
            "name": "category",
            "type": "string",
            "description": "Product category to analyze (e.g., 'cookies', 'snacks', 'beverages')",
            "required": True,
        }
    ],
    handler=handle_get_purchase_recency_data,
)


# Action 2: Get Brand Data
get_brand_data_action: CopilotAction = CopilotAction(
    name="getBrandData",
    description="Get brand breakdown data for a specific product category",
    parameters=[
        {
            "name": "category",
            "type": "string",
            "description": "Product category being analyzed",
            "required": True,
        },
        {
            "name": "selected_recency",
            "type": "string",
            "description": "Previously selected recency period",
            "required": False,
        },
    ],
    handler=handle_get_brand_data,
)


# Action 3: Get Spending Data
get_spending_data_action: CopilotAction = CopilotAction(
    name="getSpendingData",
    description="Get spending distribution data for a specific product category",
    parameters=[
        {
            "name": "category",
            "type": "string",
            "description": "Product category being analyzed",
            "required": True,
        },
        {
            "name": "selected_brands",
            "type": "array",
            "description": "Previously selected brands",
            "required": False,
        },
    ],
    handler=handle_get_spending_data,
)


# Action 4: Update Audience Insights
update_audience_insights_action = CopilotAction(
    name="updateAudienceInsights",
    description="Update audience insights with new consumer count and composition",
    parameters=[
        {
            "name": "total_consumers",
            "type": "number",
            "description": "Total number of consumers in the audience",
            "required": True,
        },
        {
            "name": "ingredients",
            "type": "array",
            "description": "list of audience ingredients",
            "required": False,
        },
    ],
    handler=lambda total_consumers, ingredients=None: {
        "total_consumers": total_consumers,
        "ingredients": ingredients or [],
        "message": f"Updated audience size: {total_consumers:,} consumers",
    },
)

# Action 5: Add Exclusion
add_exclusion_action = CopilotAction(
    name="addExclusion",
    description="Add exclusion criteria to remove certain consumer groups from the audience",
    parameters=[
        {
            "name": "exclusion_type",
            "type": "string",
            "description": "Type of exclusion (brand, category, behavior)",
            "required": True,
        },
        {
            "name": "label",
            "type": "string",
            "description": "Label for the exclusion",
            "required": True,
        },
        {
            "name": "percentage",
            "type": "number",
            "description": "Percentage of audience to exclude",
            "required": True,
        },
    ],
    handler=lambda exclusion_type, label, percentage: {
        "exclusion": {
            "id": f"exclusion_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": exclusion_type,
            "label": label,
            "percentage": percentage,
        },
        "message": f"Added exclusion: {label} (-{percentage}%)",
    },
)

# Action 6: Add Filter
add_filter_action = CopilotAction(
    name="addFilter",
    description="Add filter criteria to refine the audience",
    parameters=[
        {
            "name": "filter_type",
            "type": "string",
            "description": "Type of filter (spending, location, frequency)",
            "required": True,
        },
        {
            "name": "label",
            "type": "string",
            "description": "Label for the filter",
            "required": True,
        },
        {
            "name": "value",
            "type": "string",
            "description": "Filter value",
            "required": True,
        },
    ],
    handler=lambda filter_type, label, value: {
        "filter": {
            "id": f"filter_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": filter_type,
            "label": label,
            "value": value,
        },
        "message": f"Added filter: {label}",
    },
)

# Action 7: Create Final Audience
create_audience_action = CopilotAction(
    name="createAudience",
    description="Create the final audience with all selected criteria",
    parameters=[
        {
            "name": "audience_name",
            "type": "string",
            "description": "Name for the new audience",
            "required": True,
        },
        {
            "name": "audience_data",
            "type": "object",
            "description": "Complete audience data including insights, ingredients, exclusions, and filters",
            "required": True,
        },
    ],
    handler=lambda audience_name, audience_data: {
        "audience": {
            "id": f"audience_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": audience_name,
            "created_at": datetime.now().isoformat(),
            "data": audience_data,
        },
        "message": f"Successfully created audience: {audience_name}",
    },
)


# Test the actions on startup
def test_copilotkit_actions():
    logger.info("🧪 [STARTUP TEST] Testing backend actions...")
    try:
        # Test getPurchaseRecencyData
        result_purchase: PurchaseRecencyData = handle_get_purchase_recency_data(category="cookies")
        logger.info(f"✅ [STARTUP TEST] getPurchaseRecencyData works: {len(result_purchase)} periods")

        # Test getBrandData
        result_brand: BrandData = handle_get_brand_data(category="cookies", selected_recency="last_30_days")
        logger.info(f"✅ [STARTUP TEST] getBrandData works: {len(result_brand)} brands")

        # Test getSpendingData
        result_spending: SpendingData = handle_get_spending_data(category="cookies", selected_brands=["Oreo"])
        logger.info(f"✅ [STARTUP TEST] getSpendingData works: {len(result_spending)} ranges")

        logger.info("✅ [STARTUP TEST] All actions working correctly!")
    except Exception as e:
        logger.error(f"❌ [STARTUP TEST] Action test failed: {e!s}", stack_info=True, exc_info=e)


# Initialize the CopilotKit SDK with all actions
copilotkit_sdk: CopilotKitRemoteEndpoint = CopilotKitRemoteEndpoint(
    actions=[
        get_purchase_recency_data_action,
        get_brand_data_action,
        get_spending_data_action,
        update_audience_insights_action,
        add_exclusion_action,
        add_filter_action,
        create_audience_action,
    ]
)
