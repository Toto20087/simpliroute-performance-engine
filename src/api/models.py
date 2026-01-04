from pydantic import BaseModel
from typing import List, Optional

class DeliveryPoint(BaseModel):
    lat: float
    lng: float
    address: str

class OptimizationRequest(BaseModel):
    depot: Optional[DeliveryPoint] = None
    stops: List[DeliveryPoint]

class OptimizationResponse(BaseModel):
    route_id: str
    optimized_order: List[str] # List of addresses in optimized order
    total_distance_km: float
    estimated_travel_time_minutes: float # New Metric
    execution_time_seconds: float
    status: str
