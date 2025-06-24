# Instructions to Run Dorado Job

### General Information
**submit_dorado.sh** is the job script submission

**dorado_run.py** is the Python logic. 

These must remain in the akhil folder and have the reference_files folder in the same directory. 

## Folder Navigation

Navigate to /telomeres/akhil/

```cd /project/romano_shared/telomeres/akhil```

## Modify Parameters

Here's the standard template file for the script to be run:

```
module load dorado
module load cuda/12.4
module load gcc/12.2.0
module load samtools

python dorado_run.py \
    --pod5 /project/romano_shared/telomeres/akhil/pod5/G_filtered.pod5 \
    --output testing_python_job_G_filtered_apr11_2025.bam \
    --accuracy sup \
    --device cuda:all \
    --qscore 9 \'
    --no-trim
    --reference /project/romano_shared/telomeres/akhil/reference_files/referenceshort.fasta
```


Modify the parameters in the .sh script, including the output name, input pod5 file, and reference file, and submit to the script by using the following command:

```bsub < dorado_run.py```


To choose between calling a .fastq or .bam file, add the file type to the output and include the reference file if a BAM file is being called and don't include if a .FASTQ file is being called.






