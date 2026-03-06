TensorRT-LLM Notes
What is TensorRT-LLM?
TensorRT-LLM is NVIDIA's high-performance inference library that compiles LLMs into optimized TensorRT engines. It delivers maximum throughput and lowest latency on NVIDIA GPUs, particularly H100 and A100.

Key Features
TensorRT-LLM provides state-of-the-art optimizations including in-flight batching, paged KV cache, tensor parallelism, and quantization (INT8, FP8, INT4). It supports major model architectures (LLaMA, GPT, Falcon, etc.) and offers an OpenAI-compatible API via trtllm-serve.

Hardware Requirements
TensorRT-LLM requires compute capability sm80 or higher for full functionality. This means A100, H100, L40S, or newer GPUs. Older GPUs like the Tesla T4 (sm75) are not fully supported because they lack bfloat16 support required by the PyTorch backend.

Tested on Tesla T4
Attempted to run TensorRT-LLM 1.3.0rc6 on Tesla T4 (compute capability 7.5). Result: Failed with error "Unsupported data type, pre SM 80 GPUs do not support bfloat16". The T4 is too old for current TensorRT-LLM versions.

Inference Engine Comparison
Engine	T4 (sm75)	A100/H100 (sm80+)	Best Use Case
vLLM	Works	Works	Broad hardware support, production
SGLang	Limited	Works	Multi-turn chat, prefix caching
TensorRT-LLM	No	Yes	Maximum performance
Interview Talking Points
Production AI inference requires understanding hardware constraints. vLLM offers the best compatibility across GPU generations. TensorRT-LLM delivers highest performance but requires modern GPUs (A100/H100). When designing inference architecture, match the engine to available hardware.

Commands Reference
Pull TensorRT-LLM container: docker run --rm --gpus all --ipc=host --ulimit memlock=-1 --ulimit stack=67108864 nvcr.io/nvidia/tensorrt-llm/release:1.3.0rc6 bash

Serve a model: trtllm-serve serve MODEL_NAME --port 8080 --backend pytorch
