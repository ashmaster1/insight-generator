from fastapi import FastAPI, Depends
from insights.service import InsightsService
from insights.router import router as insights_router
from contextlib import asynccontextmanager
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create the service instance
    insights_service = InsightsService()
    # Set it in the app state
    app.state.insights_service = insights_service
    yield
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