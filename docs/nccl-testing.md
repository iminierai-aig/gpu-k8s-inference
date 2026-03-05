# NCCL Testing Guide

## What is NCCL?

NCCL (NVIDIA Collective Communications Library) optimizes multi-GPU and multi-node communication for deep learning workloads. It implements collective operations like AllReduce, AllGather, Broadcast, and ReduceScatter.

## Why NCCL Matters

- Essential for distributed training across multiple GPUs
- Optimizes data transfer over NVLink, PCIe, and InfiniBand
- Used by PyTorch, TensorFlow, and all major frameworks
- Critical skill for AI infrastructure roles

## Collective Operations

| Operation | Description | Use Case |
|-----------|-------------|----------|
| AllReduce | Reduce data across all ranks, distribute result to all | Gradient synchronization in data parallel training |
| AllGather | Gather data from all ranks to all ranks | Model parallel inference |
| Broadcast | Send data from one rank to all others | Weight initialization |
| ReduceScatter | Reduce data, scatter results across ranks | Gradient sharding |

## Running NCCL Tests

Using NVIDIA PyTorch container (recommended):

```bash
docker run --rm --gpus all nvcr.io/nvidia/pytorch:24.01-py3 \
  bash -c "cd /opt && git clone https://github.com/NVIDIA/nccl-tests.git && \
  cd nccl-tests && make -j && \
  ./build/all_reduce_perf -b 8 -e 256M -f 2 -g 1"

## Test Results - Tesla T4 Single GPU

### AllReduce Performance

| Size | Bandwidth |
|------|-----------|
| 256KB | 50 GB/s |
| 1MB | 90 GB/s |
| 8MB | 118 GB/s |
| 256MB | 121 GB/s |

### AllGather Performance

| Size | Bandwidth |
|------|-----------|
| 256KB | 48 GB/s |
| 1MB | 88 GB/s |
| 16MB | 122 GB/s |
| 134MB | 121 GB/s |

## Interpreting Results

- algbw (Algorithm Bandwidth): Actual data throughput in GB/s
- busbw (Bus Bandwidth): Normalized bandwidth for collective overhead
- For single GPU, busbw shows 0 because no actual bus transfer occurs

## Multi-GPU Expectations

- NVLink: 300-600 GB/s depending on generation
- PCIe Gen4: 25 GB/s per direction
- InfiniBand HDR: 200 GB/s

## Interview Talking Points

1. NCCL optimizes collective operations for distributed training
2. AllReduce is critical for data parallel training gradient sync
3. Bandwidth scales with message size due to fixed overhead
4. Multi-GPU training requires understanding NVLink vs PCIe topology
5. NCCL tests help diagnose interconnect bottlenecks
