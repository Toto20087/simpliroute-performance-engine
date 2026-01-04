import os
import time
from celery import Celery
from src.core.solver import LocalVRPSolver

# Initialize Celery
# We use Redis as both the Broker (Queue) and Backend (Result Storage)
redis_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "simpliroute_engine",
    broker=redis_url,
    backend=redis_url
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

@celery_app.task(bind=True)
def optimize_route_task(self, locations: list, depot_index: int = 0):
    """
    Background Task that runs the heavy OR-Tools optimization.
    """
    
    # Initialize Solver
    solver = LocalVRPSolver(vehicles=1, depot=depot_index)
    
    # Run Optimization (CPU Intensive)
    solution = solver.solve(locations)
    
    # Return raw dict (Celery will Serialize it to JSON)
    return solution
