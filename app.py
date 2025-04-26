from fastapi import FastAPI, Depends
from insights.service import InsightsService
from insights.router import router as insights_router
from insights.business_insights_agent import BusinessInsightsAgent
from insights.sql_generation_agent import SQLGenerationAgent
from contextlib import asynccontextmanager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the service instance
    business_insights_agent = BusinessInsightsAgent(bq_project_id="marketfeed-stage", gemini_api_key="AIzaSyBqoN0HnXFg5s3VJZdHUPBwLEPK4O2j83I")
    sql_generation_agent = SQLGenerationAgent(gemini_api_key="AIzaSyBqoN0HnXFg5s3VJZdHUPBwLEPK4O2j83I")
    insights_service = InsightsService(business_insights_agent, sql_generation_agent)
    
    yield {
        "insights_service": insights_service
    }
    # Cleanup (if needed)
    app.state.insights_service = None

app = FastAPI(
    lifespan=lifespan,
)

app.include_router(insights_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Insight Generator API"}

@app.get("/get-insight")
async def get_insight(insights_service: InsightsService = Depends(lambda: app.state.insights_service)):
    """
    Endpoint to get an insight.
    
    Returns:
        dict: A dictionary containing the generated SQL query
    """
    # enhanced_prompt = "SELECT all data from users table"  # You can modify this prompt
    sql_query = insights_service.generate_sql()
    return {"sql_query": sql_query}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)

# We will include the insights router here later