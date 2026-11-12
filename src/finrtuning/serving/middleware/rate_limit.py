"""Rate limiting middleware for Finr-Tuning API."""

from fastapi import Request, HTTPException
from collections import defaultdict
import time


class RateLimiter:
    """Simple rate limiter."""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        """Initialize rate limiter."""
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: defaultdict = defaultdict(list)
    
    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed."""
        current_time = time.time()
        window_start = current_time - self.window_seconds
        
        # Clean old requests
        self.requests[client_id] = [
            t for t in self.requests[client_id] if t > window_start
        ]
        
        # Check rate limit
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # Record new request
        self.requests[client_id].append(current_time)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """Get remaining requests in current window."""
        current_time = time.time()
        window_start = current_time - self.window_seconds
        
        requests_in_window = [
            t for t in self.requests[client_id] if t > window_start
        ]
        return max(0, self.max_requests - len(requests_in_window))


rate_limiter = RateLimiter(max_requests=100, window_seconds=60)


async def rate_limit(request: Request):
    """Rate limit middleware."""
    client_id = request.client.host
    if not rate_limiter.is_allowed(client_id):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please try again later.",
        )
    return request