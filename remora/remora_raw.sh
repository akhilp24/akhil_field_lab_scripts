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

# Dataset preparation


# remora dataset prepare \
#   /project/romano_shared/telomeres/data/Minion_8/total_pod5 \
#   /project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode14_merged_short.bam \
#   --output-path can_G29_chunks \
#   --refine-kmer-level-table /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/levels.txt \
#   --refine-rough-rescale \
#   --motif TTAGGG 3 \
#   --mod-base-control \
#   --focus-reference-positions /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/focus_reference_positionscan.bed

# remora dataset prepare \
#   /project/romano_shared/telomeres/data/Minion_8/total_pod5 \
#   /project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode14_merged_short.bam \
#   --output-path can_G30_chunks \
#   --refine-kmer-level-table /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/levels.txt \
#   --refine-rough-rescale \
#   --motif TTAGGG 4 \
#   --mod-base-control \
#   --focus-reference-positions /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/focus_reference_positionscan.bed

# remora dataset prepare \
#   /project/romano_shared/telomeres/data/Minion_8/total_pod5 \
#   /project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode14_merged_short.bam \
#   --output-path can_G31_chunks \
#   --refine-kmer-level-table /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/levels.txt \
#   --refine-rough-rescale \
#   --motif TTAGGG 5 \
#   --mod-base-control \
#   --focus-reference-positions /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/focus_reference_positionscan.bed

# remora dataset prepare \
#   /project/romano_shared/telomeres/data/Minion_8/total_pod5 \
#   /project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode11_merged_short.bam \
#   --output-path 8oxo_G29_chunks \
#   --refine-kmer-level-table /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/levels.txt \
#   --refine-rough-rescale \
#   --motif TTAGGG 3 \
#   --mod-base o 8oxo \
#   --focus-reference-positions /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/focus_reference_positionsG29.bed

# remora dataset prepare \
#   /project/romano_shared/telomeres/data/Minion_8/total_pod5 \
#   /project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode12_merged_short.bam \
#   --output-path 8oxo_G30_chunks \
#   --refine-kmer-level-table /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/levels.txt \
#   --refine-rough-rescale \
#   --motif TTAGGG 4 \
#   --mod-base o 8oxo \
#   --focus-reference-positions /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/focus_reference_positionsG30.bed

# remora dataset prepare \
#   /project/romano_shared/telomeres/data/Minion_8/total_pod5 \
#   /project/romano_shared/telomeres/akhil_fieldlab/data/minion_8_barcode13_merged_short.bam \
#   --output-path 8oxo_G31_chunks \
#   --refine-kmer-level-table /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/levels.txt \
#   --refine-rough-rescale \
#   --motif TTAGGG 5 \
#   --mod-base o 8oxo \
#   --focus-reference-positions /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/focus_reference_positionsG31.bed

# remora dataset prepare \
#   /mnt/f/Remora_archives/Minion_8/Flongle_68/pod5/ \
#   /mnt/f/Remora_archives/Minion_8/Flongle_68_q9short_short.bam_demuxed1/flongle68_short_short_barcode16.bam \
#   --output-path 8oxo_G35_chunks \
#   --refine-kmer-level-table /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/levels.txt \
#   --refine-rough-rescale \
#   --motif TTAGGG 3 \
#   --mod-base o 8oxo \
#   --focus-reference-positions /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/focus_reference_positionsG35.bed

# Dataset configuration
# remora \
#   dataset make_config \
#   train_dataset.jsn \
#   can_G29_chunks \
#   can_G30_chunks \
#   can_G31_chunks \
#   8oxo_G29_chunks \
#   8oxo_G30_chunks \
#   8oxo_G31_chunks \
#   --dataset-weights 16 16 16 1 1 1 \
#   --log-filename train_dataset.log

# # Dataset training
# remora model train train_dataset.jsn --model /project/romano_shared/telomeres/akhil_fieldlab/stationaryfiles/ConvLSTM_w_ref.py --device cuda:0 --chunk-context 25 25 --output-path train_results




# Inference

remora \
  infer from_pod5_and_bam --reference-anchored \
  /project/romano_shared/telomeres/data/Flongle_67/pod5 \
  /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode14_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam wt_infer.bam \
  --log-filename wt_infer.log \
  --device cuda:0

remora \
  infer from_pod5_and_bam --reference-anchored \
  /project/romano_shared/telomeres/data/Flongle_67/pod5 \
  /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode21_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam G29_infer.bam \
  --log-filename G29_infer.log \
  --device cuda:0

remora \
  infer from_pod5_and_bam --reference-anchored \
  /project/romano_shared/telomeres/data/Flongle_67/pod5 \
  /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode13_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam G31_infer.bam \
  --log-filename G31_infer.log \
  --device cuda:0

remora \
  infer from_pod5_and_bam --reference-anchored \
  /project/romano_shared/telomeres/data/Flongle_67/pod5 \
  /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode12_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam G30_infer.bam \
  --log-filename G30_infer.log \
  --device cuda:0

# remora \
#   infer from_pod5_and_bam --reference-anchored \
#   /project/romano_shared/telomeres/data/Flongle_67/pod5 \
#   /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode15_mapq20_filtered.bam \
#   --model train_results/model_best.pt \
#   --out-bam G35_infer.bam \
#   --log-filename G35_infer.log \
#   --device cuda:0
