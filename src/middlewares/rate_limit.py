import time
from falcon import HTTPTooManyRequests

class RateLimit:
    def __init__(self, limit=60, window=60):

        self.limit = limit
        self.window = window
        self.calls = {} 

    def process_request(self, req, resp):
        client_ip = req.remote_addr or "unknown"
        now = time.time()

        if client_ip not in self.calls:
            self.calls[client_ip] = []

        self.calls[client_ip] = [t for t in self.calls[client_ip] if t > now - self.window]

        if len(self.calls[client_ip]) >= self.limit:
            raise HTTPTooManyRequests(
                description=f"Rate limit exceeded. Try again in {int(self.window)}s."
            )

        self.calls[client_ip].append(now)
