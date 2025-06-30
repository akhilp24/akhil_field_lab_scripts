# Multi-G Position Remora Analysis Script

This document describes the updated `remora_run_v2.py` script that now supports analysis of multiple G positions with different motifs and files, as demonstrated in the `model141.md` example.

## Overview

The script has been enhanced to handle two modes:
1. **Single G Position Mode** (original functionality)
2. **Multi-G Position Mode** (new functionality)

## Key Features

### Multi-G Position Support
- Process multiple G positions (G29, G30, G31, G35) in a single run
- Different motif positions for each G position
- Separate BAM files for each G position
- Configurable dataset weights for training
- Individual inference outputs for each G position

### Enhanced Logging
- Tracks multiple G positions and motifs in log files
- Records dataset weights used
- Distinguishes between single and multi-G modes

## Usage Examples

### 1. Single G Position Mode (Original)

```bash
python remora_run_v2.py \
  --mode single \
  --pod5 /path/to/pod5 \
  --can-bam /path/to/canonical.bam \
  --motif TTAGGG \
  --mod-num 3 \
  --mod-bam /path/to/modified.bam \
  --g-type G29 \
  --train
```

### 2. Multi-G Position Mode (New)

```bash
python remora_run_v2.py \
  --mode multi \
  --pod5 /mnt/f/Remora_archives/Minion_8/pod5_merged/ \
  --can-bam /mnt/f/Remora_archives/Minion_8/Minion_8_qs9_38387727_mapq20_filtered_demuxed/minion_8_barcode14_merged.bam \
  --g-positions "G29:TTAGGG:3:/mnt/f/Remora_archives/Minion_8/Minion_8_qs9_38387727_mapq20_filtered_demuxed/minion_8_barcode11_merged.bam,G30:TTAGGG:4:/mnt/f/Remora_archives/Minion_8/Minion_8_qs9_38387727_mapq20_filtered_demuxed/minion_8_barcode12_merged.bam,G31:TTAGGG:5:/mnt/f/Remora_archives/Minion_8/Minion_8_qs9_38387727_mapq20_filtered_demuxed/minion_8_barcode13_merged.bam,G35:TTAGGG:3:/mnt/f/Remora_archives/Minion_8/Flongle_68_q9short_short.bam_demuxed1/flongle68_short_short_barcode16.bam:/mnt/f/Remora_archives/Minion_8/Flongle_68/pod5/" \
  --dataset-weights 16 16 16 1 1 1 1 \
  --train \
  --chunk-context 25
```

### 3. Multi-G Position Inference

```bash
python remora_run_v2.py \
  --mode multi \
  --pod5 /mnt/f/Remora_archives/Minion_8/Flongle_67/pod5 \
  --can-bam /mnt/f/Remora_archives/Minion_8/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode14_mapq20_filtered.bam \
  --g-positions "G29:TTAGGG:3:/mnt/f/Remora_archives/Minion_8/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode21_mapq20_filtered.bam,G30:TTAGGG:4:/mnt/f/Remora_archives/Minion_8/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode12_mapq20_filtered.bam,G31:TTAGGG:5:/mnt/f/Remora_archives/Minion_8/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode13_mapq20_filtered.bam,G35:TTAGGG:3:/mnt/f/Remora_archives/Minion_8/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode15_mapq20_filtered.bam" \
  --infer \
  --model train_results/model_best.pt
```

## G-Positions Format

The `--g-positions` argument uses a comma-separated format:

```
G29:TTAGGG:3:/path/to/bam,G30:TTAGGG:4:/path/to/bam
```

### Format Components:
- **G29**: G position identifier
- **TTAGGG**: Motif sequence
- **3**: Modified base position (0-indexed)
- **/path/to/bam**: Path to modified BAM file
- **Optional**: `/path/to/pod5` (if different from main pod5)
- **Optional**: `/path/to/focus.bed` (if different from default)

### Example with Optional Components:
```
G35:TTAGGG:3:/path/to/bam:/path/to/pod5:/path/to/focus.bed
```

## Dataset Weights

For N G positions, specify 2N weights:
- **First N weights**: for canonical chunks (e.g., 16 16 16)
- **Last N weights**: for modified chunks (e.g., 1 1 1)

### Example:
For 3 G positions (G29, G30, G31):
```bash
--dataset-weights 16 16 16 1 1 1
```
This gives weight 16 to each canonical chunk and weight 1 to each modified chunk.

## Output Files

### Multi-G Mode Training:
- `can_G29_chunks/`, `can_G30_chunks/`, `can_G31_chunks/`, etc.
- `8oxoG29_chunks/`, `8oxoG30_chunks/`, `8oxoG31_chunks/`, etc.
- `train_dataset.jsn` (configuration file)
- `train_results/` (training output)

### Multi-G Mode Inference:
- `G29_infer.bam`, `G30_infer.bam`, `G31_infer.bam`, etc.
- `G29_infer.log`, `G30_infer.log`, `G31_infer.log`, etc.

## Logging

The script logs all parameters to `remora_logs/remora_runs.csv` with enhanced fields:
- **Mode**: "single_g" or "multi_g"
- **Motifs**: Comma-separated list of motifs and positions
- **GPositions**: Comma-separated list of G positions
- **DatasetWeights**: Weights used for training

## Backward Compatibility

The script maintains full backward compatibility with the original single G position functionality. Simply use `--mode single` or omit the mode argument (defaults to single).

## Files Modified

1. **`remora_run_v2.py`**: Main script with multi-G position support

## Requirements

- Python 3.6+
- Remora package
- Same dependencies as the original script

## Notes

- The script automatically creates separate chunk directories for each G position
- Dataset configuration includes all canonical and modified chunks
- Inference generates separate output files for each G position
- Path sanitization works for both single and multi-G modes 