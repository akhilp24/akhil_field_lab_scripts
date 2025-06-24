#!/bin/bash
#BSUB -J samtools_filtering           # Job name
#BSUB -o output_logs/%J_samtools.out  # Output file with date and time
#BSUB -e output_logs/%J_samtools.err  # Error file with date and time
#BSUB -q lpc_normal             # Specify queue name
#BSUB -W 24:00                # Wall clock time limit
#BSUB -M 32GB                 # Memory limit
#BSUB -n 32                    # Number of cores
#BSUB -B                      # Email when job starts
#BSUB -N                      # Email when job ends
#BSUB -u akhilp24@sas.upenn.edu

# Print debug info
echo "Which samtools:"
which samtools
echo "Samtools version:"
module load samtools
samtools --version

# python samtools_filtering.py \
#     --input /project/romano_shared/telomeres/akhil/Minion_8_qs9_38423387_long_reference.bam \
#     --output Minion_8_qs9_38423387_long_reference_mapq60_filtered.bam \
#     --min-mapq 60

# python samtools_filtering.py \
#     --input /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_qs9_38217398.bam_demuxed/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode13.bam \
#     --output Flongle_67_qs9_38217398.bam_demuxed/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode13_mapq20_filtered.bam \
#     --min-mapq 20

# python samtools_filtering.py \
#     --input /project/romano_shared/telomeres/data/Flongle_67/Flongle_67_qs9_38217398.bam_demuxed/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode21.bam \
#     --output Flongle_67_qs9_38217398.bam_demuxed/32a33d53-7d3a-4b39-9aef-857f4775cfac_SQK-NBD114-24_barcode21_mapq20_filtered.bam \
#     --min-mapq 20


# python samtools_filtering.py \
#     --input /project/romano_shared/telomeres/data/Minion_8/BAM/SQK-NBD114-24_barcode11.bam \
#     --output SQK-NBD114-24_barcode11_mapq60_filtered.bam \
#     --min-mapq 60

# # Basic filtering with minimum mapq
# python samtools_filtering.py --input in.bam --output out.bam --min-mapq 10

# # Remove unmapped reads
# python samtools_filtering.py --input in.bam --output out.bam --remove-unmapped

# # Remove mapq=0 reads
# python samtools_filtering.py --input in.bam --output out.bam --remove-map0

# # Combine filters
# python samtools_filtering.py --input in.bam --output out.bam --min-mapq 10 --remove-unmapped --remove-map0



# Extra stuff

# for bam_file in /project/romano_shared/telomeres/akhil/Minion_8_qs9_38423387_long_reference_mapq60_filtered_demuxed/*.bam; do
#     sample_name=$(basename "$bam_file" .bam)
#     samtools sort -o /project/romano_shared/telomeres/akhil/sorted/${sample_name}_sorted.bam "$bam_file"
# done

# samtools merge minion_8_barcode11_merged_long.bam /project/romano_shared/telomeres/akhil/sorted/1c5b00b8-2f59-4ee2-93fb-5a5ac6642eef_SQK-NBD114-24_barcode11_sorted.bam /project/romano_shared/telomeres/akhil/sorted/3664b9f0-93af-4b9e-95dd-3dc78e7f38db_SQK-NBD114-24_barcode11_sorted.bam /project/romano_shared/telomeres/akhil/sorted/f4de4fc2-4039-4481-88c0-1f94400bd5e3_SQK-NBD114-24_barcode11_sorted.bam

# samtools merge minion_8_barcode12_merged_long.bam /project/romano_shared/telomeres/akhil/sorted/1c5b00b8-2f59-4ee2-93fb-5a5ac6642eef_SQK-NBD114-24_barcode12_sorted.bam /project/romano_shared/telomeres/akhil/sorted/3664b9f0-93af-4b9e-95dd-3dc78e7f38db_SQK-NBD114-24_barcode12_sorted.bam /project/romano_shared/telomeres/akhil/sorted/f4de4fc2-4039-4481-88c0-1f94400bd5e3_SQK-NBD114-24_barcode12_sorted.bam

# samtools merge minion_8_barcode13_merged_long.bam /project/romano_shared/telomeres/akhil/sorted/1c5b00b8-2f59-4ee2-93fb-5a5ac6642eef_SQK-NBD114-24_barcode13_sorted.bam /project/romano_shared/telomeres/akhil/sorted/3664b9f0-93af-4b9e-95dd-3dc78e7f38db_SQK-NBD114-24_barcode13_sorted.bam /project/romano_shared/telomeres/akhil/sorted/f4de4fc2-4039-4481-88c0-1f94400bd5e3_SQK-NBD114-24_barcode13_sorted.bam

# samtools merge minion_8_barcode14_merged_long.bam /project/romano_shared/telomeres/akhil/sorted/1c5b00b8-2f59-4ee2-93fb-5a5ac6642eef_SQK-NBD114-24_barcode14_sorted.bam /project/romano_shared/telomeres/akhil/sorted/3664b9f0-93af-4b9e-95dd-3dc78e7f38db_SQK-NBD114-24_barcode14_sorted.bam /project/romano_shared/telomeres/akhil/sorted/f4de4fc2-4039-4481-88c0-1f94400bd5e3_SQK-NBD114-24_barcode14_sorted.bam

python akhil/samtools_filtering.py --input input.bam --output output_filtered.bam --min-length 100

# Example: Remove reads with insertions and deletions
python samtools_filtering.py --input input.bam --output output_noindels.bam --remove-indels

# Example: Combine multiple filters including indel removal
# python samtools_filtering.py --input input.bam --output output_filtered.bam --min-mapq 20 --remove-unmapped --remove-indels --min-length 100