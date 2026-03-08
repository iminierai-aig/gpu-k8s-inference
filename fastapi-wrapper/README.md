# FastAPI Wrapper for vLLM

Production-ready API gateway for vLLM inference with authentication, rate limiting, logging, and request tracking.

## Features

- **API Key Authentication**: Bearer token auth for all completion endpoints
- **Rate Limiting**: Configurable requests per minute (default: 60 RPM)
- **Request Logging**: Detailed logging with request IDs
- **Stats Tracking**: Total requests, tokens, latency metrics
- **Health Checks**: Monitor vLLM backend status
- **CORS Support**: Cross-origin requests enabled

## Quick Start

```bash
# Ensure vLLM is running on port 8000
kubectl port-forward -n ai-lab svc/vllm-service 8000:8000 &

# Start the API gateway
cd fastapi-wrapper
source venv/bin/activate
python main.py

Configuration
Environment variables:

Variable	Default	Description
VLLM_URL	http://localhost:8000	vLLM backend URL
API_KEY	sk-demo-key-12345	API authentication key
RATE_LIMIT_RPM	60	Max requests per minute

API Endpoints

Endpoint	Method	Auth	Description
/health	GET	No	Health check
/stats	GET	Yes	Request statistics
/v1/completions	POST	Yes	Generate completion
/	GET	No	API info

Usage Examples

Health Check
curl http://localhost:8080/health

Generate Completion

curl -X POST http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-demo-key-12345" \
  -d '{"prompt": "Explain AI:", "max_tokens": 50}'

Get Stats

curl http://localhost:8080/stats \
  -H "Authorization: Bearer sk-demo-key-12345"

Interview Talking Points
API gateways add security layer between clients and inference backend
Rate limiting prevents abuse and ensures fair resource usage
Request tracking enables monitoring and debugging in production
Health checks enable load balancer integration
Stateless design allows horizontal scaling of gateway layer