# Slurm GPU Scheduling Guide

## What is Slurm?

Slurm (Simple Linux Utility for Resource Management) is the leading job scheduler for HPC clusters and AI training infrastructure. It manages compute resources, queues jobs, and allocates GPUs across nodes.

## Why Slurm Matters for AI/ML

- Used by major AI labs (Meta, Google, OpenAI) for training clusters
- Schedules GPU resources across thousands of nodes
- Integrates with NCCL for distributed training
- Supports multi-node, multi-GPU job allocation

## Key Slurm Commands

| Command | Description |
|---------|-------------|
| `sinfo` | Show cluster/partition status |
| `squeue` | List queued and running jobs |
| `sbatch script.sh` | Submit a batch job |
| `srun command` | Run interactive command |
| `scancel job_id` | Cancel a job |
| `scontrol show node` | Show node details |

## GPU Configuration (GRES)

Slurm uses GRES (Generic Resources) to manage GPUs.

### slurm.conf (key lines)

GresTypes=gpu NodeName=gpu-node01 CPUs=48 Gres=gpu:tesla_t4:1 State=UNKNOWN


### gres.conf
NodeName=gpu-node01 Name=gpu Type=tesla_t4 File=/dev/nvidia0


## Sample GPU Job Script

```bash
#!/bin/bash
#SBATCH --job-name=gpu_training
#SBATCH --output=training_%j.out
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00

echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURMD_NODENAME"
echo "GPUs: $SLURM_JOB_GPUS"

nvidia-smi
python train.py --epochs 100

Multi-GPU Job Example
Copy#!/bin/bash
#SBATCH --job-name=multi_gpu
#SBATCH --gres=gpu:4
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4

srun python -m torch.distributed.launch --nproc_per_node=4 train.py
Lab Results
Tested on Docker container with Tesla T4:

Test	Result
Slurm daemons started	✅
GPU visible via GRES	✅ gpu:tesla_t4:1
Job submission (sbatch)	✅
GPU allocation in job	✅
nvidia-smi in job	✅ Tesla T4, 15360 MiB
Interview Talking Points
Slurm is the standard scheduler for HPC and AI training clusters
GRES configuration enables GPU-aware scheduling
Jobs request GPUs with --gres=gpu:N
Multi-node training uses srun with torch.distributed
Understand job scripts: SBATCH directives, resource requests, output handling
