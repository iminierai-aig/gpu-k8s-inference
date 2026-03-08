# Kubernetes Autoscaling for LLM Inference

## Overview

This document covers Horizontal Pod Autoscaler (HPA) configuration for vLLM inference workloads on Kubernetes.

## HPA Configuration

The HPA monitors CPU utilization and scales pods between 1-3 replicas based on a 70% CPU threshold.

### Key Settings

| Setting | Value | Purpose |
|---------|-------|---------|
| minReplicas | 1 | Minimum pods running |
| maxReplicas | 3 | Maximum pods allowed |
| targetCPU | 70% | Scale up threshold |
| scaleUpWindow | 30s | Stabilization before scaling up |
| scaleDownWindow | 120s | Stabilization before scaling down |

## GPU Constraints

With a single GPU, autoscaling is limited because each vLLM pod requires a GPU. In production with multiple GPUs, HPA enables automatic scaling based on demand.

### Single GPU Behavior
- HPA correctly detects high CPU and attempts scale-up
- Pending pods wait for GPU availability
- System gracefully handles resource constraints

### Multi-GPU Production Setup
With N GPUs, set maxReplicas to N for full autoscaling capability.

## Observed Behavior

| Phase | CPU | Replicas | Notes |
|-------|-----|----------|-------|
| Model loading | 105% | 2 (1 pending) | HPA detected spike |
| Idle | 2% | 1 | Scaled down |
| Under load | 70%+ | Up to maxReplicas | Scales based on demand |

## Custom Metrics (Advanced)

For GPU-based autoscaling, use DCGM metrics with Prometheus Adapter:

1. Deploy Prometheus Adapter
2. Configure custom metrics API
3. Create HPA targeting nvidia.com/gpu_utilization

Example custom metric HPA (requires additional setup):
```yaml
metrics:
- type: Pods
  pods:
    metric:
      name: DCGM_FI_DEV_GPU_UTIL
    target:
      type: AverageValue
      averageValue: "70"

Interview Talking Points
HPA enables automatic scaling based on resource utilization
GPU workloads require one GPU per pod - maxReplicas should match available GPUs
CPU-based HPA works but GPU utilization metrics provide better signals for inference workloads
Stabilization windows prevent thrashing during load spikes
In production, combine HPA with Cluster Autoscaler for node-level scaling