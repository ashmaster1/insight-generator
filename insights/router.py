from fastapi import APIRouter, Depends, Body, Request
from pydantic import BaseModel
from .service import InsightsService

# Define the request body model
class InsightRequest(BaseModel):
    prompt: str

# Define a dependency to get the service
def get_insights_service(request: Request) -> InsightsService:
    return request.state.insights_service

router = APIRouter(
    prefix="/insights",
    tags=["insights"],
)

@router.post("/insights")
def get_insights(payload: InsightRequest = Body(...), insights_service: InsightsService = Depends(get_insights_service)):
    """Receives a prompt in the request body and returns insights."""
    return insights_service.get_insights(prompt=payload.prompt)