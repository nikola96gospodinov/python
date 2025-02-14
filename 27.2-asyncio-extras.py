import asyncio
from typing import Optional, Any
import signal
import logging

logger = logging.getLogger(__name__)

class AsyncApplication:
    def __init__(self) -> None:
        self.loop: Optional[asyncio.AbstractEventLoop] = None
        self._shutdown_requested = False
        
    async def shutdown(self, signal: Optional[signal.Signals] = None) -> None:
        """Graceful shutdown"""
        if signal:
            logger.info(f"Received exit signal {signal.name}")
        
        self._shutdown_requested = True
        
        # Example cleanup tasks
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        
        logger.info(f"Cancelling {len(tasks)} outstanding tasks")
        for task in tasks:
            task.cancel()
            
        await asyncio.gather(*tasks, return_exceptions=True)
        if self.loop:
            self.loop.stop()
        
    def handle_exception(self, loop: asyncio.AbstractEventLoop, context: dict[str, Any]) -> None:
        """Handle exceptions outside of coroutines"""
        msg = context.get("exception", context["message"])
        logger.error(f"Caught exception: {msg}")
        
        # Optionally initiate shutdown
        if not self._shutdown_requested:
            logger.info("Shutting down due to exception...")
            asyncio.create_task(self.shutdown())
            
    async def startup(self) -> None:
        """Initialise application"""
        self.loop = asyncio.get_running_loop()
        
        # Set up signal handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            self.loop.add_signal_handler(
                sig,
                lambda s=sig: asyncio.create_task(self.shutdown(s))  # type: ignore
            )
            
        # Set up exception handler
        self.loop.set_exception_handler(self.handle_exception)
        
    async def run(self) -> None:
        await self.startup()
        try:
            # Your main application logic here
            while not self._shutdown_requested:
                await asyncio.sleep(1)
        finally:
            await self.shutdown()
            
# Usage
if __name__ == "__main__":
    app = AsyncApplication()
    asyncio.run(app.run())