import os
from argparse import ArgumentParser
def install_grc(c_dir, recur=True):
    files = os.listdir(c_dir)
    for c_file in files:
        
        if os.path.isdir(c_dir + "/" + c_file):
            # if directory check if we recursively find grc files
            if recur:
                install_grc(c_dir + "/" + c_file)
        else:

            if c_file[-4:] == ".grc":
                # grc file.
                try:
                    os.system("grcc %s"%(c_dir + "/" + c_file))
                except Exception as e:
                    print("Exception caught = " + str(e))

if __name__ == "__main__":
    parser = ArgumentParser(description="Install all GRC")
    parser.add_argument("--directory", default="grc",
        help="Directory of GRC files")
    parser.add_argument("--recursive", action="store_true",
        help="Recursively search directory")
    args = parser.parse_args()

    install_grc(args.directory, args.recursive)
