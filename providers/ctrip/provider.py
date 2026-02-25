#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import threading
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Callable
from urllib.parse import urlencode

from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

TRAIN_LIST_URL = "https://trains.ctrip.com/webapp/train/list"
FLIGHT_LIST_URL_TEMPLATE = "https://flights.ctrip.com/online/list/oneway-{from_code}-{to_code}?depdate={date}"
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CITY_CODE_PATTERN = re.compile(r"^[A-Za-z]{3}$")

DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)


@dataclass(frozen=True)
class TrainQuery:
    from_station: str
    to_station: str
    date: str
    high_speed_only: int = 0
    ticket_type: int = 0


@dataclass(frozen=True)
class FlightQuery:
    from_code: str
    to_code: str
    date: str


class CtripScraper:
    def __init__(
        self,
        *,
        headless: bool = True,
        timeout_ms: int = 120_000,
        retries: int = 3,
    ) -> None:
        self._headless = headless
        self._timeout_ms = timeout_ms
        self._retries = retries
        self._lock = threading.RLock()

        self._pw = None
        self._browser: Browser | None = None

    def close(self) -> None:
        with self._lock:
            self._reset_browser()

    def search_train(self, query: TrainQuery) -> dict[str, Any]:
        self._validate_date(query.date)
        if query.high_speed_only not in (0, 1):
            raise ValueError("high_speed_only must be 0 or 1")

        params = {
            "ticketType": str(query.ticket_type),
            "dStation": query.from_station,
            "aStation": query.to_station,
            "dDate": query.date,
            "rDate": "",
            "trainsType": "",
            "hubCityName": "",
            "highSpeedOnly": str(query.high_speed_only),
        }
        url = f"{TRAIN_LIST_URL}?{urlencode(params)}"

        def work(page: Page) -> dict[str, Any]:
            page.goto(url, wait_until="domcontentloaded", timeout=self._timeout_ms)
            next_data = page.locator("script#__NEXT_DATA__").inner_text(timeout=20_000)
            payload = json.loads(next_data)
            state = payload["props"]["pageProps"]["initialState"]
            search_info = state["trainSearchInfo"]
            trains = search_info.get("trainInfoList", [])
            normalized = [self._normalize_train_item(item) for item in trains]
            return {
                "query": {
                    "from_station": query.from_station,
                    "to_station": query.to_station,
                    "date": query.date,
                    "ticket_type": query.ticket_type,
                    "high_speed_only": query.high_speed_only,
                },
                "source_url": url,
                "captured_at": datetime.now(UTC).isoformat(),
                "total": len(normalized),
                "trains": normalized,
            }

        return self._run_with_retry(work, op_name="train-search")

    def search_flight(self, query: FlightQuery) -> dict[str, Any]:
        self._validate_date(query.date)
        from_code = self._normalize_city_code(query.from_code)
        to_code = self._normalize_city_code(query.to_code)

        url = FLIGHT_LIST_URL_TEMPLATE.format(
            from_code=from_code.lower(),
            to_code=to_code.lower(),
            date=query.date,
        )

        def work(page: Page) -> dict[str, Any]:
            with page.expect_response(
                lambda resp: (
                    "/international/search/api/search/batchSearch" in resp.url
                    and resp.request.method == "POST"
                    and resp.status == 200
                ),
                timeout=self._timeout_ms,
            ) as event:
                page.goto(url, wait_until="domcontentloaded", timeout=self._timeout_ms)

            response = event.value
            payload = response.json()
            
            # Handle invalid date or empty response
            if "data" not in payload:
                error_msg = f"API returned no data field. Response: {payload}"
                if payload.get("status") == 0 and payload.get("msg") == "success":
                    error_msg += " (Date may be in the past or too far in future)"
                raise RuntimeError(error_msg)
            
            data = payload["data"]
            itineraries = data.get("flightItineraryList", [])
            normalized = [self._normalize_flight_itinerary(item) for item in itineraries]

            return {
                "query": {
                    "from_code": from_code,
                    "to_code": to_code,
                    "date": query.date,
                },
                "source_url": url,
                "batch_search_url": response.url,
                "captured_at": datetime.now(UTC).isoformat(),
                "total": len(normalized),
                "flights": normalized,
            }

        return self._run_with_retry(work, op_name="flight-search")

    def _run_with_retry(
        self,
        fn: Callable[[Page], dict[str, Any]],
        *,
        op_name: str,
    ) -> dict[str, Any]:
        failures: list[str] = []

        for attempt in range(1, self._retries + 1):
            try:
                return self._run_once(fn)
            except Exception as exc:
                failures.append(f"attempt {attempt}: {exc}")
                self._reset_browser()
                if attempt < self._retries:
                    time.sleep(1.2 * attempt)

        error_text = "; ".join(failures)
        raise RuntimeError(f"{op_name} failed after {self._retries} attempts: {error_text}")

    def _run_once(self, fn: Callable[[Page], dict[str, Any]]) -> dict[str, Any]:
        with self._lock:
            browser = self._get_browser()
            context: BrowserContext = browser.new_context(
                locale="zh-CN",
                timezone_id="Asia/Shanghai",
                user_agent=DEFAULT_UA,
                viewport={"width": 1440, "height": 2000},
            )
            page = context.new_page()
            try:
                return fn(page)
            finally:
                context.close()

    def _get_browser(self) -> Browser:
        if self._browser is not None:
            return self._browser

        self._pw = sync_playwright().start()
        self._browser = self._pw.chromium.launch(
            headless=self._headless,
            args=["--disable-blink-features=AutomationControlled"],
        )
        return self._browser

    def _reset_browser(self) -> None:
        if self._browser is not None:
            try:
                self._browser.close()
            except Exception:
                pass
            self._browser = None

        if self._pw is not None:
            try:
                self._pw.stop()
            except Exception:
                pass
            self._pw = None

    @staticmethod
    def _validate_date(date_str: str) -> None:
        if not DATE_PATTERN.match(date_str):
            raise ValueError("date must use YYYY-MM-DD format")

        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        # Check if date is in the past
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        if date_obj < today:
            raise ValueError(f"date {date_str} is in the past. Please use a future date.")

    @staticmethod
    def _normalize_city_code(code: str) -> str:
        code = code.strip().upper()
        if not CITY_CODE_PATTERN.match(code):
            raise ValueError("city code must be a 3-letter IATA city code, e.g. SHA, BJS")
        return code

    @staticmethod
    def _normalize_train_item(item: dict[str, Any]) -> dict[str, Any]:
        seats = []
        for seat in item.get("seatItemInfoList", []) or []:
            seats.append(
                {
                    "seat_name": seat.get("seatName"),
                    "seat_type_name": seat.get("seatTypeName"),
                    "price": seat.get("seatPrice"),
                    "inventory": seat.get("seatInventory"),
                    "bookable": bool(seat.get("seatBookable")),
                }
            )

        return {
            "train_number": item.get("trainNumber"),
            "train_no": item.get("trainNo"),
            "departure_station_name": item.get("departureStationName"),
            "arrival_station_name": item.get("arrivalStationName"),
            "departure_time": item.get("departureTime"),
            "arrival_time": item.get("arrivalTime"),
            "duration": item.get("duration"),
            "runtime_minutes": item.get("runTime"),
            "start_price": item.get("startPrice"),
            "bookable": bool(item.get("isBookable")),
            "seats": seats,
        }

    @staticmethod
    def _normalize_flight_itinerary(item: dict[str, Any]) -> dict[str, Any]:
        segments = item.get("flightSegments", []) or []
        first_segment = segments[0] if segments else {}
        flights = first_segment.get("flightList", []) or []
        first_flight = flights[0] if flights else {}

        prices = item.get("priceList", []) or []
        adult_prices = [
            int(price["adultPrice"])
            for price in prices
            if isinstance(price.get("adultPrice"), (int, float))
        ]
        lowest_price = min(adult_prices) if adult_prices else None

        return {
            "itinerary_id": item.get("itineraryId"),
            "flight_no": first_flight.get("flightNo"),
            "airline_name": (
                first_flight.get("marketAirlineName")
                or first_flight.get("airlineName")
                or first_segment.get("airlineName")
            ),
            "departure_city_name": first_flight.get("departureCityName"),
            "arrival_city_name": first_flight.get("arrivalCityName"),
            "departure_airport_name": first_flight.get("departureAirportName"),
            "arrival_airport_name": first_flight.get("arrivalAirportName"),
            "departure_datetime": first_flight.get("departureDateTime"),
            "arrival_datetime": first_flight.get("arrivalDateTime"),
            "duration_minutes": first_segment.get("duration"),
            "transfer_count": first_segment.get("transferCount"),
            "stop_count": first_segment.get("stopCount"),
            "lowest_adult_price": lowest_price,
            "price_option_count": len(prices),
        }
