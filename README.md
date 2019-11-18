# multiVitamin
In-Terminal multiple alignment tool for graphs

multiVitamin is a software package which allows users to perform multiple alignments with graphs. 
There are two algorithms available for this task. The Bron Kerbosch and the VF2 algorithm. Details 
on the algorithms can be found in the theory section. The main function of the package is to align 
two or more graphs following a binary alignment guide tree containing the "best" alignment procedure. 
The resulting multiple graph alignment is represented as one single graph itself. Next to this main 
function, there is also the possibility to show all co-optimals of an alignment between 2 graphs or 
to view graphical representations of graphs.  
Sounds exciting, so let's get started!


## Installation instructions

Clone the repo from github with 
```
git clone https://github.com/mk36fyvy/multivitamin.git
```
Navigate to the directory containing the setup.py file 
```
cd [yourDir]/multivitamin/multivitamin
```
and type
```
pip3 -e install .
```
Done, now you can run multiVitamin in the command shell. You can test if the installation was successful by typing
```
multiVitamin -h
```

## How to use

You can get an overview of the basic functionalities by typing
```
multiVitamin -h
```

Examples on how the graph file looks like can be found in graph_examples inside the module


## Further reading

More information on how to use the module can be found here soon.
