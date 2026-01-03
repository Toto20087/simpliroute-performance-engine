import time
import functools
import logging

# Configure basic logging if not already configured
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def monitor_performance(func):
    """
    Decorator to measure the execution time of an async function.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        func_name = func.__name__
        logger.info(f"Starting execution of {func_name}")
        
        try:
            result = await func(*args, **kwargs)
            end_time = time.perf_counter()
            duration = end_time - start_time
            logger.info(f"Finished {func_name} in {duration:.4f} seconds")
            return result
        except Exception as e:
            logger.error(f"Error in {func_name}: {str(e)}")
            raise e
            
    return wrapper
