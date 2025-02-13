import time
import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

# # Synchronous (blocking) code
# def make_coffee() -> str:
#     print("Starting to make coffee...")
#     time.sleep(2) # Blocking operation
#     return "Coffee ready!"

# def make_toast() -> str:
#     print("Starting to make toast...")
#     time.sleep(3) # Blocking operation
#     return "Toast ready!"

# def breakfast_sync() -> List[str]:
#     start = time.time()
#     coffee = make_coffee()
#     toast = make_toast()
#     duration = time.time() - start
#     print(f"Total time: {duration:.2f} seconds")
#     return [coffee, toast]

# results = breakfast_sync() # takes 5 seconds

# # It's important that these functions are asynchronous. These are called coroutine functions
# async def make_coffee_async() -> str:
#     print("Starting to make coffee...")
#     await asyncio.sleep(2)  # Adding await is crucial
#     return "Coffee ready!"

# async def make_toast_async() -> str:
#     print("Starting to make toast...")
#     await asyncio.sleep(3)  # Adding await is crucial 
#     return "Toast ready!"

# async def breakfast_async() -> List[str]:
#     start = time.time()
    
#     # Create tasks to run concurrently
#     coffee_task: asyncio.Task[str] = asyncio.create_task(make_coffee_async())
#     toast_task: asyncio.Task[str] = asyncio.create_task(make_toast_async())
    
#     # Wait for both tasks to complete
#     coffee, toast = await asyncio.gather(coffee_task, toast_task)
    
#     duration = time.time() - start
#     print(f"Total time: {duration:.2f} seconds")
#     return [coffee, toast]

# results2 = asyncio.run(breakfast_async()) # takes 3 seconds

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AsyncOperation:
    def __init__(self, name: str, duration: float) -> None:
        self.name = name
        self.duration = duration
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        
    async def execute(self) -> Dict[str, Any]:
        """Execute an async operation with proper logging and error handling."""
        try:
            self.start_time = datetime.now()
            logger.info(f"Starting operation: {self.name}")
            
            # Simulate some async work
            await asyncio.sleep(self.duration)
            
            self.end_time = datetime.now()
            duration = (self.end_time - self.start_time).total_seconds()
            
            return {
                "name": self.name,
                "status": "completed",
                "duration": duration,
                "start_time": self.start_time,
                "end_time": self.end_time
            }
            
        except Exception as e:
            logger.error(f"Error in operation {self.name}: {str(e)}")
            return {
                "name": self.name,
                "status": "failed",
                "error": str(e)
            }
            
async def process_operation(operations: List[AsyncOperation]) -> List[Dict[str, Any]]:
    """Process multiple operations concurrently with proper error handling."""
    try:
        # Create a task for all operations
        tasks = [
            asyncio.create_task(op.execute()) for op in operations
        ]
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results and handle any exceptions
        processed_results: List[Dict[str, Any]] = []
        for result in results:
            if isinstance(result, (Exception, BaseException)):
                processed_results.append({
                    "status": "failed",
                    "error": str(result)
                })
            else:
                processed_results.append(result)
                
        return processed_results
    
    except Exception as e:
        logger.error(f"Error in process_operations: {str(e)}")
        raise
    
async def main() -> None:
    operations = [
        AsyncOperation("Operation 1", 2.0),
        AsyncOperation("Operation 2", 1.5),
        AsyncOperation("Operation 3", 3.0)
    ]
    
    try:
        results = await process_operation(operations)
        
        # Print results in formatted way
        for result in results:
            if result["status"] == "completed":
                logger.info(f"Operation {result["name"]} completed in {result["duration"]:2f} seconds")
            else:
                logger.error(f"Operation {result["name"]} failed: {result["error"]}")
                
    except Exception as e:
        logger.error(f"Main execution failed: {str(e)}")
        
if __name__ == "__main__":
    asyncio.run(main())