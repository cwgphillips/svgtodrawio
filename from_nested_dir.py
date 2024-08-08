from os import listdir, path
import re
from sys import argv
import svgtodrawio

def main():
    output_parent_folder = path.normpath(parent_file_path) + "_Exported_Library"

    for dirnames in listdir(parent_file_path):
        print(f"dirnames: {dirnames}")
        child_file_path = path.normpath(path.join(parent_file_path, dirnames))
        print(f"\t\t### Exporting {child_file_path}")
        svgtodrawio.convert(child_file_path, None, output_parent_folder)

    output_text_for_vs_code(output_parent_folder, custom_lib)

def output_text_for_vs_code(output_parent_folder, custom_lib_prefix_in=None):
    custom_lib_prefix = "" if custom_lib_prefix_in is None else custom_lib_prefix_in
    custom_lib = "Custom Library"
    output_text = []
    output_text.append(""""hediet.vscode-drawio.customLibraries": [""")

    for file_name in listdir(output_parent_folder):
        full_file_name  = path.join(output_parent_folder, file_name)
        file_path = re.escape(path.dirname(full_file_name))
        lib_name = path.splitext(path.basename(file_name))[0].title()
        extension = path.splitext(path.basename(file_name))[1].title()

        if extension.lower() != ".xml":
            continue
        full_file_name = file_path + "\\\\" + lib_name + extension
        
        output_text.append(f"""\n\t{{"file":"{full_file_name}", "libName": "{custom_lib_prefix}{lib_name}", "entryId": "{custom_lib}"}},""")
    
    output_text.append("""\n]""")
      
    output_file_name = "settings_for_vs_code.json"
    output_file_full = path.join(output_parent_folder, output_file_name)

    with open(output_file_full, "w") as file_out:
        file_out.writelines(output_text)

if __name__ == "__main__":
    parent_file_path = argv[1]
    try: 
        custom_lib = argv[2]
    except IndexError: 
        custom_lib = None
    main()