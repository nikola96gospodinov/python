import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, TypedDict, Literal, Mapping
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SortProperties = Literal["created", "updated", "pushed", "full_name"]
Direction = Literal["asc", "desc"]

class UserRepoQueryParams(TypedDict, total=False):
    per_page: int
    page: int
    sort: SortProperties
    direction: Direction

class RateLimitExceeded(Exception):
    """Custom exception for rate limit handling."""
    pass

MAX_RETRIES = 3
BASE_DELAY = 1

class GitHubClient:
    def __init__(self) -> None:
        self.base_url = "https://api.github.com"
        self.session: Optional[aiohttp.ClientSession] = None
        self._requests: List[datetime] = []
        
    async def connect(self) -> None:
        """Initialise HTTP session."""
        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=aiohttp.ClientTimeout(total=30)
        )
        logger.info("GitHub client session initialised")
        
    async def close(self) -> None:
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            logger.info("GitHub client session closed")
        
    async def _check_rate_limit(self) -> None:
        """
        Check if the rate limit has been reached.
        The limit is 60 requests per hour
        """
        self._requests = [request for request in self._requests if (datetime.now() - request).total_seconds() < 3600]
        if len(self._requests) > 60:
            raise RateLimitExceeded("Rate limit exceeded")
        
    async def _make_request(self, method: str, url: str, **kwargs) -> Any:
        """
        Make an API request with:
            - retry logic
            - rate limiting
        """
        if not self.session:
            raise RuntimeError("API client not connected")
        
        await self._check_rate_limit()
        
        for attempt in range(MAX_RETRIES):
            try:
                async with self.session.request(method, url, **kwargs) as response:
                    response.raise_for_status()
                    self._requests.append(datetime.now())
                    
                    return await response.json()
                
            except aiohttp.ClientResponseError as e:
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Failed after {MAX_RETRIES} attempts: {e}")
                    raise
                
                delay = BASE_DELAY * (2 ** attempt)
                logger.warning(f"Request failed, retrying in {delay}s: {e}")
                await asyncio.sleep(delay)

            except aiohttp.ClientError as e:
                logger.error(f"Request failed: {e}")
                raise
                
        
    
    async def get_user(self, username: str) -> Dict[str, Any]:
        logger.info(f"Fetching user data for {username}")
        return await self._make_request("GET", f"/users/{username}")
        
    async def get_user_repos(self, username: str, query_params: Optional[UserRepoQueryParams] = None) -> List[Dict[str, Any]]:
        logger.info(f"Fetching repositories for {username}")
        return await self._make_request("GET", f"/users/{username}/repos", params=query_params)
    
    async def fetch_user_data(self, username: str) -> Dict[str, Any]:
        """
        Fetch both user data and repositories concurrently.
        """
        logger.info(f"Starting concurrent fetch for {username}")
        
        try:
            user_data, user_repos = await asyncio.gather(
                self.get_user(username),
                self.get_user_repos(username, None)
            )
            
            return {
                "user": user_data,
                "repositories": user_repos
            }
            
        except Exception as e:
            logger.error(f"Failed to fetch data for {username}: {e}")
            raise
        
async def main():
    client = GitHubClient()
    try:
        await client.connect()
        result = await client.get_user_repos("nikola96gospodinov")
        print(result)
    except RateLimitExceeded:
        logger.error("Rate limit exceeded, try again later")
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
    finally:
        await client.close()
        
if __name__ == "__main__":
    asyncio.run(main())