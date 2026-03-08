#!/bin/bash
# Test script for FastAPI wrapper

API_URL="http://localhost:8080"
API_KEY="sk-demo-key-12345"

echo "=== Testing vLLM API Gateway ==="
echo ""

# Test 1: Health check (no auth required)
echo "1. Health Check:"
curl -s $API_URL/health | jq .
echo ""

# Test 2: Root endpoint
echo "2. API Info:"
curl -s $API_URL/ | jq .
echo ""

# Test 3: Completion without auth (should fail)
echo "3. Completion without auth (expect 401):"
curl -s -X POST $API_URL/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello", "max_tokens": 10}' | jq .
echo ""

# Test 4: Completion with auth
echo "4. Completion with auth:"
curl -s -X POST $API_URL/v1/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_KEY" \
  -d '{"prompt": "What is Kubernetes?", "max_tokens": 50}' | jq .
echo ""

# Test 5: Get stats
echo "5. Request Stats:"
curl -s $API_URL/stats \
  -H "Authorization: Bearer $API_KEY" | jq .
echo ""

echo "=== Tests Complete ==="