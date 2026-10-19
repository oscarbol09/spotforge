"""Unit tests for sliding window rate limiter."""

from app.services.rate_limiter import SlidingWindowRateLimiter


def test_rate_limiter_allows_under_limit():
    limiter = SlidingWindowRateLimiter(max_requests=3, window_seconds=60)
    client = "192.168.1.50"

    allowed1, _ = limiter.is_allowed(client)
    allowed2, _ = limiter.is_allowed(client)
    allowed3, _ = limiter.is_allowed(client)

    assert allowed1 is True
    assert allowed2 is True
    assert allowed3 is True


def test_rate_limiter_blocks_on_excess():
    limiter = SlidingWindowRateLimiter(max_requests=2, window_seconds=60)
    client = "10.0.0.1"

    limiter.is_allowed(client)
    limiter.is_allowed(client)

    allowed, retry_after = limiter.is_allowed(client)
    assert allowed is False
    assert retry_after > 0


def test_rate_limiter_isolates_different_ips():
    limiter = SlidingWindowRateLimiter(max_requests=1, window_seconds=60)
    client_a = "1.1.1.1"
    client_b = "2.2.2.2"

    allowed_a1, _ = limiter.is_allowed(client_a)
    allowed_a2, _ = limiter.is_allowed(client_a)
    allowed_b1, _ = limiter.is_allowed(client_b)

    assert allowed_a1 is True
    assert allowed_a2 is False
    assert allowed_b1 is True


def test_rate_limiter_global_daily_ceiling():
    limiter = SlidingWindowRateLimiter(max_requests=10, window_seconds=60, max_global_daily=2)

    allowed1, _ = limiter.is_allowed("ip-1")
    allowed2, _ = limiter.is_allowed("ip-2")
    allowed3, retry_after = limiter.is_allowed("ip-3")

    assert allowed1 is True
    assert allowed2 is True
    assert allowed3 is False
    assert retry_after > 0

