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

element_to_atomcolor = {
    "H"  : "#f0f3f4",
    "C"  : "",
    "N"  : "#2471a3",
    "O100"  : "#e74c3c",
    "O80"  : "#e74c3c",
    "O60"  : "#e74c3c",
    "F"  : "",
    "Na" : "",
    "Mg" : "",
    "P"  : "",
    "S"  : "#f1c40f",
    "Cl" : "#229954",
    "K"  : "",
    "Fe" : "",
    "Br" : "",
    "I"  : "",
}

element_to_textcolor = {
    "H"     : "#f0f3f4",
    "C100"  : "#566573",
    "C70"   : "#abb2b9",
    "C51"   : "#d6dbdf",
    "N100"  : "#2471a3",
    "N70"   : "#5499c7",
    "N51"   : "#aed6f1",
    "O100"  : "#e74c3c",
    "O70"   : "#f1948a",
    "O51"   : "#fadbd8",
    "F100"  : "#0affe5",
    "F70"   : "#9bfff4",
    "F51"   : "#dafffb",
    "Na100" : "",
    "Na70"  : "",
    "Na51"  : "",
    "Mg100" : "",
    "Mg70 " : "",
    "Mg51 " : "",
    "P100"  : "#8e44ad",
    "P70 "  : "#bb8fce",
    "P51"   : "#e8daef",
    "S100"  : "#fff000",
    "S70"   : "#fff997",
    "S51"   : "#fdfbd1",
    "Cl100" : "#229954",
    "Cl70"  : "#7fdda6",
    "Cl51"  : "#c0f1d5",
    "K100"  : "",
    "K70"   : "",
    "K51"   : "",
    "Fe100" : "#7e2600",
    "Fe70"  : "#ca460c",
    "Fe51"  : "#ff8854",
    "Br100" : "",
    "Br70"  : "",
    "Br51"  : "",
    "I100"  : "",
    "I70"   : "",
    "I51"   : "",
    "dummy" : "#abb2b9"
}

def get_size_by_element( label ):
    if label in element_to_size:
        return element_to_size[label]
    else:
        return "10"
        
        