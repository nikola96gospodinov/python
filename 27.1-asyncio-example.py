import asyncio
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime
import aiohttp
import asyncpg  # type: ignore
from dataclasses import dataclass
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class User:
    id: int
    name: str
    email: str
    created_at: datetime
    
class DatabaseClient:
    def __init__(self, dsn: str) -> None:
        self.dsn = dsn
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self) -> None:
        """Initialise database connection pool."""
        try:
            self.pool = await asyncpg.create_pool(
                self.dsn,
                min_size=5,  # min_size represents the minimum number of connections in the pool
                max_size=20  # max_size represents the maximum number of connections allowed in the pool
            )
            logger.info("Database connection pool created")
        except Exception as e:
            logger.error(f"Failed to create a database pool: {e}")
            raise
        
    async def close(self) -> None:
        """Close database connection pool."""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
    
    @asynccontextmanager
    async def transaction(self):
        """Asynchronous context manager for handling a database transaction."""
        if not self.pool:
            raise RuntimeError("Database not connected")
        
        async with self.pool.acquire() as connection:
            async with connection.transaction():
                yield connection
                
    async def store_users(self, users: List[User]) -> None:
        """Store users in database."""
        try:
            async with self.transaction() as conn:
                # Prepare the insert statement
                statement = """
                    INSERT INTO users (id, name, email, created_at)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT (id) DO UPDATE
                    SET name = EXCLUDED.name,
                        email = EXCLUDED.email,
                        updated_at = NOW()
                """
                
                # Execute in batch
                await conn.executemany(
                    statement,
                    [(user.id, user.name, user.email, user.created_at) for user in users]
                )
                
                logger.info(f"Stored {len(users)} users in database")
        except Exception as e:
            logger.error(f"Failed to store users: {e}")
            raise
        
class APIClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def connect(self) -> None:
        """Initialise HTTP session."""
        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        
    async def close(self) -> None:
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            
    async def fetch_users(self, page: int = 1) -> List[User]:
        """Fetch users from API."""
        if not self.session:
            raise RuntimeError("API client not connected")
        
        try:
            async with self.session.get(
                f"/api/users",
                params={"page": page}
            ) as response:
                # This checks the HTTP response status. If the status code indicates an error (e.g., 4xx or 5xx),
                # it raises an exception so that errors can be handled appropriately.
                response.raise_for_status()
                data = await response.json()
                
                return [
                    User(
                        id=user["id"],
                        name=user["name"],
                        email=user["email"],
                        created_at=datetime.fromtimestamp(user["created_at"])
                    )
                    for user in data["users"]
                ]
                
        except aiohttp.ClientError as e:
            logger.error(f"API request failed: {e}")
            raise
        
class UserSyncService:
    def __init__(self, db_client: DatabaseClient, api_client: APIClient) -> None:
        self.db = db_client
        self.api = api_client
        
    async def syn_users(self, max_pages: int = 5) -> None:
        """Sync users from API to database"""
        try:
            # Create tasks for each page
            tasks = [
                self.api.fetch_users(page) for page in range(1, max_pages + 1)
            ]
            
            # Fetch all pages concurrently
            user_pages = await asyncio.gather(*tasks)
            
            # Flatten the list of users
            all_pages = (page for page in user_pages)
            all_users = (user for user in all_pages)
            
            # Store users in db
            await self.db.store_users(*all_users)
            
            logger.info(f"Successfully synced {len(*all_users)} users from {max_pages} pages")
            
        except Exception as e:
            logger.error(f"User syn failed: {e}")
            raise
        
async def main():
    # Initialise clients
    db_client = DatabaseClient(dsn="postgresql://user:password@localhost:5432/dbname")
    api_client = APIClient(base_url="https://api.example.com")
    
    try:
        # Connect to service
        await asyncio.gather(
            db_client.connect(),
            api_client.connect()
        )
        
        # Create sync service and run sync
        sync_service = UserSyncService(db_client, api_client)
        await sync_service.syn_users()
        
    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
    
    finally:
        # Clean up connections
        await asyncio.gather(
            db_client.close(),
            api_client.close()
        )
        
if __name__ == "__main__":
    asyncio.run(main())