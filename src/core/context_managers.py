import json
import logging
from typing import Any, Dict
from datetime import datetime

logger = logging.getLogger(__name__)

class MockStorageConnection:
    """
    Context Manager to simulate a connection to cloud storage (e.g., S3).
    Saves logs to a local JSON file.
    """
    def __init__(self, filename="logs.json"):
        self.filename = filename

    def __enter__(self):
        logger.info("Opening secure connection to storage...")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        logger.info("Closing connection to storage...")
        if exc_type:
            logger.error(f"An error occurred: {exc_value}")
        # Return False to propagate exceptions
        return False

    def save_log(self, data: Dict[str, Any]):
        """
        Simulates saving a log entry to the cloud.
        """
        try:
            # Add timestamp
            data["timestamp"] = datetime.utcnow().isoformat()
            
            # Read existing logs
            try:
                with open(self.filename, "r") as f:
                    logs = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                logs = []
            
            logs.append(data)
            
            # Write back
            with open(self.filename, "w") as f:
                json.dump(logs, f, indent=4)
                
            logger.info(f"Log saved successfully to {self.filename}")
            
        except Exception as e:
            logger.error(f"Failed to save log: {str(e)}")
            raise e
