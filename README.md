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


## Comments for practical course

#### Changes from 04.02 to 05.02
- added the `-o` flag with which you can specify the name of your resulting multiple alignment graph.
- fixed the very ugly node IDs in the output_graphs. They now look better (relatively) and are actually reparsable, i.e. realignable.
- The scoring table layout changed, because there were issues with some editors concerning the tab spaces. This is why tabs were replaced by `labelsep` which you can specify in custom.py. The default is space. If you use labels that include spaces, you should change `labelsep` accordingly.
- added some more comments to the functions and the code in general here and there.

#### Please note
- At the beginning of your day, please take the time to pull and reinstall `multiVitamin` (if you previously installed it via pip3). For the rest of the day, unless otherwise communicated, pulls from time to time should be enough, you should not need to reinstall the package after each pull.
- Due to time reasons, many useful features are not indicated/explained in the [multivitaminReadme.pdf](multivitaminReadme.pdf), if you experience any trouble with the program, feel free to ask. I will try and add the missing information to the Readme as soon as possible.
- The `subVF2` algorithm is the only one suitable for multiple alignment. You do not need to specify it as it is also the default algorithm.
- The greedy multiple alignment algorithm is the only one available at the moment due to its acceptable running time. If you experience otherwise, please tell me and I will implement a progressive version.
- There are many useful features in the [`custom.py`](multivitamin/custom.py) script explained inside.
- Many changes had to be done last minute, unfortunately. So you could quite likely experience some bugs here and there. Please let me know, if anything appears odd to you. Many excuses in advance!

## Installation instructions

Clone the repo from github with
```
git clone https://github.com/mk36fyvy/multivitamin.git
```
There are two possibilities to run `multiVitamin`.

#### pip3 install

Navigate to the directory containing the setup.py file
```
cd multivitamin/
```
If you have **root permissions**, run
```
pip3 install -e .
```
and you're good to go.

If you **do not have root permissions**, run
```
pip3 install -e . --user
```
to install `multiVitamin` locally. Then put it into your PATH, so it can be run from everywhere within the system.
```
echo 'export PATH=$PATH:~/.local/bin/' >> ~/.bashrc
```
After this, you will need to either run `source ~/.bashrc` or open a new terminal window.

Done, now you can run multiVitamin in the command shell. You can test if the installation was successful by typing
```
multiVitamin -h
```

#### Without installation

You can also run the package without installation by running
```
[path_to_dir]/multivitamin/run.sh 
```
followed by the standard input specified in
```
[path_to_dir]/multivitamin/run.sh -h 
```

## How to use

#### Basics

You can get an overview of the basic flags and functionalities by typing
```
multiVitamin -h
```
A basic run example looks like the following
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

Pairwise alignments are scored in a very generic and basic way by default: exact matches are rewarded, gaps are punished, both with fixed values (4 and -1 respectively, editable [here](multivitamin/utils/scoring.py) in `score_without_matrix()`). 

With the flag `-t` you can provide a scoring table with custom sum-of-pair scores. A table example can be found [here](scoring_table_example.txt).

If you do not want to type all the pairings of the labels yourself, just specify all single labels like so
```
 -\t-2
 C\t2
 N\t2
```
where `\t` indicates a `tab` spacing. 

This specifies the exact match score, i.e for instance `match(C,C)` (the gap symbol `-` has to be indicated in the first line, if you want a different gap score than -1. Simply omit it, if this is not the case.). 

If you run the program with this minimal scoring table, you will get a warning with all the missing pairs written out. Like that, you can simply copy and paste those of interest into your scoring table file, change the scores and rerun the program.

You can also forbid the alignment of nodes with specific labels. Check [`custom.py`](multivitamin/custom.py) for this. 

## Further reading

More information on how to use the module can be found [here](multivitaminReadme.pdf).
