from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, Action as CopilotAction
from typing import Dict, List, Optional
import json
from datetime import datetime
import logging
import os
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = FastAPI(debug=True)

# middleware to register CORS headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://audience-builder-demo-v2-fe-vz5cg6nm5a-uc.a.run.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"❌ [GLOBAL ERROR] {str(exc)}")
    logger.error(f"❌ [TRACEBACK]:\n{traceback.format_exc()}")
    return JSONResponse(
        {"detail": str(exc), "type": type(exc).__name__},
        status_code=500
    )

# Add a health check endpoint
@app.get("/health")
async def health_check():
    logger.info("🏥 [HEALTH CHECK] Health check endpoint called")
    return {"status": "healthy", "message": "CopilotKit server is running"}

# Add a test endpoint to verify server is running
@app.get("/")
async def root():
    logger.info("🌐 [ROOT] Root endpoint called")
    return {"message": "CopilotKit Server is running", "actions": len(sdk.actions)}

#@app.post("/test-action")
#async def test_action():
#   logger.info("🧪 [TEST] Test action called!")
#   return {"message": "Test action works!", "timestamp": datetime.now().isoformat()}



# Mock data functions for different categories
def get_purchase_recency_data(category: str) -> List[Dict]:
    
    """Get purchase recency data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating purchase recency data for category: {category}")
    
    # Updated purchase recency data with new periods and counts
    
    if category.lower() in ["cosmetics"]:
        base_data = [
            {"period": "0-30 Days", "count": 954000, "percentage": 14.06},
            {"period": "30-60 Days", "count": 1305000, "percentage": 19.24},
            {"period": "60-90 Days", "count": 1684000, "percentage": 24.83},
            {"period": "90-180 Days", "count": 2840000, "percentage": 41.87},
        ]
    elif category.lower() in ["cookies"]:
        base_data = [
            {"period": "0-30 Days", "count": 710000, "percentage": 19.29},
            {"period": "30-60 Days", "count": 830000, "percentage": 22.55},
            {"period": "60-90 Days", "count": 690000, "percentage": 18.75},
            {"period": "90-180 Days", "count": 1450000, "percentage": 39.4},
        ]
    elif category.lower() in ["beer"]:
        base_data = [
            {"period": "0-30 Days", "count": 1284000, "percentage": 26.27},
            {"period": "30-60 Days", "count": 854600, "percentage": 17.49},
            {"period": "60-90 Days", "count": 980510, "percentage": 20.06},
            {"period": "90-180 Days", "count": 1768000, "percentage": 36.18},
        ]
    elif category.lower() in ["beverages", "snacks"]:
        base_data = [
            {"period": "0-30 Days", "count": 6512000, "percentage": 15.22},
            {"period": "30-60 Days", "count": 6824800, "percentage": 15.95},
            {"period": "60-90 Days", "count": 7623000, "percentage": 17.81},
            {"period": "90-180 Days", "count": 21840000, "percentage": 51.03},
        ]
    else:
        base_data = [
            {"period": "0-30 Days", "count": 710000, "percentage": 19.29},
            {"period": "30-60 Days", "count": 830000, "percentage": 22.55},
            {"period": "60-90 Days", "count": 690000, "percentage": 18.75},
            {"period": "90-180 Days", "count": 1450000, "percentage": 39.4},
        ]
        
    
        
    # Adjust data based on category
#   multiplier = 1.0
#   if category.lower() in ["premium", "luxury"]:
#       multiplier = 0.6
#   elif category.lower() in ["snacks", "beverages", "beer"]:
#       multiplier = 1.4
    
    result = [
        {
            "period": item["period"],
            "count": item["count"],
            "percentage": item["percentage"]
        }
        for item in base_data
    ]
    
    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} periods for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample data: {result[0] if result else 'None'}")
    
    return result

def get_brand_data(category: str) -> List[Dict]:
    """Get brand data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating brand data for category: {category}")
    
    brand_mapping = {
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
        ]
    }
    
    result = brand_mapping.get(category.lower(), brand_mapping["cookies"])
    
    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} brands for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample brand data: {result[0] if result else 'None'}")
    
    return result

def get_spending_data(category: str) -> List[Dict]:
    """Get spending data for a specific category"""
    logger.info(f"📊 [DATA GENERATION] Generating spending data for category: {category}")
    
    base_data = [
        {"range": "$0-10", "count": 8000000, "percentage": 22.7},
        {"range": "$10-25", "count": 11000000, "percentage": 32.1},
        {"range": "$25-50", "count": 5000000, "percentage": 25.4},
        {"range": "$50+", "count": 7400, "percentage": 19.8},
    ]
    
    # Adjust ranges based on category
    if category.lower() in ["cosmetics"]:
        result = [
            {"range": "$25-50", "count": 5000, "percentage": 20},
            {"range": "$50-100", "count": 10000, "percentage": 40},
            {"range": "$100-200", "count": 7000, "percentage": 28},
            {"range": "$200+", "count": 3000, "percentage": 12},
        ]
    elif category.lower() in ["cookies"]:
        result = [
            {"range": "$0-5", "count": 12000, "percentage": 35},
            {"range": "$5-15", "count": 15000, "percentage": 44},
            {"range": "$15-30", "count": 6000, "percentage": 17},
            {"range": "$30+", "count": 1000, "percentage": 3},
        ]
    elif category.lower() in ["beer"]:
        result = [
            {"range": "$0-10", "count": 15000000, "percentage": 22.7},
            {"range": "$10-25", "count": 10000000, "percentage": 32.1},
            {"range": "$25-50", "count": 6000000, "percentage": 25.4},
            {"range": "$50+", "count": 3000000, "percentage": 19.8},
        ]
    elif category.lower() in ["beverages", "snacks"]:
        result = [
            {"range": "$0-10", "count": 15000000, "percentage": 22.7},
            {"range": "$10-25", "count": 10000000, "percentage": 32.1},
            {"range": "$25-50", "count": 6000000, "percentage": 25.4},
            {"range": "$50+", "count": 3000000, "percentage": 19.8},
        ]
    else:
        result = base_data
    
    logger.info(f"📊 [DATA GENERATION] Generated {len(result)} spending ranges for {category}")
    logger.info(f"📊 [DATA GENERATION] Sample spending data: {result[0] if result else 'None'}")
    
    return result

# Action handlers
def handle_get_purchase_recency_data(**kwargs):
    category = kwargs.get("category")
    logger.info(f"🚀 [BACKEND ACTION] *** getPurchaseRecencyData CALLED *** with category: {category}")
    logger.info(f"🔥 [BACKEND ACTION] *** THIS IS A BACKEND ACTION - LLM SHOULD CALL THIS ***")
    logger.info(f"📊 [BACKEND DATA] Getting purchase recency data for {category}")
    
    try:
        data = get_purchase_recency_data(category)
        total_consumers = sum(item["count"] for item in data)
        
        result = {
            "chart_type": "purchase_recency",
            "data": data,
            "category": category,
            "total_consumers": total_consumers,
            "title": f"Purchase Recency Distribution",
            "description": f"Analysis of consumers who purchased {category} and their purchase recency distribution."
        }
        
        logger.info(f"✅ [BACKEND ACTION] *** SUCCESSFULLY RETURNING DATA *** with {len(data)} periods")
        logger.info(f"🎯 [BACKEND ACTION] Result: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [BACKEND ACTION] Error in getPurchaseRecencyData: {str(e)}")
        raise

def handle_get_brand_data(**kwargs):
    category = kwargs.get("category")
    selected_recency = kwargs.get("selected_recency")
    selected_recency_percentage = kwargs.get("selected_recency_percentage", 100.0)
    logger.info(f"🚀 [BACKEND ACTION] *** getBrandData CALLED *** with category: {category}, selected_recency: {selected_recency}")
    logger.info(f"🔥 [BACKEND ACTION] *** THIS IS A BACKEND ACTION - LLM SHOULD CALL THIS ***")
    logger.info(f"📊 [BACKEND DATA] Getting brand data for {category}")
    
    try:
        brand_data = get_brand_data(category)
        
        # 2. Get the *original* total consumer count from the recency data
        all_recency_data = get_purchase_recency_data(category)
        original_total_consumers = sum(item["count"] for item in all_recency_data)
        
        # 3. Calculate the new total_consumers based on the percentage
        # Convert percentage (e.g., 44.1) to a factor (e.g., 0.441)
        percentage_factor = selected_recency_percentage / 100.0
        new_total_consumers = int(original_total_consumers * percentage_factor)
        
        logger.info(f"📊 [CALCULATION] Original total: {original_total_consumers}")
        logger.info(f"📊 [CALCULATION] Percentage factor: {percentage_factor} (from {selected_recency_percentage}%)")
        logger.info(f"📊 [CALCULATION] New total consumers: {new_total_consumers}")
        
        # 4. Scale brand data counts to match the new total
        scaled_brand_data = [
            {
                "brand": item["brand"],
                "count": int(item["count"] * percentage_factor), # Apply scaling factor
                "percentage": item["percentage"] # Keep original percentage distribution
            }
            for item in brand_data
        ]
        
        result = {
            "chart_type": "brand_breakdown",
            "data": scaled_brand_data,
            "category": category,
            "selected_recency": selected_recency,
            "selected_recency_percentage": selected_recency_percentage, # Pass back the percentage
            "total_consumers": new_total_consumers, # <-- HERE IS THE NEW TOTAL
            "title": f"{category.title()} Brand Breakdown",
            "description": f"Brand distribution for {new_total_consumers:,} {category} consumers in your audience."
        }
        
        logger.info(f"✅ [BACKEND ACTION] *** SUCCESSFULLY RETURNING DATA *** with {len(scaled_brand_data)} brands")
        logger.info(f"🎯 [BACKEND ACTION] Result: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [BACKEND ACTION] Error in getBrandData: {str(e)}")
        raise

def handle_get_spending_data(**kwargs):
    category = kwargs.get("category")
    selected_brands = kwargs.get("selected_brands")
    logger.info(f"🚀 [BACKEND ACTION] *** getSpendingData CALLED *** with category: {category}, selected_brands: {selected_brands}")
    logger.info(f"🔥 [BACKEND ACTION] *** THIS IS A BACKEND ACTION - LLM SHOULD CALL THIS ***")
    logger.info(f"📊 [BACKEND DATA] Getting spending data for {category}")
    
    try:
        data = get_spending_data(category)
        
        result = {
            "chart_type": "spending_distribution",
            "data": data,
            "category": category,
            "selected_brands": selected_brands or [],
            "title": f"Spending Distribution (Last 30 Days)",
            "description": f"Spending patterns for {category} consumers your audience."
        }
        
        logger.info(f"✅ [BACKEND ACTION] *** SUCCESSFULLY RETURNING DATA *** with {len(data)} spending ranges")
        logger.info(f"🎯 [BACKEND ACTION] Result: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ [BACKEND ACTION] Error in getSpendingData: {str(e)}")
        raise

# Action 1: Get Purchase Recency Data
get_purchase_recency_data_action = CopilotAction(
    name="getPurchaseRecencyData",
    description="Get purchase recency distribution data for a specific product category",
    parameters=[{
        "name": "category",
        "type": "string",
        "description": "Product category to analyze (e.g., 'cookies', 'snacks', 'beverages')",
        "required": True
    }],
    handler=handle_get_purchase_recency_data
)

# Action 2: Get Brand Data
get_brand_data_action = CopilotAction(
    name="getBrandData",
    description="Get brand breakdown data for a specific product category",
    parameters=[{
        "name": "category",
        "type": "string",
        "description": "Product category being analyzed",
        "required": True
    }, {
        "name": "selected_recency",
        "type": "string",
        "description": "Previously selected recency period",
        "required": False
    }, {
        "name": "selected_recency_percentage",  # for calculating
        "type": "number",                      
        "description": "The combined percentage (0-100) of all selected recency periods.",
        "required": False
    }],
    handler=handle_get_brand_data
)

# Action 3: Get Spending Data
get_spending_data_action = CopilotAction(
    name="getSpendingData",
    description="Get spending distribution data for a specific product category",
    parameters=[{
        "name": "category",
        "type": "string",
        "description": "Product category being analyzed",
        "required": True
    }, {
        "name": "selected_brands",
        "type": "array",
        "description": "Previously selected brands",
        "required": False
    }],
    handler=handle_get_spending_data
)

# Action 4: Update Audience Insights
update_audience_insights_action = CopilotAction(
    name="updateAudienceInsights",
    description="Update audience insights with new consumer count and composition",
    parameters=[{
        "name": "total_consumers",
        "type": "number",
        "description": "Total number of consumers in the audience",
        "required": True
    }, {
        "name": "ingredients",
        "type": "array",
        "description": "List of audience ingredients",
        "required": False
    }],
    handler=lambda total_consumers, ingredients=None: {
        "total_consumers": total_consumers,
        "ingredients": ingredients or [],
        "message": f"Updated audience size: {total_consumers:,} consumers"
    }
)

# Action 5: Add Exclusion
add_exclusion_action = CopilotAction(
    name="addExclusion",
    description="Add exclusion criteria to remove certain consumer groups from the audience",
    parameters=[{
        "name": "exclusion_type",
        "type": "string",
        "description": "Type of exclusion (brand, category, behavior)",
        "required": True
    }, {
        "name": "label",
        "type": "string",
        "description": "Label for the exclusion",
        "required": True
    }, {
        "name": "percentage",
        "type": "number",
        "description": "Percentage of audience to exclude",
        "required": True
    }],
    handler=lambda exclusion_type, label, percentage: {
        "exclusion": {
            "id": f"exclusion_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": exclusion_type,
            "label": label,
            "percentage": percentage
        },
        "message": f"Added exclusion: {label} (-{percentage}%)"
    }
)

# Action 6: Add Filter
add_filter_action = CopilotAction(
    name="addFilter",
    description="Add filter criteria to refine the audience",
    parameters=[{
        "name": "filter_type",
        "type": "string",
        "description": "Type of filter (spending, location, frequency)",
        "required": True
    }, {
        "name": "label",
        "type": "string",
        "description": "Label for the filter",
        "required": True
    }, {
        "name": "value",
        "type": "string",
        "description": "Filter value",
        "required": True
    }],
    handler=lambda filter_type, label, value: {
        "filter": {
            "id": f"filter_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": filter_type,
            "label": label,
            "value": value
        },
        "message": f"Added filter: {label}"
    }
)

# Action 7: Create Final Audience
create_audience_action = CopilotAction(
    name="createAudience",
    description="Create the final audience with all selected criteria",
    parameters=[{
        "name": "audience_name",
        "type": "string",
        "description": "Name for the new audience",
        "required": True
    }, {
        "name": "audience_data",
        "type": "object",
        "description": "Complete audience data including insights, ingredients, exclusions, and filters",
        "required": True
    }],
    handler=lambda audience_name, audience_data: {
        "audience": {
            "id": f"audience_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "name": audience_name,
            "created_at": datetime.now().isoformat(),
            "data": audience_data
        },
        "message": f"Successfully created audience: {audience_name}"
    }
)

# Initialize the CopilotKit SDK with all actions
sdk = CopilotKitRemoteEndpoint(actions=[
    get_purchase_recency_data_action,
    get_brand_data_action,
    get_spending_data_action,
    update_audience_insights_action,
    add_exclusion_action,
    add_filter_action,
    create_audience_action
])

# Test the actions on startup
def test_actions():
    logger.info("🧪 [STARTUP TEST] Testing backend actions...")
    try:
        # Test getPurchaseRecencyData
        result = handle_get_purchase_recency_data(category="cookies")
        logger.info(f"✅ [STARTUP TEST] getPurchaseRecencyData works: {len(result['data'])} periods")
        
        # Test getBrandData
        result = handle_get_brand_data(category="cookies")
        logger.info(f"✅ [STARTUP TEST] getBrandData works: {len(result['data'])} brands")
        
        # Test getSpendingData
        result = handle_get_spending_data(category="cookies")
        logger.info(f"✅ [STARTUP TEST] getSpendingData works: {len(result['data'])} ranges")
        
        logger.info("✅ [STARTUP TEST] All actions working correctly!")
    except Exception as e:
        logger.error(f"❌ [STARTUP TEST] Action test failed: {str(e)}")

# Add the CopilotKit endpoint to your FastAPI app 
        
try:
    add_fastapi_endpoint(app, sdk, "/copilotkit_remote")
    print("✅ [SETUP] CopilotKit endpoint added successfully")
except Exception as e:
    print(f"❌ [SETUP] Failed to add CopilotKit endpoint: {e}")
    import traceback
    traceback.print_exc()

# troubleshooting the fastapi server - list all the routes
print("\n🚦 [ROUTES] Registered FastAPI routes:")
for route in app.router.routes:
    print(f"  - {getattr(route, 'path', str(route))} {getattr(route, 'methods', '')}")
print()


# Add middleware to log all requests
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"📨 [REQUEST] {request.method} {request.url.path} - Headers: {dict(request.headers)}")
    response = await call_next(request)
    logger.info(f"📤 [RESPONSE] {response.status_code} for {request.url.path}")
    return response

def main():
    """Run the uvicorn server."""
    logger.info("🚀 [SERVER] Starting CopilotKit server...")
    logger.info(f"📊 [SERVER] Registered {len(sdk.actions)} actions:")
    for action in sdk.actions:
        logger.info(f"  - {action.name}: {action.description}")
    
    port = int(os.environ.get("PORT", 8000))
    logger.info("🌍 [SERVER] Server will be available at:")
    logger.info(f"  - http://0.0.0.0:{port} - API documentation")
    logger.info(f"  - http://0.0.0.0:{port}/health - Health check")
    logger.info(f"  - http://0.0.0.0:{port}/copilotkit_remote - CopilotKit endpoint")
    
    # Test actions
    test_actions()
    
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False, log_level="info")
 
if __name__ == "__main__":
    main()