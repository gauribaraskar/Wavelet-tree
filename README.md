# Wavelet-tree Implementation

### Prerequisites
1. python3
2. pip3
3. `pip3 install networkx`
4. `pip3 install pydot`
5. `pip3 install matplotlib`
6. `pip3 install memory_profiler`

### Folder structure
1. **testFiles** - This folder holds all the input.txt, testcases.txt and output.txt.
2. **InputGenerator.py** - This file generates input (either random/Fibonnaci) or reads input from a file. It has additional functions to generate either random test cases or multiplicative increasing testcases. It generates two files input.txt and testcases.txt. 
3. **OutputGenerator.py** - This file reads the input.txt and testcases.txt and generates an out.txt which contains actual outputs to all queries in testcases.txt. This one contains all naive implementations. 
4. **Tester.py** - This file runs the wavelet tree implementation on testcases.txt and diffs this generated output with the actual output. Additionally, it also give statistics like avg rank query time, avg select query time, etc.
5. **WaveletTreeNode.py** - This file holds the class for the tree node. The tree node stores the bit vector, pointers to left and right child, rank and sub rank vectors.
6. **WaveletTree.py** - This file holds the class for Wavelet tree. It stores the root node and alphabet for the input string. It contains implementations of Rank, Access and Select queries for all variations mentioned in our presentation.
7. **plot.py** - This file holds a utility function to plot two arrays in matplotlib.

### Instructions to run
1. **Generate input: <br/>**
    
    **1.1** <u>Generate Random String of length N</u> : <br/>
    	Change line #ADDLINENUMBER in **InputGenerator.py** to <br/>
    	`input_generator = InputGenerator(None, None, {N}, {alphabet_set})`<br/>
    	e.g.,<br/>
    	`input_generator = InputGenerator(None, None, 10000, string.ascii_lowercase)`<br/>
    	alphabet_set can be any list to alphabets that the user wants to use. 
    <br><br>
    
    
    **1.2** <u>Generate Fibonacci String for input</u>: <br/>
    	Change line #ADDLINENUMBER in **InputGenerator.py** to <br/>					
    	`input_generator = InputGenerator(None,{N})`<br/> 
    	Here, N is the number of times you want the fibonacci iteration to happen. 
    <br><br>
    
    
    **1.3** <u>Read input from a file</u>: <br/>
    	Change line #ADDLINENUMBER in **InputGenerator.py** to <br/>
    `	input_generator = InputGenerator('path/to/input.txt',None)` <br/>
    	Remember to place your `input.txt` in `testFiles/`.<br/>
    <br><br>
    Finally, in the terminal run `python3 InputGenerator.py`<br/>
    **Note:** To run any other pre-generated string file (dna50mb.txt, proteins.50mb, tm29) place the contents of the file in `input.txt`
    
    
    <br><br>
2. **Generate Actual output:** <br/>
    Run `python3 OutputGenerator.py`
    
    <br><br>
    
    
3. **Check correctness of outputs:** <br/>
    Run `python3 Tester.py`
    <br>Note: This file takes a lot of time to run if the number of test cases is large.
