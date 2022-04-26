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
    alphabet.sort()

    tree = WaveletTree()
    tree.build(input_file.data,alphabet)

    # Printing the tree
    #tree.visualize_tree()
    # i = 10
    # s = 'a'
    # rank = tree.rank(s,i)
    # print("Rank of character %s till position %d is %d" % (s,i,rank))

    i = 3
    s = 'c'
    position = tree.select(s,i)
    print("The answer to select query is %s" % position)


    



    
