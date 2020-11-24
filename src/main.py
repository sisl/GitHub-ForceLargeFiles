import sys
import os
import shutil
import subprocess
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description='GitHub-ForceLargeFiles')

    parser.add_argument('--root_dir', type=str, default=os.getcwd(), help="Root directory to start traversing. Defaults to current working directory.")
    parser.add_argument('--delete_original', type=bool, default=True, help="Do you want to delete the original (large) file after compressing to archives?")

    # The two arguments below default to compressing files only if they are over 100 MB.
    parser.add_argument('--threshold_size', type=int, default=100, help="Max threshold of the original file size to split into archive. I.e. files with sizes below this arg are ignored.")
    parser.add_argument('--threshold_size_unit', type=str, default='m', choices=['b', 'k', 'm', 'g'], help="Unit of the threshold size specified (bytes, kilobytes, megabytes, gigabytes).")
    
    # The two arguments below default to creating archives with a maximum size of 95 MB.
    parser.add_argument('--partition_size', type=int, default=95, help="Max size of an individual archive. May result in actual partition size to be higher than this value due to disk formatting. In that case, reduce this arg value.")
    parser.add_argument('--partition_size_unit', type=str, default='m', choices=['b', 'k', 'm', 'g'], help="Unit of the partition size specified (bytes, kilobytes, megabytes, gigabytes).")
    
    args = parser.parse_args()
    return args


def check_7z_install():
    if shutil.which("7z"):
        return True
    else:
    	sys.exit("ABORTED. You do not have 7z properly installed at this time. Make sure it is added to PATH.")


def is_over_threshold(f_full_dir, args):

    size_dict = {
        "b": 1e-0,
        "k": 1e-3,
        "m": 1e-6,
        "g": 1e-9
    }

    if os.stat(f_full_dir).st_size * size_dict[args.threshold_size_unit] >= args.threshold_size:
        return True
    else:
        return False


def traverse_root_dir(args):
    for root, dirs, files in os.walk(args.root_dir):
#        for d in dirs:
#            print(os.path.join(root, d))
        for f in files:
            f_full_dir = os.path.join(root, f)

            if is_over_threshold(f_full_dir, args):
                f_full_dir_noext, _ = os.path.splitext(f_full_dir)
                subprocess.run(["7z", "-v" + str(args.partition_size) + args.partition_size_unit, "a", f_full_dir_noext + ".7z", f_full_dir])
                
                if args.delete_original:
                    os.remove(f_full_dir) 


if __name__ == '__main__':
    check_7z_install()
    traverse_root_dir(parse_arguments())