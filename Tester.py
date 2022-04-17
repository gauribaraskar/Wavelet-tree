import sys

from FileRead import FileRead
from WaveletTree import WaveletTree


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Missing arguments!')
        exit(-1)

    input_file = FileRead(sys.argv[1])
    input_file.read()

    # Construct alphabet from data string
    alphabet = list(set(input_file.data))
    # not necessary
    #alphabet.sort()

    tree = WaveletTree()
    tree.build(input_file.data,alphabet)

    ## Printing the tree
    tree.visualize_tree()

    

    
