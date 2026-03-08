#!/usr/bin/env python3
"""
FastAPI Wrapper for vLLM
Adds logging, request tracking, rate limiting, and basic auth
"""

import os
import time
import uuid
import logging
from datetime import datetime
from typing import Optional
from functools import wraps

from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

# Configuration
VLLM_URL = os.getenv("VLLM_URL", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "sk-demo-key-12345")
RATE_LIMIT_RPM = int(os.getenv("RATE_LIMIT_RPM", "60"))

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Request tracking
request_stats = {
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "total_tokens": 0,
    "total_latency_ms": 0
}

# Rate limiting storage (in production, use Redis)
rate_limit_store = {}

app = FastAPI(
    title="vLLM API Gateway",
    description="Production-ready wrapper for vLLM inference",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class CompletionRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7
    model: str = "microsoft/phi-2"

class CompletionResponse(BaseModel):
    id: str
    text: str
    model: str
    tokens_used: int
    latency_ms: float

class HealthResponse(BaseModel):
    status: str
    vllm_status: str
    uptime_seconds: float
    total_requests: int

# Startup time
START_TIME = time.time()

# Auth dependency
async def verify_api_key(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing API key")
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth format")
    
    token = authorization.replace("Bearer ", "")
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    
    return token

# Rate limiting dependency
async def check_rate_limit(request: Request):
    client_ip = request.client.host
    current_minute = int(time.time() / 60)
    
    key = f"{client_ip}:{current_minute}"
    
    if key not in rate_limit_store:
        rate_limit_store[key] = 0
    
    rate_limit_store[key] += 1
    
    if rate_limit_store[key] > RATE_LIMIT_RPM:
        raise HTTPException(
            status_code=429, 
            detail=f"Rate limit exceeded. Max {RATE_LIMIT_RPM} requests per minute."
        )
    
    # Cleanup old entries
    old_keys = [k for k in rate_limit_store if int(k.split(":")[1]) < current_minute - 1]
    for k in old_keys:
        del rate_limit_store[k]

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    vllm_status = "unknown"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{VLLM_URL}/health", timeout=5.0)
            vllm_status = "healthy" if response.status_code == 200 else "unhealthy"
    except Exception:
        vllm_status = "unreachable"
    
    return HealthResponse(
        status="healthy",
        vllm_status=vllm_status,
        uptime_seconds=time.time() - START_TIME,
        total_requests=request_stats["total_requests"]
    )

@app.get("/stats")
async def get_stats(api_key: str = Depends(verify_api_key)):
    """Get request statistics"""
    avg_latency = 0
    if request_stats["successful_requests"] > 0:
        avg_latency = request_stats["total_latency_ms"] / request_stats["successful_requests"]
    
    return {
        **request_stats,
        "average_latency_ms": round(avg_latency, 2)
    }

@app.post("/v1/completions", response_model=CompletionResponse)
async def create_completion(
    request: CompletionRequest,
    api_key: str = Depends(verify_api_key),
    _rate_limit: None = Depends(check_rate_limit)
):
    """Generate text completion with logging and tracking"""
    request_id = str(uuid.uuid4())[:8]
    request_stats["total_requests"] += 1
    
    logger.info(f"[{request_id}] New request - prompt length: {len(request.prompt)}, max_tokens: {request.max_tokens}")
    
    start_time = time.time()
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{VLLM_URL}/v1/completions",
                json={
                    "model": request.model,
                    "prompt": request.prompt,
                    "max_tokens": request.max_tokens,
                    "temperature": request.temperature
                },
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
        
        latency_ms = (time.time() - start_time) * 1000
        tokens_used = result.get("usage", {}).get("completion_tokens", 0)
        
        request_stats["successful_requests"] += 1
        request_stats["total_tokens"] += tokens_used
        request_stats["total_latency_ms"] += latency_ms
        
        logger.info(f"[{request_id}] Success - tokens: {tokens_used}, latency: {latency_ms:.0f}ms")
        
        return CompletionResponse(
            id=request_id,
            text=result["choices"][0]["text"],
            model=request.model,
            tokens_used=tokens_used,
            latency_ms=round(latency_ms, 2)
        )
        
    except httpx.TimeoutException:
        request_stats["failed_requests"] += 1
        logger.error(f"[{request_id}] Timeout after 60s")
        raise HTTPException(status_code=504, detail="vLLM request timeout")
        
    except Exception as e:
        request_stats["failed_requests"] += 1
        logger.error(f"[{request_id}] Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """API info"""
    return {
        "name": "vLLM API Gateway",
        "version": "1.0.0",
        "endpoints": ["/health", "/stats", "/v1/completions"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
