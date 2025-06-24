import subprocess
import os
import argparse
import datetime
import csv
from pathlib import Path

def run_command(command):
    """Execute a shell command and return the return code"""
    print(f"Running: {command}")
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Print output in real-time
    for line in iter(process.stdout.readline, ''):
        print(line.strip())
    
    process.stdout.close()
    return_code = process.wait()
    
    if return_code != 0:
        print(f"Command failed with return code {return_code}")
    
    return return_code

def log_parameters(args):
    """Log all parameters to a CSV file"""
    # Get current timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Get LSB_JOBID from environment, default to 'local' if not in LSB environment
    job_id = os.environ.get('LSB_JOBID', 'local')
    
    # Create log entry
    log_entry = [
        job_id,
        timestamp,
        str(args.pod5),
        str(args.output),
        str(args.accuracy),
        str(args.device),
        str(args.qscore),
        str(args.reference) if args.reference else "no_reference",
        "moves_enabled" if args.emit_moves else "",
        "remove_map0" if args.remove_map0 else "",
        "remove_unmapped" if args.remove_unmapped else ""
    ]
    
    # Write to CSV file
    log_file = "dorado_job_parameters.csv"
    file_exists = Path(log_file).is_file()
    
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write header if file does not exist
            writer.writerow(["Job ID", "Timestamp", "Pod5", "Output", "Accuracy", "Device", "Q-score", "Reference", "Moves", "Remove Map0", "Remove Unmapped"])
        writer.writerow(log_entry)
    
    print(f"Parameters logged to {log_file}")

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Dorado Basecalling and Demuxing Assistant")
    parser.add_argument("--qscore", type=str, default="9", help="Minimum q-score")
    parser.add_argument("--device", type=str, default="0", choices=["0", "metal", "cuda:all"], help="Device type: 0 for GPU, metal for Apple Silicon")
    parser.add_argument("--accuracy", type=str, default="hac", choices=["hac", "sup"], help="Accuracy type")
    parser.add_argument("--pod5", type=str, required=True, help="Path to pod5 folder or file")
    parser.add_argument("--reference", type=str, default="", help="Path to reference fasta file (optional)")
    parser.add_argument("--emit-moves", action="store_true", help="Emit moves table")
    parser.add_argument("--no-trim", action="store_true", help="Do not trim reads")
    parser.add_argument("--demux-no-trim", action="store_true", help="Do not trim reads for demultiplexing")
    parser.add_argument("--output", type=str, required=True, help="Output file name (.bam or .fastq)")
    parser.add_argument("--remove-map0", action="store_true", help="Remove mapped reads with score of 0")
    parser.add_argument("--remove-unmapped", action="store_true", help="Remove unmapped reads")
    parser.add_argument("--kit-name", type=str, default="SQK-NBD114-24", help="Kit name")
    
    args = parser.parse_args()
    
    # Add logging call right after argument parsing
    log_parameters(args)
    
    # Set up basecaller command
    basecaller_command = "dorado basecaller "
    if args.emit_moves:
        basecaller_command += "--emit-moves "
    
    if args.no_trim:
        basecaller_command += "--no-trim "
    
    basecaller_command += f"--min-qscore {args.qscore} --device {args.device} /project/romano_shared/telomeres/models/dna_r10.4.1_e8.2_400bps_{args.accuracy}@v5.0.0 {args.pod5} "
    
    if args.output.endswith("fastq"):
        basecaller_command += "--emit-fastq "
    
    if args.reference == "":
        basecaller_command += f"--kit-name {args.kit_name} > {args.output}"
    else:
        basecaller_command += f"--reference {args.reference} --kit-name {args.kit_name} > {args.output}"
    
    print("=== Basecalling Command ===")
    print(basecaller_command)
    
    # Run basecalling
    return_code = run_command(basecaller_command)
    if return_code == 0:
        print("Basecalling completed successfully!")
    else:
        print("Basecalling failed!")
        return
    
    output = args.output
    
    # Process mapped reads with score of 0 if requested
    if args.remove_map0 and not output.endswith('.fastq'):
        print("=== Processing mapped reads ===")
        map0_command = f"samtools view -b -q 1 {output} > {output}_map0.bam"
        print(map0_command)
        run_command(map0_command)
        output = f"{output}_map0"
    
    # Process unmapped reads if requested
    if args.remove_unmapped and not output.endswith('.fastq'):
        print("=== Processing unmapped reads ===")
        unmapped_command = f"samtools view -F 4 -b {output} > {output}_unmapped_remove.bam"
        print(unmapped_command)
        run_command(unmapped_command)
        output = f"{output}_unmapped_remove"
    
    # Run demultiplexing
    print("=== Demultiplexing ===")
    demux_command = ""
    if output.endswith("fastq"):
        demux_command = f"dorado demux --emit-fastq -o {output}_demuxed {output}"
    else:
        demux_command = f"dorado demux -o {output}_demuxed "
        if args.demux_no_trim:
            demux_command += "--no-trim "
        demux_command += f"--no-classify {output}"
    
    print(demux_command)
    return_code = run_command(demux_command)
    if return_code == 0:
        print("Demultiplexing completed successfully!")
    else:
        print("Demultiplexing failed!")
        return
    
    print("All processing completed!")

if __name__ == "__main__":
    main()
