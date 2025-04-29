from fastapi import APIRouter, Depends, Body, Request
from pydantic import BaseModel
from .service import InsightsService

# Define the request body model
class InsightRequest(BaseModel):
    prompt: str
    elaboration: str = None

class InsightElaborationRequest(BaseModel):
    prompt: str

# Define a dependency to get the service
def get_insights_service(request: Request) -> InsightsService:
    return request.state.insights_service

router = APIRouter(
    prefix="/insights",
    tags=["insights"],
)

@router.post("/elaborate")
def elaborate_insights(payload: InsightElaborationRequest = Body(...), insights_service: InsightsService = Depends(get_insights_service)):
    """Receives a prompt in the request body and returns elaborated insights."""
    return insights_service.elaborate_business_head_query(user_query=payload.prompt)

@router.post("/")
def get_insights(payload: InsightRequest = Body(...), insights_service: InsightsService = Depends(get_insights_service)):
    """Receives a prompt in the request body and returns insights."""
    return insights_service.get_insights(prompt=payload.prompt, elaboration=payload.elaboration)