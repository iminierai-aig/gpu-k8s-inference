AI Infrastructure Skills Summary
Overview
This repository demonstrates hands-on experience with GPU-accelerated AI infrastructure, including Kubernetes orchestration, LLM inference serving, GPU monitoring, and HPC job scheduling.

Skills Demonstrated
Kubernetes & Container Orchestration
Deployed K3s single-node cluster on bare metal. Configured NVIDIA device plugin for GPU scheduling. Created deployments, services, and namespaces for AI workloads. Troubleshot container runtime issues (NVIDIA runtime handler, GPU operator compatibility).

LLM Inference Serving
Deployed vLLM inference server with OpenAI-compatible API. Tested SGLang and documented T4 GPU compatibility limitations. Understand PagedAttention vs RadixAttention trade-offs. Experience with model serving (microsoft/phi-2, 2.7B parameters).

GPU Monitoring & Observability
Deployed DCGM Exporter for GPU metrics collection. Configured Prometheus to scrape GPU metrics. Built Grafana dashboards (temperature, power, utilization, memory). Understand production monitoring patterns for AI workloads.

NCCL & Distributed Training
Ran NCCL collective operation benchmarks (AllReduce, AllGather). Measured GPU memory bandwidth (~121 GB/s on T4). Understand collective operations for distributed training.

HPC Job Scheduling (Slurm)
Configured Slurm with GPU GRES support. Submitted GPU jobs with resource requests. Understand SBATCH directives and job scripting.

Lab Environment
Component	Specification
Server	Dell R640
GPU	NVIDIA Tesla T4 (16 GB)
RAM	768 GB
Storage	2 TB NVMe
OS	Ubuntu 24.04 LTS
Kubernetes	K3s v1.34.4
Driver	NVIDIA 535.288.01
CUDA	12.2
Certifications
CKA (Certified Kubernetes Administrator) and NVIDIA NCA-AIIO (AI Infrastructure and Operations).
