from typing import Optional, Dict, Any

import redis
import requests
from itsdangerous import URLSafeTimedSerializer


# Constants for Redis configuration and CBR API URL
REDIS_HOST: str = "redis"
REDIS_PORT: int = 6379
REDIS_DB: int = 0
CBR_API_URL: str = "https://www.cbr-xml-daily.ru/daily_json.js"

# Initialize the Redis client
REDIS_CLIENT: redis.Redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class SessionManager:
    def __init__(self, secret_key: str):
        self.serializer = URLSafeTimedSerializer(secret_key)

    def create_session_id(self) -> str:
        return self.serializer.dumps({})

    def validate_session_id(self, session_id: str) -> bool:
        try:
            self.serializer.loads(session_id)
            return True
        except:
            return False


def get_cached_usd_rate() -> Optional[float]:
    """Retrieve the cached USD exchange rate from Redis."""
    rate = REDIS_CLIENT.get("usd_rate")
    return float(rate) if rate else None


def cache_usd_rate(rate: float) -> None:
    """Cache the USD exchange rate in Redis for 24 hours."""
    REDIS_CLIENT.setex("usd_rate", 86400, str(rate))


def fetch_usd_rate_from_api() -> float:
    """Fetch the current USD exchange rate from the CBR API."""
    response = requests.get(CBR_API_URL)
    data: Dict[str, Any] = response.json()
    return data["Valute"]["USD"]["Value"]


def get_usd_exchange_rate() -> float:
    """Get the USD exchange rate either from cache or fetch from the API."""
    cached_rate = get_cached_usd_rate()
    if cached_rate is not None:
        return cached_rate
    usd_rate = fetch_usd_rate_from_api()
    cache_usd_rate(usd_rate)
    return usd_rate


def calculate_delivery_cost(weight: float, content_value_cents: int) -> int:
    """
    Calculate the delivery cost based on weight, content value in cents, and USD exchange rate.
    Both the content value and the delivery cost are in cents.
    """
    usd_rate = get_usd_exchange_rate()

    # Convert USD rate to a cents-based rate for consistency
    usd_rate_cents = usd_rate * 100

    # Calculate the delivery cost in cents
    delivery_cost_cents = int(
        (weight * 0.5 + content_value_cents * 0.01) * usd_rate_cents
    )

    return delivery_cost_cents
