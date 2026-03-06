#!/bin/bash

# vLLM Load Test Script
# Tests latency and throughput at different concurrency levels

ENDPOINT="http://localhost:8000/v1/completions"
MODEL="microsoft/phi-2"
MAX_TOKENS=50
PROMPT="Explain the benefits of cloud computing in simple terms:"

echo "=========================================="
echo "vLLM Load Test - $(date)"
echo "Model: $MODEL"
echo "Max Tokens: $MAX_TOKENS"
echo "=========================================="
echo ""

# Function to run single request and measure time
single_request() {
    start=$(date +%s.%N)
    response=$(curl -s $ENDPOINT \
        -H "Content-Type: application/json" \
        -d "{\"model\": \"$MODEL\", \"prompt\": \"$PROMPT\", \"max_tokens\": $MAX_TOKENS}")
    end=$(date +%s.%N)
    
    latency=$(echo "$end - $start" | bc)
    tokens=$(echo $response | jq -r '.usage.completion_tokens // 0')
    echo "$latency $tokens"
}

# Function to run concurrent requests
run_concurrent() {
    concurrency=$1
    requests=$2
    
    echo "--- Concurrency: $concurrency, Requests: $requests ---"
    
    start_time=$(date +%s.%N)
    
    for i in $(seq 1 $requests); do
        single_request &
        
        # Limit concurrent jobs
        while [ $(jobs -r | wc -l) -ge $concurrency ]; do
            sleep 0.1
        done
    done
    
    wait
    
    end_time=$(date +%s.%N)
    total_time=$(echo "$end_time - $start_time" | bc)
    throughput=$(echo "scale=2; $requests / $total_time" | bc)
    
    echo "Total time: ${total_time}s"
    echo "Throughput: ${throughput} req/s"
    echo ""
}

# Warmup
echo "Warming up..."
single_request > /dev/null
single_request > /dev/null
echo "Warmup complete"
echo ""

# Test 1: Single request latency (10 requests)
echo "=== Test 1: Single Request Latency ==="
total_latency=0
for i in $(seq 1 10); do
    result=$(single_request)
    latency=$(echo $result | awk '{print $1}')
    tokens=$(echo $result | awk '{print $2}')
    echo "Request $i: ${latency}s, ${tokens} tokens"
    total_latency=$(echo "$total_latency + $latency" | bc)
done
avg_latency=$(echo "scale=3; $total_latency / 10" | bc)
echo "Average latency: ${avg_latency}s"
echo ""

# Test 2: Concurrent requests
echo "=== Test 2: Concurrent Requests ==="
run_concurrent 2 10
run_concurrent 5 20
run_concurrent 10 30

echo "=========================================="
echo "Load test complete"
echo "=========================================="
