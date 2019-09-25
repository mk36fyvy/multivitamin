import os

from multivitamin.utils.parser import parse_graph


def process_file(filename):
    print(filename)
    if os.path.isdir(filename):
        print("parsing .graph files in directory")
        return process_directory(filename)
    else:
        if not filename.endswith('.graph'):
            raise Exception("{} is not a valid input (not a .graph file)!".format(filename)) 
        return parse_graph( filename ) # this is what is done to the parsed command-line arguments (graphs)
        
    

def process_directory(directory_name):
    graphs = []
    for filename in os.listdir(directory_name):
        if filename.endswith('.graph'):
            
            graphs.append( process_file(os.path.join(directory_name, filename)) )
    if not graphs:
        raise Exception("No .graph file found in the given directory! Aborting...")
    return graphs