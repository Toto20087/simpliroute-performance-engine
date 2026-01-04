import asyncio
import uuid
import time
import logging
from typing import List
from fastapi import APIRouter
from src.api.models import OptimizationRequest, OptimizationResponse
from src.core.decorators import monitor_performance
from src.core.context_managers import MockStorageConnection
from src.core.solver import LocalVRPSolver

# Setup Logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/optimize", response_model=OptimizationResponse)
@monitor_performance
async def optimize_route(request: OptimizationRequest):
    """
    Optimizes route using Google OR-Tools (Local Engine).
    """
    logger.info("Starting local optimization with OR-Tools...")
    start_total = time.perf_counter()
    
    if not request.stops:
         return OptimizationResponse(
            route_id="empty", 
            optimized_order=[], 
            total_distance_km=0.0,
            estimated_travel_time_minutes=0.0,
            execution_time_seconds=0.0,
            status="error_empty"
        )
    
    # 1. Prepare Data for Solver
    # Handle Explicit Depot logic
    if request.depot:
        # If depot is explicit, it becomes index 0
        all_points = [request.depot] + request.stops
    else:
        # Legacy: request.stops[0] is the depot
        if not request.stops:
             return OptimizationResponse(
                route_id="empty", 
                optimized_order=[], 
                total_distance_km=0.0,
                execution_time_seconds=0.0,
                status="error_empty"
            )
        all_points = request.stops
    
    locations = [(p.lat, p.lng) for p in all_points]
    
    # 2. Initialize Solver
    # We assume 1 Vehicle starting at index 0 (which is now correctly the depot)
    solver = LocalVRPSolver(vehicles=1, depot=0)
    
    # Run the math in a threadpool to avoid blocking the Async Event Loop
    # (Constraint Solving is CPU intensive)
    loop = asyncio.get_event_loop()
    solution = await loop.run_in_executor(None, solver.solve, locations)
    
    end_total = time.perf_counter()
    duration = end_total - start_total
    
    # 3. Parse Result
    if solution["status"] == "optimized":
        # The solver returns indices [0, 2, 1, 3, 0].
        # We match these back to the addresses in 'all_points'.
        optimized_indices = solution["route_indices"]
        final_addresses = [all_points[i].address for i in optimized_indices]
        
        # Calculate Estimated Time
        # Assumption: Average City Speed = 25 km/h
        avg_speed_kmh = 25.0
        estimated_hours = solution["total_distance_km"] / avg_speed_kmh
        estimated_minutes = round(estimated_hours * 60, 2)
        
        result = OptimizationResponse(
            route_id=str(uuid.uuid4()),
            optimized_order=final_addresses,
            total_distance_km=round(solution["total_distance_km"], 2),
            estimated_travel_time_minutes=estimated_minutes,
            execution_time_seconds=duration,
            status="optimized_local_ortools"
        )
        logger.info(f"Optimization successful: {solution['total_distance_km']} km")
    else:
        # Fallback if solver fails (rare for simple cases)
        logger.warning("Solver found no solution.")
        result = OptimizationResponse(
            route_id="solver_fail",
            optimized_order=[s.address for s in request.stops],
            total_distance_km=0.0,
            estimated_travel_time_minutes=0.0,
            execution_time_seconds=duration,
            status="no_solution"
        )

    # Audit Log
    with MockStorageConnection() as storage:
        storage.save_log(result.dict())
        
    return result
