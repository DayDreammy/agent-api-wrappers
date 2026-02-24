"""
Ctrip (携程) Provider

Provides flight and hotel search capabilities for Ctrip.com
"""

import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.base import BaseProvider


class CtripProvider(BaseProvider):
    """
    Ctrip API Provider
    
    Features:
    - Flight search
    - Hotel search (planned)
    
    Limitations:
    - No booking capability (read-only)
    - May require handling anti-bot measures
    """
    
    name = "ctrip"
    version = "1.0.0"
    author = "@DayDreammy"
    required_config = []  # No login required for search
    
    BASE_URL = "https://www.ctrip.com"
    FLIGHT_SEARCH_URL = "https://flights.ctrip.com/online/channel/domestic"
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self._playwright = None
        self._browser = None
        self._page = None
    
    async def _init_browser(self):
        """Initialize browser if not already done."""
        if self._page is None:
            from playwright.async_api import async_playwright
            
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-dev-shm-usage']
            )
            self._page = await self._browser.new_page()
            await self._page.set_viewport_size({"width": 1920, "height": 1080})
    
    async def close(self):
        """Clean up browser resources."""
        if self._page:
            await self._page.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
    
    async def health_check(self) -> bool:
        """Check if Ctrip is accessible."""
        try:
            await self._init_browser()
            await self._page.goto(self.BASE_URL, wait_until="networkidle")
            return "ctrip" in await self._page.title().lower()
        except Exception:
            return False
    
    async def search_flights(
        self,
        origin: str,
        destination: str,
        date: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search for flights on Ctrip.
        
        Args:
            origin: Origin city code (e.g., "SHA" for Shanghai)
            destination: Destination city code (e.g., "PEK" for Beijing)
            date: Departure date in YYYY-MM-DD format
            **kwargs: Additional search parameters
                - adult: Number of adults (default: 1)
                - child: Number of children (default: 0)
        
        Returns:
            List of flight dictionaries containing:
            - airline: Airline name
            - flight_no: Flight number
            - dep_time: Departure time
            - arr_time: Arrival time
            - dep_airport: Departure airport
            - arr_airport: Arrival airport
            - price: Price in CNY
            - duration: Flight duration
        
        Example:
            >>> provider = CtripProvider()
            >>> flights = await provider.search_flights("SHA", "PEK", "2026-03-01")
            >>> print(flights[0])
            {
                'airline': 'China Eastern',
                'flight_no': 'MU5101',
                'dep_time': '08:00',
                'arr_time': '10:15',
                'dep_airport': 'SHA',
                'arr_airport': 'PEK',
                'price': 850,
                'duration': '2h 15m'
            }
        """
        await self._init_browser()
        
        # Format date for Ctrip URL
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        date_str = date_obj.strftime("%Y-%m-%d")
        
        # Build search URL
        search_url = (
            f"{self.FLIGHT_SEARCH_URL}?"
            f"dep={origin}&arr={destination}&depDate={date_str}"
        )
        
        try:
            # Navigate to search page
            await self._page.goto(search_url, wait_until="networkidle")
            
            # Wait for flight results to load
            await self._page.wait_for_selector(".flight-item", timeout=30000)
            
            # Extract flight data
            flights = await self._page.evaluate("""
                () => {
                    const flights = [];
                    const items = document.querySelectorAll('.flight-item');
                    items.forEach(item => {
                        const airline = item.querySelector('.airline-name')?.textContent?.trim();
                        const flightNo = item.querySelector('.flight-no')?.textContent?.trim();
                        const depTime = item.querySelector('.dep-time')?.textContent?.trim();
                        const arrTime = item.querySelector('.arr-time')?.textContent?.trim();
                        const depAirport = item.querySelector('.dep-airport')?.textContent?.trim();
                        const arrAirport = item.querySelector('.arr-airport')?.textContent?.trim();
                        const priceText = item.querySelector('.price')?.textContent?.trim();
                        const duration = item.querySelector('.duration')?.textContent?.trim();
                        
                        if (airline && flightNo) {
                            flights.push({
                                airline,
                                flight_no: flightNo,
                                dep_time: depTime,
                                arr_time: arrTime,
                                dep_airport: depAirport,
                                arr_airport: arrAirport,
                                price: parseInt(priceText?.replace(/[^0-9]/g, '') || 0),
                                duration
                            });
                        }
                    });
                    return flights;
                }
            """)
            
            return flights
            
        except Exception as e:
            # Take screenshot for debugging
            await self._page.screenshot(path=f"ctrip_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise Exception(f"Failed to search flights: {str(e)}")
    
    async def search_hotels(
        self,
        city: str,
        checkin: str,
        checkout: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search for hotels on Ctrip. (Planned feature)
        
        Args:
            city: City name or code
            checkin: Check-in date (YYYY-MM-DD)
            checkout: Check-out date (YYYY-MM-DD)
        
        Returns:
            List of hotel dictionaries
        """
        raise NotImplementedError("Hotel search is planned but not yet implemented")


# Convenience function for quick usage
async def search_flights(origin: str, destination: str, date: str) -> List[Dict[str, Any]]:
    """
    Quick search function without initializing provider.
    
    Args:
        origin: Origin city code
        destination: Destination city code
        date: Departure date (YYYY-MM-DD)
    
    Returns:
        List of flight results
    """
    async with CtripProvider() as provider:
        return await provider.search_flights(origin, destination, date)
