import os

from multivitamin.utils.parser import parse_graph


def process_file(filename):
    parse_graph( filename ) # this is what is done to the parsed command-line arguments (graphs)
        
    

def process_directory(directory_name):
    found_graph = False
    for filename in os.listdir(directory_name):
        if filename.endswith('.graph'):
            found_graph = True
            process_file(os.path.join(directory_name, filename))
    if not found_graph:
        raise Exception("No .graph file found in the given directory! Aborting...")
