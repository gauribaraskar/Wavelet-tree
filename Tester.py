import sys

from FileRead import FileRead
from WaveletTree import WaveletTree
#from multiprocessing import Process, Queue
import time
import matplotlib.pyplot as plt
import os 
import psutil
import random
import threading


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

    # Printing the tree and testing the tree
    #tree.preorder_traversal()
    #tree.visualize_tree()


    #Writing results to a file
    output_file = open('5MB.txt','w')

    # Read queries through file and plot graphs for time
    query_file = open('query.txt', 'r')
    
    # Store time for jacobsons and normal query
    position = []
    characters = []
    count = 0
    while True:
        count += 1
     
        # Get next line from file
        line = query_file.readline()
     
        # if line is empty
        # end of file is reached
        if not line:
            break

        args = line.split()
        if args[0] == 'R':
            i = int(args[1])
            s = args[2]

            positions.append(i)
            characters.append(s)

            output_file.write("Naive Rank\n")
            start_time = time.time()
            rank = tree.rank(s,i,False)
            print("Rank of character %s till position %d is %d" % (s,i,rank))
            end_time = time.time()
            output_file.write(str(end_time - start_time))
            output_file.write("\n")


            output_file.write("Jacobsons Rank\n")
            # print("Jacobsons")
            start_time = time.time()
            rank = tree.rank(s,i,True)
            print("Rank of character %s till position %d is %d" % (s,i,rank))
            end_time = time.time()
            output_file.write(str(end_time - start_time))
            output_file.write("\n")
        else:
            continue
        #print("Line{}: {}".format(count, line.strip()))
 
    query_file.close()  



    #for position,character in zip(positions,characters):


    #Plot the times
    # print(jacobsons_query_time)
    print(naive_query_times)
    # plt.plot(range(1,len(jacobsons_query_time)), jacobsons_query_time, 'g', label='Jacobsons rank')
    # plt.plot(range(1,len(naive_query_times)), naive_query_times, 'b', label='Naive rank')    
    # plt.show()

    



    
