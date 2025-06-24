import subprocess
import os
import argparse
import shutil
from pathlib import Path

def run_command(command):
    """Execute a shell command and return the return code"""
    print(f"Running: {command}")
    
    # Check if samtools is available in the environment
    if command.startswith("samtools") and shutil.which("samtools") is None:
        print("Error: samtools is not available in the PATH. Make sure it's installed and loaded.")
        return 127
    
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=os.environ.copy()  # Use current environment variables
    )
    
    # Print output in real-time
    for line in iter(process.stdout.readline, ''):
        print(line.strip())
    
    process.stdout.close()
    return_code = process.wait()
    
    if return_code != 0:
        print(f"Command failed with return code {return_code}")
        
        # Check for common errors
        if return_code == 127:
            print("This error typically indicates missing libraries or executables.")
            print("Try loading required modules with 'module load samtools' and 'module load openssl'")
    
    return return_code

def filter_bam(input_bam, output_bam, min_mapq=0, remove_unmapped=False, remove_map0=False, min_length=None, remove_indels=False):
    """
    Filter BAM file based on mapping quality, mapping status, and read length.
    
    Args:
        input_bam (str): Path to input BAM file
        output_bam (str): Path to output BAM file
        min_mapq (int): Minimum mapping quality score (default: 0)
        remove_unmapped (bool): Whether to remove unmapped reads (default: False)
        remove_map0 (bool): Whether to remove reads with mapping quality 0 (default: False)
        min_length (int or None): Minimum read length to keep (default: None)
        remove_indels (bool): Whether to remove reads with insertions or deletions (default: False)
    """
    # Validate input file exists
    if not os.path.exists(input_bam):
        raise FileNotFoundError(f"Input BAM file not found: {input_bam}")
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_bam)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # If removing indels, use the special awk-based command
    if remove_indels:
        cmd = f"samtools view -h {input_bam} | awk 'BEGIN{{OFS=\"\\t\"}} /^@/ {{print $0}} !/^@/ && $6 !~ /[ID]/ {{print $0}}' | samtools view -b -o {output_bam}"
        return_code = run_command(cmd)
        
        if return_code == 0:
            print(f"Successfully filtered BAM file (removed indels). Output written to: {output_bam}")
            return True
        else:
            print(f"Failed to filter BAM file. Return code: {return_code}")
            return False
    
    # Build samtools view command for other filters
    cmd = ["samtools view -b"]
    
    # Add mapping quality filter
    if min_mapq > 0:
        cmd.append(f"-q {min_mapq}")
    
    # Add unmapped filter
    if remove_unmapped:
        cmd.append("-F 4")  # -F 4 excludes unmapped reads
    
    # Add mapq=0 filter
    if remove_map0:
        cmd.append("-q 1")  # -q 1 excludes mapq=0 reads
    
    # Add minimum read length filter
    if min_length is not None:
        cmd.append(f"-e 'rlen > {min_length}'")
    
    # Add input and output files
    cmd.append(input_bam)
    cmd.append(f"> {output_bam}")
    
    # Join command parts
    full_cmd = " ".join(cmd)
    
    # Run the command
    return_code = run_command(full_cmd)
    
    if return_code == 0:
        print(f"Successfully filtered BAM file. Output written to: {output_bam}")
        return True
    else:
        print(f"Failed to filter BAM file. Return code: {return_code}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Filter BAM files using samtools")
    parser.add_argument("--input", required=True, help="Input BAM file path")
    parser.add_argument("--output", required=True, help="Output BAM file path")
    parser.add_argument("--min-mapq", type=int, default=0, help="Minimum mapping quality score (default: 0)")
    parser.add_argument("--remove-unmapped", action="store_true", help="Remove unmapped reads")
    parser.add_argument("--remove-map0", action="store_true", help="Remove reads with mapping quality 0")
    parser.add_argument("--min-length", type=int, default=None, help="Minimum read length to keep (optional)")
    parser.add_argument("--remove-indels", action="store_true", help="Remove reads with insertions or deletions")
    
    args = parser.parse_args()
    
    # Perform filtering
    success = filter_bam(
        input_bam=args.input,
        output_bam=args.output,
        min_mapq=args.min_mapq,
        remove_unmapped=args.remove_unmapped,
        remove_map0=args.remove_map0,
        min_length=args.min_length,
        remove_indels=args.remove_indels
    )
    
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
