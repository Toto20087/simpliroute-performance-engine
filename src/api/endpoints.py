import uuid
import logging
from fastapi import APIRouter, HTTPException, Depends
from src.api.models import OptimizationRequest, OptimizationResponse, TaskResponse, TaskResult
from src.core.decorators import monitor_performance
from src.celery_worker.celery_app import optimize_route_task
from celery.result import AsyncResult

# Setup Logger
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/optimize", response_model=TaskResponse)
@monitor_performance
async def optimize_route(request: OptimizationRequest):
    """
    Submit optimization task to Celery (Async).
    """
    logger.info("Received optimization request. Enqueuing task...")
    
    # 1. Prepare Data
    if request.depot:
        all_points = [request.depot] + request.stops
    else:
        if not request.stops:
             raise HTTPException(status_code=400, detail="No stops provided")
        all_points = request.stops
    
    # Serialize to simple list of tuples for Celery (JSON serializable)
    locations = [(p.lat, p.lng) for p in all_points]
    
    # 2. Submit to Celery
    task = optimize_route_task.delay(locations, depot_index=0)
    
    logger.info(f"Task Enqueued: {task.id}")
    
    return TaskResponse(
        task_id=task.id,
        status="PROCESSING"
    )

@router.get("/tasks/{task_id}", response_model=TaskResult)
async def get_task_status(task_id: str):
    task_result = AsyncResult(task_id)
    
    if task_result.state == 'PENDING':
        return TaskResult(task_id=task_id, status="PROCESSING")
    
    elif task_result.state == 'SUCCESS':
        # Result is the dict returned by solver.solve()
        solution = task_result.result
        
        # Reconstruct Response
        # NOTE: In a real app we would persist 'all_points' to DB to map back addresses.
        # For this demo, we can't map back addresses easily in a stateless GET.
        # TRICK: We will return the raw indices and let the Frontend map them!
        
        # To make this robust without DB, we need the frontend to hold the state of "What stops did I send?"
        # The solver returns: {"route_indices": [0, 2, 1, ...], "distance": ...}
        
        return TaskResult(
            task_id=task_id,
            status="SUCCESS",
            result=OptimizationResponse(
                route_id=str(uuid.uuid4()),
                optimized_order=[str(i) for i in solution["route_indices"]], # Returning INDICES as strings
                total_distance_km=round(solution["total_distance_km"], 2),
                estimated_travel_time_minutes=round((solution["total_distance_km"]/25.0)*60, 2),
                execution_time_seconds=0.0, # Not tracked in async same way
                status="optimized_celery"
            )
        )
        
    elif task_result.state == 'FAILURE':
        return TaskResult(task_id=task_id, status="FAILURE")
    
    return TaskResult(task_id=task_id, status="PROCESSING")
