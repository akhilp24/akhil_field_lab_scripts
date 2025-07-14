Here is your Word document content converted to Markdown, with clear formatting for sections, code blocks, and emphasis where appropriate[1].

**Model 140**

```bash
cd /mnt/f/Remora_archives/Minion_8
```

## Dataset Prepare

**WT** *(Modify Motif for different G of interest)*

```bash
remora dataset prepare \
  /mnt/f/Remora_archives/Minion_8/pod5_merged/ \
  /mnt/f/Remora_archives/Minion_8/Minion_8_qs9_38387727_mapq20_filtered_demuxed/minion_8_barcode14_merged.bam \
  --output-path can_all_chunks \
  --refine-kmer-level-table /mnt/c/users/lab/desktop/minion8/stationaryfiles/levels.txt \
  --refine-rough-rescale \
  --motif TTAGGG 3 \
  --mod-base-control \
  --focus-reference-positions /mnt/f/Remora_archives/Minion_8/stationaryfiles/focus_reference_positionscan.bed
```

**G29**

```bash
remora dataset prepare \
  /mnt/f/Remora_archives/Minion_8/pod5_merged/ \
  /mnt/f/Remora_archives/Minion_8/Minion_8_qs9_38387727_mapq20_filtered_demuxed/minion_8_barcode11_merged.bam \
  --output-path 8oxo_G29_chunks \
  --refine-kmer-level-table /mnt/f/Remora_archives/Minion_8/stationaryfiles/levels.txt \
  --refine-rough-rescale \
  --motif TTAGGG 3 \
  --mod-base o 8oxo \
  --focus-reference-positions /mnt/f/Remora_archives/Minion_8/stationaryfiles/focus_reference_positionsG29.bed
```

**G30**

```bash
remora dataset prepare \
  /mnt/f/Remora_archives/Minion_8/pod5_merged/ \
  /mnt/f/Remora_archives/Minion_8/Minion_8_qs9_38387727_mapq20_filtered_demuxed/minion_8_barcode12_merged.bam \
  --output-path 8oxo_G30_chunks \
  --refine-kmer-level-table /mnt/f/Remora_archives/Minion_8/stationaryfiles/levels.txt \
  --refine-rough-rescale \
  --motif TTAGGG 4 \
  --mod-base o 8oxo \
  --focus-reference-positions /mnt/f/Remora_archives/Minion_8/stationaryfiles/focus_reference_positionsG30.bed
```

**G31**

```bash
remora dataset prepare \
  /mnt/f/Remora_archives/Minion_8/pod5_merged/ \
  /mnt/f/Remora_archives/Minion_8/Minion_8_qs9_38387727_mapq20_filtered_demuxed/minion_8_barcode13_merged.bam \
  --output-path 8oxo_G31_chunks \
  --refine-kmer-level-table /mnt/f/Remora_archives/Minion_8/stationaryfiles/levels.txt \
  --refine-rough-rescale \
  --motif TTAGGG 5 \
  --mod-base o 8oxo \
  --focus-reference-positions /mnt/f/Remora_archives/Minion_8/stationaryfiles/focus_reference_positionsG31.bed
```

**G35**

```bash
remora dataset prepare \
  /mnt/f/Remora_archives/Minion_8/Flongle_68/pod5/ \
  /mnt/f/Remora_archives/Minion_8/Flongle_68_q9short_short.bam_demuxed1/flongle68_short_short_barcode16.bam \
  --output-path 8oxo_G35_chunks \
  --refine-kmer-level-table /mnt/f/Remora_archives/Minion_8/stationaryfiles/levels.txt \
  --refine-rough-rescale \
  --motif TTAGGG 3 \
  --mod-base o 8oxo \
  --focus-reference-positions /mnt/f/Remora_archives/Minion_8/stationaryfiles/focus_reference_positionsG35.bed
```

## Dataset Configuration

```bash
remora \
  dataset make_config \
  train_dataset.jsn \
  can_G29_chunks \
  can_G30_chunks \
  can_G31_chunks \
  8oxo_G29_chunks \
  8oxo_G30_chunks \
  8oxo_G31_chunks \
  8oxo_G35_chunks \
  --dataset-weights 16 16 16 1 1 1 1 \
  --log-filename train_dataset.log
```

## Training

```bash
remora model train train_dataset.jsn --model /home/lab/mambaforge/lib/python3.10/site-packages/remora/ConvLSTM_w_ref.py --device 0 --chunk-context 25 25 --output-path train_results
```

## Infer

```bash
remora \
  infer from_pod5_and_bam --reference-anchored \
  Flongle_67/pod5 \
  Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode14_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam wt_infer.bam \
  --log-filename wt_infer.log \
  --device 0

remora \
  infer from_pod5_and_bam --reference-anchored \
  Flongle_67/pod5 \
  Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode21_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam G29_infer.bam \
  --log-filename G29_infer.log \
  --device 0

remora \
  infer from_pod5_and_bam --reference-anchored \
  Flongle_67/pod5 \
  Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode13_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam G31_infer.bam \
  --log-filename G31_infer.log \
  --device 0

remora \
  infer from_pod5_and_bam --reference-anchored \
  Flongle_67/pod5 \
  Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode12_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam G30_infer.bam \
  --log-filename G30_infer.log \
  --device 0

remora \
  infer from_pod5_and_bam --reference-anchored \
  Flongle_67/pod5 \
  Flongle_67/Flongle_67_demuxed_calls/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode15_mapq20_filtered.bam \
  --model train_results/model_best.pt \
  --out-bam G35_infer.bam \
  --log-filename G35_infer.log \
  --device 0
```