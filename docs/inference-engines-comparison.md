# Inference Engines Comparison: vLLM vs SGLang

## Overview

| Feature | vLLM | SGLang |
|---------|------|--------|
| Primary Innovation | PagedAttention | RadixAttention |
| KV Cache Management | Paged memory blocks | Radix tree for prefix sharing |
| Best For | General inference serving | Complex multi-turn, branching |
| Hardware Support | Broad (T4, A100, H100) | Newer GPUs preferred (sm80+) |
| API | OpenAI-compatible | OpenAI-compatible |
| Maturity | Production-ready | Rapidly evolving |

## PagedAttention (vLLM)

How it works:
- Divides KV cache into fixed-size blocks (like virtual memory pages)
- Allocates blocks on-demand, reducing memory waste
- Enables efficient memory sharing across sequences

Benefits:
- 2-4x higher throughput than naive implementations
- Near-zero memory waste
- Efficient batching of variable-length sequences

Use cases:
- High-throughput API serving
- Batch inference workloads
- Production deployments with diverse hardware

## RadixAttention (SGLang)

How it works:
- Uses radix tree to store and reuse KV cache across requests
- Automatically identifies shared prefixes between prompts
- Enables efficient branching and multi-turn conversations

Benefits:
- Excellent for shared system prompts
- Efficient multi-turn conversations
- Fast prefix caching

Use cases:
- Chatbots with shared system prompts
- Agentic workflows with branching
- Applications with repeated prompt patterns

## Practical Experience

### vLLM Deployment (Successful)

Deployed on K3s with Tesla T4 GPU (16GB). Model: microsoft/phi-2 (2.7B parameters). Memory usage approximately 17GB. Latency under 100ms for short prompts.

### SGLang Deployment (Compatibility Issue)

Issue encountered: CUDA graph capture failed due to T4 compute capability (sm75). SGLang flashinfer backend requires sm80+ for some features.

Resolution options:
1. Use --disable-cuda-graph flag (performance impact)
2. Use A100/H100 GPUs (sm80+)
3. Use vLLM for broader hardware compatibility

## When to Choose Which

| Scenario | Recommendation |
|----------|----------------|
| Production API serving | vLLM |
| Diverse GPU fleet | vLLM |
| Multi-turn chatbots | SGLang |
| Shared prompt patterns | SGLang |
| Older GPUs (T4, V100) | vLLM |
| Cutting-edge GPUs (H100) | Either |

## Interview Talking Points

1. I have deployed both vLLM and SGLang on Kubernetes with hands-on experience

2. I understand the trade-offs between PagedAttention and RadixAttention

3. I can troubleshoot GPU compatibility issues including sm75 vs sm80 CUDA graph requirements

4. I know when to use each engine based on use case and hardware constraints
