import sys
import os
import shutil
import subprocess
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='GitHub-ForceLargeFiles_reverse')

    parser.add_argument('--root_dir', type=str, default=os.getcwd(), help="Root directory to start traversing. Defaults to current working directory.")
    parser.add_argument('--delete_partitions', type=bool, default=True, help="Do you want to delete the partition archives after extracting the original files?")
    
    args = parser.parse_args()
    return args


def check_7z_install():
    if shutil.which("7z"):
        return True
    else:
    	sys.exit("ABORTED. You do not have 7z properly installed at this time. Make sure it is added to PATH.")


def is_partition(f_full_dir):
    return any(f_full_dir.endswith(ext) for ext in [".7z.001", ".xz.001", ".bzip2.001", ".gzip.001", ".tar.001", ".zip.001", ".wim.001"])


def reverse_root_dir(args):
    for root, _, files in os.walk(args.root_dir):
        for f in files:
            f_full_dir = os.path.join(root, f)

            if is_partition(f_full_dir):
                prc = subprocess.run(["7z", "e", f_full_dir, "-o" + root])
                
                if args.delete_partitions and prc.returncode == 0:
                    f_noext, _ = os.path.splitext(f)
                    os.chdir(root)
                    os.system("rm" + " \"" + f_noext + "\"*")


if __name__ == '__main__':
    check_7z_install()
    reverse_root_dir(parse_arguments())