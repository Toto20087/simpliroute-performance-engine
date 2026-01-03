import asyncio
import uuid
import time
from typing import List
from fastapi import APIRouter
from src.api.models import OptimizationRequest, OptimizationResponse
from src.core.decorators import monitor_performance
from src.core.context_managers import MockStorageConnection

router = APIRouter()

@router.post("/optimize", response_model=OptimizationResponse)
@monitor_performance
async def optimize_route(request: OptimizationRequest):
    """
    Simulates a heavy route optimization process.
    """
    # Start internal timer for response payload
    start = time.perf_counter()

    # Simulate processing delay (async non-blocking)
    await asyncio.sleep(2)
    
    # Mock logic: just reverse the order as a simple "optimization"
    optimized_stops = request.stops[::-1]
    optimized_addresses = [stop.address for stop in optimized_stops]
    
    # Mock specific metrics
    distance = len(request.stops) * 1.5  # Fake math
    route_id = str(uuid.uuid4())
    
    end = time.perf_counter()
    duration = end - start

    result = {
        "route_id": route_id,
        "input_stops_count": len(request.stops),
        "total_distance_km": distance,
         "optimized_order": optimized_addresses
    }
    
    # Use the context manager to save the audit trail
    with MockStorageConnection() as storage:
        storage.save_log(result)
        
    return OptimizationResponse(
        route_id=route_id,
        optimized_order=optimized_addresses,
        total_distance_km=distance,
        execution_time_seconds=duration,
        status="success"
    )
