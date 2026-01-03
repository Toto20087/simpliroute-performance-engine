from pydantic import BaseModel
from typing import List, Optional

class DeliveryPoint(BaseModel):
    lat: float
    lng: float
    address: str

class OptimizationRequest(BaseModel):
    stops: List[DeliveryPoint]

class OptimizationResponse(BaseModel):
    route_id: str
    optimized_order: List[str] # List of addresses in optimized order
    total_distance_km: float
    execution_time_seconds: float
    status: str
