"""In-memory sliding window rate limiter for public demo protection."""

import logging
import threading
import time
from collections import defaultdict

logger = logging.getLogger(__name__)


class SlidingWindowRateLimiter:
    """Thread-safe sliding-window rate limiter per client identifier (IP address)."""

    def __init__(self, max_requests: int = 5, window_seconds: int = 300):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._lock = threading.Lock()
        self._request_history: dict[str, list[float]] = defaultdict(list)
        self._last_cleanup = time.time()

    def is_allowed(self, client_id: str) -> tuple[bool, int]:
        """Check whether a client request is allowed under the current window.
        
        Returns:
            (allowed: bool, retry_after_seconds: int)
        """
        now = time.time()
        window_start = now - self.window_seconds

        with self._lock:
            # Periodic cleanup of stale client keys every 10 minutes
            if now - self._last_cleanup > 600:
                self._cleanup_stale(window_start)
                self._last_cleanup = now

            timestamps = self._request_history[client_id]
            # Prune timestamps older than window
            valid_timestamps = [t for t in timestamps if t > window_start]
            self._request_history[client_id] = valid_timestamps

            if len(valid_timestamps) >= self.max_requests:
                # Oldest timestamp in window determines retry-after
                oldest_in_window = valid_timestamps[0]
                retry_after = max(1, int((oldest_in_window + self.window_seconds) - now))
                return False, retry_after

            # Record this request
            valid_timestamps.append(now)
            return True, 0

    def _cleanup_stale(self, cutoff: float) -> None:
        """Remove clients with no requests in the current window."""
        stale_keys = [
            k for k, timestamps in self._request_history.items()
            if not timestamps or timestamps[-1] <= cutoff
        ]
        for k in stale_keys:
            del self._request_history[k]

    def reset(self) -> None:
        """Clear all rate limiting records (useful for test isolation)."""
        with self._lock:
            self._request_history.clear()
            self._last_cleanup = time.time()


_global_limiter: SlidingWindowRateLimiter | None = None


def get_rate_limiter(max_requests: int = 5, window_seconds: int = 300) -> SlidingWindowRateLimiter:
    """Get or create singleton rate limiter instance."""
    global _global_limiter
    if _global_limiter is None:
        _global_limiter = SlidingWindowRateLimiter(
            max_requests=max_requests,
            window_seconds=window_seconds,
        )
    return _global_limiter
