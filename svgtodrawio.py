from sys import argv
import re
from os import listdir, mkdir, path
from string import printable
from svgcolorreplacer import search_and_replace
from base64 import b64encode

PRINTABLE = set(printable)

# Takes an svg string of an image and returns the draw.io compatible XML string
def generate_xml_string(svg_string, title):
    imagedata = b64encode(svg_string.encode('ascii')).decode('ascii')

    # Extract image dimensions from svg
    viewbox_start = svg_string.find('viewBox="')
    svg_string_after_viewbox = svg_string[viewbox_start+9:]
    viewbox_string = svg_string_after_viewbox[:svg_string_after_viewbox.find('"')]

    minx, miny, w, h = viewbox_string.split(' ')
    aspect = "fixed"
    return f'\t{{\n\t"data":"data:image/svg+xml;base64,{imagedata};",\n\t\t"w":{w},\n\t\t"h":{h},\n\t\t"title":"{title}",\n\t\t"aspect":"{aspect}"\n\t}},\n'


def convert(input_file_path, color, output_folder_name=None):
    # Loop over all files in input folder
    xml_library_string = '<mxlibrary>[\n'
    if output_folder_name is None:
        output_folder_name = path.dirname(path.abspath(input_file_path)) 
        xml_library_file_name = output_folder_name + ".xml"
    else:
        if not path.exists(output_folder_name):
            mkdir(output_folder_name)
        child_folder = path.basename(input_file_path)
        xml_library_file_name = path.join(output_folder_name, child_folder)   + ".xml"
        
    # Regex pattern to match any five digits followed by "-icon-service"
    pattern = r"\d{5}-icon-service-?"

    print("Converting svg files...")

    for input_filename in listdir(input_file_path):
        if input_filename.endswith(".svg"):
            #   Read file to string
            file_to_open = path.join(input_file_path, input_filename)
            with open(file_to_open, "r") as svg_file:
                svg_string = svg_file.read()
                if len("".join(filter(lambda x: x not in PRINTABLE, svg_string))) > 0:
                    svg_string = "".join(filter(lambda x: x in PRINTABLE, svg_string))
            if color is not None:
                #   Replace color in string
                new_svg_string = search_and_replace(svg_string, color)
            else:   
                new_svg_string = svg_string
            title_full = path.splitext(input_filename)[0]

            # Replace the matched pattern with an empty string
            title = re.sub(pattern, "", title_full)

            title = "az " + title.replace('-', ' ')

            xml_string = generate_xml_string(new_svg_string, title)
            xml_library_string = xml_library_string + xml_string
    
    xml_library_string = xml_library_string[:-2] + "\n]</mxlibrary>"
    with open(xml_library_file_name, "w") as xml_library_file:
        xml_library_file.write(xml_library_string)
    print(f'Conversion successful. Library saved as "{xml_library_file_name}".')

if __name__ == "__main__":
    color = None
    # Check if input arguments are present
    print("Checking input arguments...")
    try:
        input_file_path = argv[1]
        if input_file_path.startswith('#'):
            print("Only color provided as input.")
            argv[2] = input_file_path
            raise IndexError 
    except IndexError:
        input_file_path = input("Enter the folder path with the svg files: ")        
    if len(argv)>2:
        try:
            color = argv[2]
        except IndexError:
            color = input("Enter the color you want for the svg files: ")
    convert(input_file_path, color)