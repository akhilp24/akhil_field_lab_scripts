# Job Script Guide for Remora Multi-G Position Analysis

This guide explains how to use the job scripts with your updated `remora_run_v2.py` script.

## Quick Start

### 1. Use the Template Script (Recommended)

The `run_remora_job.sh` file is a ready-to-use template:

```bash
# 1. Copy and modify the template
cp run_remora_job.sh my_analysis_job.sh

# 2. Edit the configuration section in my_analysis_job.sh
#    - Set WORK_DIR to your working directory
#    - Update POD5_PATH and CAN_BAM paths
#    - Modify G_POSITIONS for your data
#    - Adjust DATASET_WEIGHTS if needed

# 3. Uncomment the appropriate job scheduler directives (LSF or SLURM)

# 4. Submit the job
# For LSF: bsub < my_analysis_job.sh
# For SLURM: sbatch my_analysis_job.sh
# For local execution: bash my_analysis_job.sh
```

### 2. Generate Custom Scripts

Use the script generator:

```bash
# Run the generator
bash job_script_examples.sh

# Choose option 7 to create all script types
# Then modify the generated scripts as needed
```

## Job Scheduler Examples

### LSF (IBM Spectrum LSF)

```bash
# Submit training job
bsub < lsf_training_job.sh

# Submit inference job
bsub < lsf_inference_job.sh

# Check job status
bjobs

# Monitor job output
tail -f logs/training_*.out
```

### SLURM

```bash
# Submit training job
sbatch slurm_training_job.sh

# Submit inference job
sbatch slurm_inference_job.sh

# Check job status
squeue

# Monitor job output
tail -f logs/training_*.out
```

### Local Execution

```bash
# Run locally (no job scheduler)
bash local_single_g_job.sh

# Or run the template directly
bash run_remora_job.sh
```

## Configuration Examples

### Example 1: Multi-G Position Training (Model141-like)

```bash
# In your job script, set:
MODE="multi"
JOB_TYPE="train"
G_POSITIONS="G29:TTAGGG:3:/path/to/G29.bam,G30:TTAGGG:4:/path/to/G30.bam,G31:TTAGGG:5:/path/to/G31.bam"
DATASET_WEIGHTS="16 16 16 1 1 1"
CHUNK_CONTEXT=25
```

### Example 2: Single G Position Training

```bash
# In your job script, set:
MODE="single"
JOB_TYPE="train"
# Use individual arguments instead of G_POSITIONS:
# --motif TTAGGG --mod-num 3 --mod-bam /path/to/bam --g-type G29
```

### Example 3: Multi-G Position Inference

```bash
# In your job script, set:
MODE="multi"
JOB_TYPE="infer"
G_POSITIONS="G29:TTAGGG:3:/path/to/G29.bam,G30:TTAGGG:4:/path/to/G30.bam"
MODEL_PATH="train_results/model_best.pt"
```

## Parameterized Jobs

For dynamic job submission, use the parameterized approach:

```bash
# Set environment variables
export G_TYPE="G29,G30,G31"
export JOB_TYPE="train"
export MEMORY=32
export WALL_TIME="24:00"
export WORK_DIR="/path/to/work"
export POD5_PATH="/path/to/pod5"
export CAN_BAM="/path/to/can.bam"
export G_POSITIONS="G29:TTAGGG:3:/path/to/G29.bam,G30:TTAGGG:4:/path/to/G30.bam"
export DATASET_WEIGHTS="16 16 1 1"
export CHUNK_CONTEXT=25
export MODEL_PATH="/path/to/model.pt"

# Submit job
bsub < parameterized_job.sh
```

## Batch Processing

For processing multiple G positions separately:

```bash
# Run the batch submission script
bash batch_submit.sh

# This will create and submit separate jobs for each G position
```

## Common Modifications

### Memory Requirements

```bash
# For LSF
#BSUB -R "rusage[mem=64GB]"  # Increase for larger datasets

# For SLURM
#SBATCH --mem=64G  # Increase for larger datasets
```

### GPU Requirements

```bash
# For LSF
#BSUB -R "rusage[ngpus_excl_p=2]"  # Request 2 GPUs

# For SLURM
#SBATCH --gres=gpu:2  # Request 2 GPUs
```

### Time Limits

```bash
# For LSF
#BSUB -W 48:00  # 48 hours

# For SLURM
#SBATCH --time=48:00:00  # 48 hours
```

### Module Loading

```bash
# Modify for your system
module load python/3.9
module load cuda/11.8

# Or use conda
conda activate remora_env
```

## Troubleshooting

### Common Issues

1. **Path not found**: Check that all file paths are correct and accessible
2. **Memory errors**: Increase memory allocation in job script
3. **GPU errors**: Ensure CUDA modules are loaded and GPU is available
4. **Permission errors**: Make sure job script is executable (`chmod +x script.sh`)

### Debug Mode

Add debugging to your job script:

```bash
# Add these lines to your job script
set -x  # Print commands as they execute
set -e  # Exit on any error
set -u  # Exit on undefined variable
```

### Log Monitoring

```bash
# Monitor job output in real-time
tail -f logs/remora_*.out

# Check for errors
grep -i error logs/remora_*.err

# Check job status
bjobs  # for LSF
squeue # for SLURM
```

## Best Practices

1. **Test locally first**: Run with a small dataset before submitting to cluster
2. **Use meaningful job names**: Include G positions and job type in job name
3. **Monitor resources**: Start with conservative memory/GPU requests
4. **Keep logs organized**: Use timestamped log files
5. **Backup configurations**: Save your working job script configurations

## File Structure

After running jobs, you'll have:

```
your_working_directory/
├── logs/
│   ├── remora_*.out          # Job output
│   ├── remora_*.err          # Job errors
│   └── remora_runs.csv       # Parameter logging
├── can_G29_chunks/           # Canonical chunks (multi-G mode)
├── can_G30_chunks/
├── 8oxoG29_chunks/           # Modified chunks (multi-G mode)
├── 8oxoG30_chunks/
├── train_dataset.jsn         # Dataset configuration
├── train_results/            # Training output
├── G29_infer.bam            # Inference results (multi-G mode)
├── G30_infer.bam
└── remora_run_v2.py         # Your analysis script
``` 