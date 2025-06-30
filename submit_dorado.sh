#!/bin/bash
#BSUB -J dorado_python           # Job name
#BSUB -o output_logs/%J.out                 # Output file
#BSUB -e output_logs/%J.err                 # Error file
#BSUB -q romanogpu             # Specify queue name
#BSUB -m romanogpu1           # Request specific GPU node
#BSUB -W 24:00                # Wall clock time limit
#BSUB -M 32GB                 # Memory limit
#BSUB -n 48                    # Number of cores
#BSUB -gpu "num=1"
#BSUB -B                      # Email when job starts
#BSUB -N                      # Email when job ends
#BSUB -u akhilp24@sas.upenn.edu


module load dorado/0.9.5
module load cuda/12.4
module load gcc/12.2.0
module load samtools

python dorado_run.py \
    --pod5 /project/romano_shared/telomeres/data/Minion10/combined_pod5 \
    --output Minion_10_qs9_${LSB_JOBID}.fastq \
    --accuracy sup \
    --device cuda:all \
    --qscore 9 \
    --no-trim \
    --kit-name SQK-NBD114-96 \
    --emit-moves

   
# --reference /project/romano_shared/telomeres/akhil/reference_files/referenceshort.fasta \
# --reference /project/romano_shared/telomeres/akhil/reference_files/reference.fasta \
# --emit-moves