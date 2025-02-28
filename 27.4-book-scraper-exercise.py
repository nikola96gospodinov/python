import asyncio
import aiohttp
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
import logging
from pathlib import Path

BASE_URL = "http://books.toscrape.com"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class Category:
    name: str
    url: str
    id: int
    
@dataclass
class Book:
    title: str
    price: float
    availability: int
    rating: int
    
def spelled_out_number_to_numerical(value: str) -> int:
    match value.lower():
        case "one":
            return 1
        case "two":
            return 2
        case "three":
            return 3
        case "four":
            return 4
        case "five":
            return 5
        case _:
            return 0
    
class BookScraper:
    def __init__(self, base_url: str = BASE_URL) -> None:
        self.base_url = base_url
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def connect(self) -> None:
        self.session = aiohttp.ClientSession()
        
    async def close(self) -> None:
        if self.session:
            await self.session.close()
        
    async def get_page_content(self, url: str = BASE_URL) -> str:
        if not self.session:
            raise RuntimeError("Session not initialized")
            
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                text = await response.text()
                return text
        except Exception as e:
            logger.error(f"Failed to get page content: {e}")
            raise
    
    async def get_categories(self) -> List[Category]:
        html = await self.get_page_content()
        soup = BeautifulSoup(html, "html.parser")
        category_links = soup.select(".side_categories ul li ul li a")
        
        categories: List[Category] = []
        for category in category_links:
            name = category.get_text(strip=True)
            url = f"{self.base_url}/{category.get("href")}"
            id = len(categories) + 2
            categories.append(Category(name, url, id))
            
        return categories
        
    
    async def scrape_book_page(self, url: str) -> Book:
        html = await self.get_page_content(url)
        soup = BeautifulSoup(html, "html.parser")
        
        title = soup.select_one("h1").get_text(strip=True)
        price = float(soup.select_one(".price_color").get_text(strip=True))
        availability_text = soup.select_one(".availability").get_text(strip=True)
        availability = int(''.join(filter(str.isdigit, availability_text)))
        rating = spelled_out_number_to_numerical(soup.select_one(".star-rating").get("class").split(" ")[1])
        
        return Book(title, price, availability, rating)
    
    async def scrape_category_page(self, category: Category, page: int = 1) -> None:
        url = f"{self.base_url}/catalogue/category/books/{category.name.lower()}_{category.id}/page-{page}.html"
        html = await self.get_page_content(url)
        soup = BeautifulSoup(html, "html.parser")
        category_books = soup.select(".product_pod h3 a")
        print(category_books)
        
        books: List[Book] = []
        for category_book in category_books:
            url = category_book.get('href')
            book = await self.scrape_book_page(str(url))
            books.append(book)
    
    async def scrape_all(self, max_concurrent: int = 3) -> None:
        categories = await self.get_categories()
        tasks = [
            asyncio.create_task(self.scrape_category_page(categories[i])) for i in range(1, max_concurrent)
        ]
        results = await asyncio.gather(*tasks)
        for result in results:
            if isinstance(result, (Exception, BaseException)):
                print(f"Error for: {result}")
            else:
                print(f"Result: {result}")
    
async def main():
    scraper = BookScraper()
    try:
        await scraper.connect()
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise
    finally:
        await scraper.close()
    
if __name__ == "__main__":
    asyncio.run(main())