# Remora Analysis Pipeline Documentation

## Overview
This document describes how to use the Remora analysis pipeline for detecting modified bases in nanopore sequencing data. The pipeline includes tools for dataset preparation, model training, inference, and visualization.

## Prerequisites
- Access to a GPU node on the cluster
- Required modules: dorado, cuda, gcc, samtools, and anaconda
- Sufficient storage space for input/output files
- Appropriate permissions to access input data

## Setup

### Environment Setup
The script automatically sets up a conda environment with the required dependencies:
```bash
conda create -y -n remora_env python=3.11
conda install -y -c conda-forge libffi
pip install torch
pip install --no-cache-dir ont-remora
```

### Resource Requirements
- GPU: 1 GPU node
- Memory: 32GB
- Cores: 16
- Wall time: 24 hours

## Usage

### Basic Command Structure

Ensure you are running this command in the same directory as the script file.
```bash
bsub < submit_remora.sh
```

### Required Parameters
The script requires the following parameters to be set in the Python command:
- `--pod5`: Path to POD5 file or directory
- `--can-bam`: Path to canonical BAM file
- `--motif`: Motif sequence (e.g., TTAGGG)
- `--mod-num`: Position of modified base in motif (0-based)
- `--mod-bam`: Path to modified BAM file
- `--g-type`: Type of G modification (G29, G30, G31, or G35)

### Operation Modes

#### 1. Training Mode
To train a new model:
```bash
python remora_run.py \
    --pod5 /path/to/pod5 \
    --can-bam /path/to/canonical.bam \
    --motif TTAGGG \
    --mod-num 3 \
    --mod-bam /path/to/modified.bam \
    --g-type G29 \
    --train
```

#### 2. Inference Mode
To perform inference with a trained model:
```bash
python remora_run.py \
    --pod5 /path/to/pod5 \
    --can-bam /path/to/canonical.bam \
    --motif TTAGGG \
    --mod-num 3 \
    --mod-bam /path/to/modified.bam \
    --g-type G29 \
    --infer \
    --model /path/to/model_best.pt
```

#### 3. Plotting Mode
To generate visualization plots:
```bash
python remora_run.py \
    --pod5 /path/to/pod5 \
    --can-pod5 /path/to/canonical.pod5 \
    --mod-pod5 /path/to/modified.pod5 \
    --can-sort-bam /path/to/canonical.sorted.bam \
    --mod-sort-bam /path/to/modified.sorted.bam \
    --plot
```

## Output Files

### Training Output
- `train_results/`: Directory containing trained model files
- `train_dataset.jsn`: Dataset configuration file
- `train_dataset.log`: Training log file

### Inference Output
- `can_infer.bam`: Inference results for canonical data
- `mod_infer.bam`: Inference results for modified data
- `can_infer.log`: Log file for canonical inference
- `mod_infer.log`: Log file for modified inference

### Plotting Output
- Various visualization plots in the current directory
- `plot.log`: Log file for plotting operations

## Troubleshooting

### Common Issues
1. **Empty Dataset Error**
   - Verify the `--mod-num` parameter matches the correct position in the motif
   - Check that the BAM files contain reads aligned to the target region
   - Ensure the bed files contain the correct positions

2. **GPU Memory Issues**
   - Reduce the batch size in the training configuration
   - Request more GPU memory in the job submission

3. **Library Dependencies**
   - If encountering library errors, try recreating the conda environment
   - Ensure all required modules are loaded before running

### Error Logs
- Check the `%J.err` file for job-specific errors
- Review the log files in the output directories for operation-specific errors

## Best Practices
1. Always verify input file paths before submission
2. Monitor job status using `bjobs`
3. Check output files for expected results
4. Keep track of successful runs in the `remora_logs/remora_runs.csv` file

## Example Workflows

### Complete Training and Inference
1. Train the model:
```bash
python remora_run.py \
    --pod5 /path/to/pod5 \
    --can-bam /path/to/canonical.bam \
    --motif TTAGGG \
    --mod-num 3 \
    --mod-bam /path/to/modified.bam \
    --g-type G29 \
    --train
```

2. Perform inference:
```bash
python remora_run.py \
    --pod5 /path/to/pod5 \
    --can-bam /path/to/canonical.bam \
    --motif TTAGGG \
    --mod-num 3 \
    --mod-bam /path/to/modified.bam \
    --g-type G29 \
    --infer \
    --model train_results/model_best.pt
```

3. Generate plots:
```bash
python remora_run.py \
    --pod5 /path/to/pod5 \
    --can-pod5 /path/to/canonical.pod5 \
    --mod-pod5 /path/to/modified.pod5 \
    --can-sort-bam can_infer.sorted.bam \
    --mod-sort-bam mod_infer.sorted.bam \
    --plot
```

