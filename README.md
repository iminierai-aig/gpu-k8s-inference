# GPU-Accelerated LLM Inference on Kubernetes

Deploy vLLM inference servers on Kubernetes with NVIDIA GPU support.

## Prerequisites

- Kubernetes cluster (K3s, K8s, or managed)
- NVIDIA GPU with drivers installed
- NVIDIA Container Toolkit
- NVIDIA Device Plugin for Kubernetes

## Quick Start

```bash
# Create namespace
kubectl create namespace ai-lab

# Deploy vLLM
kubectl apply -f manifests/vllm-deployment.yaml

# Verify GPU allocation
kubectl get pods -n ai-lab

# Port-forward and test
kubectl port-forward -n ai-lab svc/vllm-service 8000:8000 &

curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "microsoft/phi-2", "prompt": "Hello!", "max_tokens": 50}'

Lab Environment
Component	Specification
Server	Dell R640
GPU	NVIDIA Tesla T4 (16GB)
RAM	768GB
OS	Ubuntu 24.04 LTS
Kubernetes	K3s v1.34.4
CUDA	12.2
Skills Demonstrated
Kubernetes deployment and service configuration
NVIDIA GPU integration with Kubernetes
LLM inference server deployment (vLLM)
OpenAI-compatible API serving
Author
Johnny - Solutions Engineer | CKA Certified | NVIDIA NCA-AIIO
