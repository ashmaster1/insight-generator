from fastapi import FastAPI
from insights.service import InsightsService
from insights.router import router as insights_router
from contextlib import asynccontextmanager
import uvicorn
@asynccontextmanager
async def lifespan(_: FastAPI):
    insights_service = InsightsService()
    yield {"insights_service": insights_service}

app = FastAPI(
    lifespan=lifespan,
)

app.include_router(insights_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Insight Generator API"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080, reload=True)

# We will include the insights router here later