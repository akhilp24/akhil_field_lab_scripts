#!/bin/bash
#BSUB -J remora_python           # Job name
#BSUB -o output_logs/%J_remora.out  # Output file with date and time
#BSUB -e output_logs/%J_remora.err  # Error file with date and time
#BSUB -q romanogpu             # Specify queue name
#BSUB -m romanogpu1           # Request specific GPU node
#BSUB -W 24:00                # Wall clock time limit
#BSUB -M 32GB                 # Memory limit
#BSUB -n 32                    # Number of cores
#BSUB -gpu "num=1"
#BSUB -B                      # Email when job starts
#BSUB -N                      # Email when job ends
#BSUB -u akhilp24@sas.upenn.edu

module load dorado/0.9.5
module load cuda/12.4
module load gcc/12.2.0
module load samtools
# module load anaconda/3
module load python/3.11

# eval "$(conda shell.bash hook)"

# Commenting out the creation of the venv
#if ! conda info --envs | grep -q remora_env; then
#    conda create -y -n remora_env python=3.11
#    conda activate remora_env
#    conda install -y -c conda-forge libffi
#    pip install torch
#    # pip install --no-cache-dir ont-remora
#else
    # conda activate remora_env
#fi

# Remove the PATH modification that was pointing to conda's remora
# export PATH="$CONDA_PREFIX/bin:$PATH"

# Verify we're using system remora
which remora
remora -v

# To train a model

# python remora_run.py \
#     --pod5 /project/romano_shared/telomeres/data/Minion_8/pod5 \
#     --can-bam /project/romano_shared/telomeres/data/Minion_8/minion_8_q9_mapq_60demuxed_calls/SQK-NBD114-24_barcode14.bam \
#     --motif TTAGGG \
#     --mod-num 3 \
#     --mod-bam /project/romano_shared/telomeres/data/Minion_8/minion_8_q9_mapq_60demuxed_calls/SQK-NBD114-24_barcode11.bam \
#     --g-type G29 \
#     --train

# python remora_run_v2.py \
#   --mode multi \
#   --pod5 /project/romano_shared/telomeres/data/Minion_8/total_pod5 \
#   --can-bam /project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode14_merged_short.bam \
#   --g-positions "G29:TTAGGG:3:/project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode11_merged_short.bam,G30:TTAGGG:4:/project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode12_merged_short.bam,G31:TTAGGG:5:/project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode13_merged_short.bam,G35:TTAGGG:3:/mnt/f/Remora_archives/Minion_8/Flongle_68_q9short_short.bam_demuxed1/flongle68_short_short_barcode16.bam:/mnt/f/Remora_archives/Minion_8/Flongle_68/pod5/" \
#   --dataset-weights 16 16 16 1 1 1 1 \
#   --train \
#   --chunk-context 25

# To do inference

# python remora_run.py \
#     --pod5 /project/romano_shared/telomeres/data/flg64/pod5 \
#     --can-bam /project/romano_shared/telomeres/data/flg64/flg64_q8.bam_demuxed/730bb123-5334-42d3-9fd2-7ada7257d1d2_SQK-NBD114-24_barcode11.bam \
#     --motif TTAGGG \
#     --mod-num 3 \
#     --mod-bam /project/romano_shared/telomeres/data/flg64/flg64_q8.bam_demuxed/730bb123-5334-42d3-9fd2-7ada7257d1d2_SQK-NBD114-24_barcode14.bam \
#     --g-type G29 \
#     --infer \
#     --model /project/romano_shared/telomeres/akhil/train_results/model_best.pt



# To do inference

# python remora_run.py \
#     --pod5 /project/romano_shared/telomeres/data/Flongle_67/pod5 \
#     --can-bam /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_demuxed_calls/SQK-NBD114-24_barcode14.bam \
#     --motif TTAGGG \
#     --mod-num 3 \
#     --mod-bam /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_demuxed_calls/SQK-NBD114-24_barcode15.bam \
#     --g-type G35 \
#     --infer \
#     --model /project/romano_shared/telomeres/akhil/train_results/model_best.pt

# To generate a plot

# python remora_run.py \
#     --pod5 /project/romano_shared/telomeres/data/Minion_8/pod5 \
#     --can-pod5 /project/romano_shared/telomeres/data/Minion_8/pod5 \
#     --mod-pod5 /project/romano_shared/telomeres/data/Minion_8/pod5 \
#     --can-bam /project/romano_shared/telomeres/data/testing/plotting/minion8_q9/mapq60/g31/SQK-NBD114-24_barcode14.bam \
#     --mod-bam /project/romano_shared/telomeres/data/testing/plotting/minion8_q9/mapq60/g31/SQK-NBD114-24_barcode13.bam \
#     --motif TTAGGG \
#     --mod-num 5 \
#     --g-type G31 \
#     --can-sort-bam /project/romano_shared/telomeres/data/testing/plotting/minion8_q9/mapq60/g31/SQK-NBD114-24_barcode14.sorted.bam \
#     --mod-sort-bam /project/romano_shared/telomeres/data/testing/plotting/minion8_q9/mapq60/g31/SQK-NBD114-24_barcode13.sorted.bam \
#     --plot

# Optional flags you can add:
# --train              # If you want to train a model
# --infer --model /path/to/model  # If you want to do inference
# --plot --can-pod5 /path/to/can.pod5 --mod-pod5 /path/to/mod.pod5 --can-sort-bam /path/to/can.sorted.bam --mod-sort-bam /path/to/mod.sorted.bam



