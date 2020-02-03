# multiVitamin
In-Terminal multiple alignment tool for graphs

`multiVitamin` is a software package which allows users to perform multiple alignments with graphs.
There are three algorithms available for this task: The `Bron-Kerbosch` and the `VF2` algorithm and a custom subgraph-isomorphism-VF2 (called `subVF2`). Details
on the algorithms can be found in the theory section [here](multivitaminReadme.pdf). The main function of the package is to align
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

#### Basics

You can get an overview of the basic functionalities by typing
```
multiVitamin -h
```
A run example would look like the following
```
multiVitamin -a subVF2 -i graph1.graph graph2.graph graph3.graph
```
or simply
```
multiVitamin -i .
```
This will align all the .graph files (mind the extension!) in the current working directory.

Examples on what our custom graph file format looks like can be found in [graph_examples](graph_examples) inside the module.

#### Custom scoring

With the flag `-t` you can specify a scoring table with custom sum-of-pair scores. A table example can be found [here](scoring_table_example.txt).

If you do not want to type all the pairings of the labels yourself, just specify all single labels like so
```
 -\t-2
 C\t2
 N\t2
```
This specifies the exact match score (the gap symbol `-` has to be indicated in the first line, if you want a different gap score than -1). If you run the program with this minimal scoring table, you will get a warning with all the missing pairs written out. Like that, you can simply copy and paste those into your scoring table file, change the scores and rerun the program.

## Notes for practical course

Please note
- Due to time reasons, many useful features are not indicated/explained in the [multivitaminReadme.pdf](multivitaminReadme.pdf), if you experience any trouble with the program, feel free to ask. I will try, to add the missing information to the Readme as soon as possible.
- The `subVF2` algorithm is the only one suitable for multiple alignment. You do not need to specify it as it is also the default algorithm.
- The greedy multiple alignment algorithm is the only one available at the moment due to its acceptable running time. If you experience otherwise, please tell me and I will implement a progressive version.
- There are many useful features in the [`custom.py`](custom.py) script explained inside.
- Many changes had to be done last minute, unfortunately. So you could quite likely experience some bugs here and there. Please let me know, if anything appears odd to you. Many excuses in advance!

## Further reading

More information on how to use the module can be found [here](multivitaminReadme.pdf).
