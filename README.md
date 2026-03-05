# GPU-Accelerated LLM Inference on Kubernetes

Deploy vLLM inference servers on Kubernetes with NVIDIA GPU support and full observability stack.

## Components

### Inference
- **vLLM**: High-throughput LLM serving with PagedAttention
- **Model**: microsoft/phi-2 (2.7B parameters)
- **API**: OpenAI-compatible endpoints

### Monitoring
- **DCGM Exporter**: NVIDIA GPU metrics (utilization, memory, temperature, power)
- **Prometheus**: Metrics collection and storage
- **Grafana**: Real-time dashboards

## Quick Start

### Deploy vLLM

```bash
kubectl create namespace ai-lab
kubectl apply -f manifests/vllm-deployment.yaml
kubectl get pods -n ai-lab
```

## Deploy Monitoring Stack

kubectl create namespace monitoring
kubectl apply -f manifests/dcgm-exporter.yaml
kubectl apply -f manifests/prometheus.yaml
kubectl apply -f manifests/grafana.yaml
kubectl get pods -n monitoring

Testing vLLM
```
kubectl port-forward -n ai-lab svc/vllm-service 8000:8000 &

curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "microsoft/phi-2", "prompt": "Hello!", "max_tokens": 50}'
```

Accessing Grafana
```
kubectl port-forward -n monitoring svc/grafana 3000:3000 --address 0.0.0.0 &
```

URL: http://server-ip:3000
Username: admin
Password: admin123

## GPU Metrics Available

| Metric | Description |
|--------|-------------|
| DCGM_FI_DEV_GPU_TEMP | GPU Temperature (C) |
| DCGM_FI_DEV_POWER_USAGE | Power Draw (W) |
| DCGM_FI_DEV_GPU_UTIL | GPU Utilization (%) |
| DCGM_FI_DEV_FB_USED | GPU Memory Used (MB) |

## Lab Environment

| Component | Specification |
|-----------|---------------|
| Server | Dell R640 |
| GPU | NVIDIA Tesla T4 (16GB) |
| RAM | 768GB |
| Storage | 2TB NVMe |
| OS | Ubuntu 24.04 LTS |
| Kubernetes | K3s v1.34.4 |
| Driver | NVIDIA 535.288.01 |
| CUDA | 12.2 |

Skills Demonstrated

Kubernetes deployment and service configuration
NVIDIA GPU integration with Kubernetes
LLM inference server deployment (vLLM)
GPU monitoring with DCGM, Prometheus, Grafana
OpenAI-compatible API serving
Production observability patterns

Author
Johnny - Solutions Engineer | CKA Certified | NVIDIA NCA-AIIO

License
MIT
