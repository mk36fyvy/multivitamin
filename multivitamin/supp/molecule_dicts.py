atomic_number_to_element = {
    "1"  : "H",
    "5"  : "B",
    "6"  : "C",
    "7"  : "N",
    "8"  : "O",
    "9"  : "F",
    "11" : "Na",
    "12" : "Mg",
    "15" : "P",
    "16" : "S",
    "17" : "Cl",
    "19" : "K",
    "26" : "Fe",
    "35" : "Br",
    "53" : "I",
    "-"  : "-"
}
# gap to gap translation is necessary to preserve them 

element_to_size = {
    "H"  : "1",
    "B"  : "10",
    "C"  : "12",
    "N"  : "14",
    "O"  : "16",
    "F"  : "11",
    "Na" : "8",
    "Mg" : "10",
    "P"  : "15",
    "S"  : "18",
    "Cl" : "23",
    "K"  : "9",
    "Fe" : "12",
    "Br" : "24",
    "I"  : "28",
}


def get_size_by_element( label ):
    if label in element_to_size:
        return element_to_size[label]
    else:
        return "10"
        
        