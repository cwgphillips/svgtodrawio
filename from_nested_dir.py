from os import listdir, path
from sys import argv
import svgtodrawio

def main():
    output_parent_folder = path.normpath(parent_file_path) + "_Exported_Library"

    for dirnames in listdir(parent_file_path):
        print(f"dirnames: {dirnames}")
        child_file_path = path.normpath(path.join(parent_file_path, dirnames))
        print(f"\t\t### Exporting {child_file_path}")
        svgtodrawio.convert(child_file_path, None, output_parent_folder)

if __name__ == "__main__":
    parent_file_path = argv[1]
    main()