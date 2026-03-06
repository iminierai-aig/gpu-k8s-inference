# vLLM Load Test Results

## Test Environment
- **Server**: Dell R640
- **GPU**: NVIDIA Tesla T4 (16GB)
- **Model**: microsoft/phi-2 (2.7B parameters)
- **Max Tokens**: 50
- **Date**: March 6, 2026

## Results Summary

### Single Request Latency
| Metric | Value |
|--------|-------|
| Average Latency | 1.87s |
| Min Latency | ~1.86s |
| Max Latency | ~1.89s |
| Tokens Generated | 50 |

### Throughput at Different Concurrency Levels
| Concurrency | Requests | Total Time | Throughput |
|-------------|----------|------------|------------|
| 1 | 10 | 18.7s | 0.53 req/s |
| 2 | 10 | 9.4s | 1.06 req/s |
| 5 | 20 | 7.6s | 2.61 req/s |
| 10 | 30 | 5.7s | 5.21 req/s |

## Key Insights

1. **Latency is consistent**: ~1.87s per request regardless of concurrency
2. **Throughput scales with concurrency**: 5.21 req/s at concurrency 10
3. **GPU memory efficient**: vLLM's PagedAttention enables concurrent requests
4. **T4 handles production loads**: 5+ requests/second is viable for many use cases

## Tokens Per Second
At 50 tokens per request and 5.21 req/s:
- **~260 tokens/second** throughput at concurrency 10

## Interview Talking Points
- "I benchmarked vLLM on a Tesla T4 and achieved 5.2 requests/second at concurrency 10"
- "Latency stayed consistent at ~1.9 seconds even under load due to PagedAttention"
- "The T4 delivered approximately 260 tokens/second with phi-2"
