import subprocess
import os
import argparse
import datetime
import csv
from pathlib import Path
import json

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
    
    # Create log entry for multi-G setup
    g_positions_str = ",".join([g.g_type for g in args.g_positions]) if hasattr(args, 'g_positions') else str(args.g_type)
    motifs_str = ",".join([f"{g.motif}:{g.mod_num}" for g in args.g_positions]) if hasattr(args, 'g_positions') else f"{args.motif}:{args.mod_num}"
    
    log_entry = [
        job_id,
        timestamp,
        str(args.pod5),
        str(args.can_bam),
        motifs_str,
        g_positions_str,
        "multi_g" if hasattr(args, 'g_positions') else "single_g",
        "plot" if args.plot else "no_plot",
        "train" if args.train else "no_train",
        "infer" if args.infer else "no_infer",
        str(args.model) if args.model else "no_model",
        str(args.chunk_context) if args.chunk_context else "default_chunk_context",
        str(args.dataset_weights) if hasattr(args, 'dataset_weights') else "default_weights"
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
                "JobID", "Timestamp", "Pod5", "CanBAM", "Motifs", "GPositions", 
                "Mode", "Plot", "Train", "Infer", "Model", "ChunkContext", "DatasetWeights"
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

class GPosition:
    """Class to hold information about a G position"""
    def __init__(self, g_type, motif, mod_num, mod_bam, pod5=None, focus_bed=None):
        self.g_type = g_type
        self.motif = motif
        self.mod_num = mod_num
        self.mod_bam = mod_bam
        self.pod5 = pod5
        self.focus_bed = focus_bed

def dataset_prepare_multi_g(args):
    """Prepare datasets for multiple G positions"""
    # Check if chunk folders already exist
    existing_chunks = []
    for g_pos in args.g_positions:
        if os.path.exists(f"can_{g_pos.g_type}_chunks") and os.path.exists(f"8oxo{g_pos.g_type}_chunks"):
            existing_chunks.append(g_pos.g_type)
    
    if existing_chunks:
        print(f"Chunk folders already exist for: {', '.join(existing_chunks)}. Skipping dataset preparation.")
        return

    # Canonical dataset preparation for each G position
    for g_pos in args.g_positions:
        can_cmd = [
            "remora", "dataset", "prepare",
            str(args.pod5), str(args.can_bam),
            "--output-path", f"can_{g_pos.g_type}_chunks",
            "--refine-kmer-level-table", "stationaryfiles/levels.txt",
            "--refine-rough-rescale",
            "--motif", str(g_pos.motif), str(g_pos.mod_num),
            "--mod-base-control",
            "--focus-reference-positions", f"stationaryfiles/focus_reference_positions{g_pos.g_type}.bed"
        ]
        run_command(" ".join(can_cmd))
    
    # Modified dataset preparation for each G position
    for g_pos in args.g_positions:
        pod5_path = g_pos.pod5 if g_pos.pod5 else args.pod5
        mod_cmd = [
            "remora", "dataset", "prepare",
            str(pod5_path), str(g_pos.mod_bam),
            "--output-path", f"8oxo{g_pos.g_type}_chunks",
            "--refine-kmer-level-table", "stationaryfiles/levels.txt",
            "--refine-rough-rescale",
            "--motif", str(g_pos.motif), str(g_pos.mod_num),
            "--mod-base", "o", "8oxoG",
            "--focus-reference-positions", f"stationaryfiles/focus_reference_positions{g_pos.g_type}.bed"
        ]
        run_command(" ".join(mod_cmd))

def dataset_prepare_single_g(args):
    """Prepare datasets for single G position (original functionality)"""
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

def dataset_configure_multi_g(args):
    """Configure dataset for multiple G positions"""
    cmd = ["remora", "dataset", "make_config", "train_dataset.jsn"]
    
    # Add canonical chunks for each G position
    for g_pos in args.g_positions:
        cmd.append(f"can_{g_pos.g_type}_chunks")
    
    # Add modified chunks for each G position
    for g_pos in args.g_positions:
        cmd.append(f"8oxo{g_pos.g_type}_chunks")
    
    # Add dataset weights
    if hasattr(args, 'dataset_weights') and args.dataset_weights:
        cmd.extend(["--dataset-weights"] + [str(w) for w in args.dataset_weights])
    else:
        # Default weights: 16 for canonical, 1 for modified (as in model141)
        default_weights = [16] * len(args.g_positions) + [1] * len(args.g_positions)
        cmd.extend(["--dataset-weights"] + [str(w) for w in default_weights])
    
    cmd.extend(["--log-filename", "train_dataset.log"])
    run_command(" ".join(cmd))

def dataset_configure_single_g(g_type):
    """Configure dataset for single G position (original functionality)"""
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

def dataset_infer_multi_g(args):
    """Perform inference for multiple G positions"""
    for g_pos in args.g_positions:
        pod5_path = g_pos.pod5 if g_pos.pod5 else args.pod5
        mod_cmd = [
            "remora", "infer", "from_pod5_and_bam", 
            "--reference-anchored",
            str(pod5_path), str(g_pos.mod_bam), 
            "--model", str(args.model), 
            "--out-bam", f"{g_pos.g_type}_infer.bam",
            "--log-filename", f"{g_pos.g_type}_infer.log", 
            "--device", "0"
        ]
        run_command(" ".join(mod_cmd))

def dataset_infer_single_g(args):
    """Perform inference for single G position (original functionality)"""
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

def parse_g_positions(g_positions_str):
    """Parse G positions from string format"""
    g_positions = []
    for g_str in g_positions_str.split(','):
        parts = g_str.strip().split(':')
        if len(parts) >= 4:
            g_type = parts[0]
            motif = parts[1]
            mod_num = int(parts[2])
            mod_bam = parts[3]
            pod5 = parts[4] if len(parts) > 4 else None
            focus_bed = parts[5] if len(parts) > 5 else None
            g_positions.append(GPosition(g_type, motif, mod_num, mod_bam, pod5, focus_bed))
    return g_positions

def main():
    parser = argparse.ArgumentParser(description="Run Remora analysis pipeline")
    
    # Mode selection
    parser.add_argument("--mode", choices=["single", "multi"], default="single",
                       help="Single G position or multiple G positions mode")
    
    # Required arguments for single mode
    parser.add_argument("--pod5", help="Path to pod5 file or directory")
    parser.add_argument("--can-bam", help="Path to canonical BAM file")
    parser.add_argument("--motif", help="Motif sequence (e.g., TTAGGG)")
    parser.add_argument("--mod-num", type=int, help="Which base is modified (0 represents the first letter)")
    parser.add_argument("--mod-bam", help="Path to modified BAM file")
    parser.add_argument("--g-type", choices=["G29", "G30", "G31", "G35"], help="Which G is modified")
    
    # Required arguments for multi mode
    parser.add_argument("--g-positions", help="Comma-separated G positions with format: G29:TTAGGG:3:/path/to/bam,G30:TTAGGG:4:/path/to/bam")
    parser.add_argument("--dataset-weights", nargs='+', type=int, 
                       help="Dataset weights for canonical and modified chunks (e.g., 16 16 16 1 1 1 1)")
    
    # Optional arguments
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
    
    # Validate arguments based on mode
    if args.mode == "single":
        if not all([args.pod5, args.can_bam, args.motif, args.mod_num, args.mod_bam, args.g_type]):
            parser.error("Single mode requires --pod5, --can-bam, --motif, --mod-num, --mod-bam, and --g-type")
    else:  # multi mode
        if not all([args.pod5, args.can_bam, args.g_positions]):
            parser.error("Multi mode requires --pod5, --can-bam, and --g-positions")
        args.g_positions = parse_g_positions(args.g_positions)
        if not args.g_positions:
            parser.error("Failed to parse G positions. Use format: G29:TTAGGG:3:/path/to/bam,G30:TTAGGG:4:/path/to/bam")
    
    # Sanitize paths
    if args.mode == "single":
        args.pod5 = sanitize_path(args.pod5)
        args.can_bam = sanitize_path(args.can_bam)
        args.mod_bam = sanitize_path(args.mod_bam)
    else:
        args.pod5 = sanitize_path(args.pod5)
        args.can_bam = sanitize_path(args.can_bam)
        for g_pos in args.g_positions:
            g_pos.mod_bam = sanitize_path(g_pos.mod_bam)
            if g_pos.pod5:
                g_pos.pod5 = sanitize_path(g_pos.pod5)
    
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
    if args.mode == "single":
        dataset_prepare_single_g(args)
    else:
        dataset_prepare_multi_g(args)
    
    # Plotting
    if args.plot:
        dataset_plotting(args)
    
    # Training
    if args.train:
        if args.mode == "single":
            dataset_configure_single_g(args.g_type)
        else:
            dataset_configure_multi_g(args)
        dataset_train(args)
    
    # Inference
    if args.infer:
        if args.mode == "single":
            dataset_infer_single_g(args)
        else:
            dataset_infer_multi_g(args)

if __name__ == "__main__":
    main()
