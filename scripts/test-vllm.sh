#!/bin/bash
# Test vLLM inference endpoint

echo "Testing vLLM completions endpoint..."
curl -s http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "microsoft/phi-2",
    "prompt": "Explain Kubernetes in one sentence:",
    "max_tokens": 50
  }' | jq .

echo ""
echo "Testing model list..."
curl -s http://localhost:8000/v1/models | jq .
