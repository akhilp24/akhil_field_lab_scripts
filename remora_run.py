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
        str(args.can_bam),
        str(args.motif),
        str(args.mod_num),
        str(args.mod_bam),
        str(args.g_type),
        "plot" if args.plot else "no_plot",
        "train" if args.train else "no_train",
        "infer" if args.infer else "no_infer",
        str(args.model) if args.model else "no_model",
        str(args.chunk_context) if args.chunk_context else "default_chunk_context"
    ]
    
    # Create logs directory if it doesn't exist
    log_dir = Path("remora_logs")
    log_dir.mkdir(exist_ok=True)
    
    # Write to CSV
    log_file = log_dir / "remora_runs.csv"
    file_exists = log_file.exists()
    
    with open(log_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([
                "JobID", "Timestamp", "Pod5", "CanBAM", "Motif", "ModNum", 
                "ModBAM", "GType", "Plot", "Train", "Infer", "Model", "ChunkContext"
            ])
        writer.writerow(log_entry)
    
    print(f"Parameters logged to {log_file}")

def sanitize_path(path):
    if not path:
        return path
        
    path = str(path).replace("\\", "/")
    
    # If path is already relative, just return it
    if path.startswith("./") or path.startswith("../"):
        return path
        
    # Get current working directory
    current_working_directory = os.getcwd().replace("\\", "/")
    
    # If the path is already absolute and doesn't contain the current directory
    if path.startswith("/") and current_working_directory not in path:
        return path
        
    # Try to make the path relative to current directory
    try:
        return os.path.relpath(path, current_working_directory)
    except ValueError:
        # If that fails, just return the original path
        return path

def dataset_prepare(args):
    # Check if chunk folders already exist
    if os.path.exists("can_all_chunks") and os.path.exists(f"8oxo{args.g_type}_chunks"):
        print("Chunk folders already exist. Skipping dataset preparation.")
        return

    # Canonical dataset preparation
    can_cmd = [
        "remora", "dataset", "prepare",
        str(args.pod5), str(args.can_bam),
        "--output-path", "can_all_chunks",
        "--refine-kmer-level-table", "stationaryfiles/levels.txt",
        "--refine-rough-rescale",
        "--motif", str(args.motif), str(args.mod_num),
        "--mod-base-control",
        "--focus-reference-positions", "stationaryfiles/focus_reference_positionscan.bed"
    ]
    run_command(" ".join(can_cmd))
    
    # Modified dataset preparation
    mod_cmd = [
        "remora", "dataset", "prepare",
        str(args.pod5), str(args.mod_bam),
        "--output-path", f"8oxo{args.g_type}_chunks",
        "--refine-kmer-level-table", "stationaryfiles/levels.txt",
        "--refine-rough-rescale",
        "--motif", str(args.motif), str(args.mod_num),
        "--mod-base", "o", "8oxoG",
        "--focus-reference-positions", f"stationaryfiles/focus_reference_positions{args.g_type}.bed"
    ]
    run_command(" ".join(mod_cmd))

def dataset_configure(g_type):
    cmd = [
        "remora", "dataset", "make_config",
        "train_dataset.jsn",
        "can_all_chunks",
        f"8oxo{g_type}_chunks",
        "--dataset-weights", "1", "1",
        "--log-filename", "train_dataset.log"
    ]
    run_command(" ".join(cmd))

def dataset_train(args):
    cmd = [
        "remora", "model", "train",
        "train_dataset.jsn",
        "--model", "stationaryfiles/ConvLSTM_w_ref.py",
        "--device", "cuda:0",
        "--chunk-context", str(args.chunk_context), str(args.chunk_context),
        "--output-path", "train_results"
    ]
    run_command(" ".join(cmd))
    print("Training completed!")

def dataset_infer(args):
    # Canonical inference
    can_cmd = [
        "remora", "infer", "from_pod5_and_bam", 
        "--reference-anchored", 
        str(args.pod5), str(args.can_bam), 
        "--model", str(args.model), 
        "--out-bam", "can_infer.bam",
        "--log-filename", "can_infer.log", 
        "--device", "0"
    ]
    run_command(" ".join(can_cmd))
    
    # Modified inference
    mod_cmd = [
        "remora", "infer", "from_pod5_and_bam", 
        "--reference-anchored",
        str(args.pod5), str(args.mod_bam), 
        "--model", str(args.model), 
        "--out-bam", "mod_infer.bam",
        "--log-filename", "mod_infer.log", 
        "--device", "0"
    ]
    run_command(" ".join(mod_cmd))

def dataset_plotting(args):
    cmd = [
        "remora", "analyze", "plot", "ref_region",
        "--pod5-and-bam", str(args.can_pod5), str(args.can_sort_bam),
        "--pod5-and-bam", str(args.mod_pod5), str(args.mod_sort_bam),
        "--ref-regions", "stationaryfiles/focus_reference_positionscan.bed",
        "--highlight-ranges", f"stationaryfiles/focus_reference_positions{args.g_type}.bed",
        "--refine-kmer-level-table", "stationaryfiles/levels.txt",
        "--refine-rough-rescale",
        "--log-filename", "plot.log"
    ]
    run_command(" ".join(cmd))
    print("Plotting completed!")

def main():
    parser = argparse.ArgumentParser(description="Run Remora analysis pipeline")
    
    # Required arguments
    parser.add_argument("--pod5", required=True, help="Path to pod5 file or directory")
    parser.add_argument("--can-bam", required=True, help="Path to canonical BAM file")
    parser.add_argument("--motif", required=True, help="Motif sequence (e.g., TTAGGG)")
    parser.add_argument("--mod-num", required=True, help="Which base is modified (0 represents the first letter)")
    parser.add_argument("--mod-bam", required=True, help="Path to modified BAM file")
    parser.add_argument("--g-type", required=True, choices=["G29", "G30", "G31", "G35"], help="Which G is modified")
    
    # Optional arguments
    # Add argument for weights
    parser.add_argument("--plot", action="store_true", help="Generate plots")
    parser.add_argument("--can-pod5", help="Path to canonical pod5 file for plotting")
    parser.add_argument("--mod-pod5", help="Path to modified pod5 file for plotting")
    parser.add_argument("--can-sort-bam", help="Path to canonical sorted BAM file for plotting")
    parser.add_argument("--mod-sort-bam", help="Path to modified sorted BAM file for plotting")
    parser.add_argument("--train", action="store_true", help="Train a model")
    parser.add_argument("--infer", action="store_true", help="Perform inference")
    parser.add_argument("--model", help="Path to model for inference")
    parser.add_argument("--chunk-context", type=int, default=50, help="Chunk context for training")
    
    args = parser.parse_args()
    
    # Sanitize paths
    args.pod5 = sanitize_path(args.pod5)
    args.can_bam = sanitize_path(args.can_bam)
    args.mod_bam = sanitize_path(args.mod_bam)
    
    if args.plot:
        if not all([args.can_pod5, args.mod_pod5, args.can_sort_bam, args.mod_sort_bam]):
            parser.error("--plot requires --can-pod5, --mod-pod5, --can-sort-bam, and --mod-sort-bam")
        args.can_pod5 = sanitize_path(args.can_pod5)
        args.mod_pod5 = sanitize_path(args.mod_pod5)
        args.can_sort_bam = sanitize_path(args.can_sort_bam)
        args.mod_sort_bam = sanitize_path(args.mod_sort_bam)
    
    if args.infer and not args.model:
        parser.error("--infer requires --model")
    
    if args.model:
        args.model = sanitize_path(args.model)
    
    # Log parameters
    log_parameters(args)
    
    # Dataset preparation
    dataset_prepare(args)
    
    # Plotting
    if args.plot:
        dataset_plotting(args)
    
    # Training
    if args.train:
        dataset_configure(args.g_type)
        dataset_train(args)
    
    # Inference
    if args.infer:
        dataset_infer(args)

if __name__ == "__main__":
    main()
