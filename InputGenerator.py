import string
import random
from random import randint
from FileRead import FileRead
import time
from WaveletTree import WaveletTree
import gc
import numpy as np

class InputGenerator():
    def __init__(self,file,Fibonacci=None,length=10,alphabet=string.ascii_lowercase):

        self.query_choices = ['R']
        #self.query_choices = ['S']
        if file:
            self.file = file
            input_file = FileRead(self.file)
            input_file.read()
            self.length = len(input_file.data)
            self.alphabet = list(set(input_file.data))
            #input_file.close()
        elif Fibonacci:
            s = InputGenerator.generate_Fibonacci_string(Fibonacci)
            input_file = open('input.txt','w')
            input_file.write(s)
            input_file.close()
            self.length = len(s)
            self.alphabet = ['a','b','c']
        else:
            self.length = length
            self.alphabet = alphabet

    @staticmethod
    def generate_Fibonacci_string(n):
        s = ""
        for i in range(1,n+1):
            if i == 1:
                prev = "a"
                s =  "a"
            elif i == 2:
                curr = "bc"
                s = "bc"
            else:
                s = prev + curr
                prev = curr
                curr = s
        return s


    def generate_input_text(self):
        INPUT_FILE = open('input.txt','w')
        INPUT_FILE.write(''.join(random.choice(self.alphabet) for i in range(self.length)))
        INPUT_FILE.close()


    def generate_test_cases(self):

        # Output file 
        TEST_CASE_FILE = open('testcases.txt','w')

        #Input file for generating rank queries
        INPUT_FILE = open('input.txt','r')
        string = INPUT_FILE.readline()

        TEST_CASE_FILE.write(str(100) + "\n")

        # Number of test cases = 1000
        for i in range(100):

            # Generate two numbers for extracting substring
            start_index, end_index = random.sample(range(1,self.length),2)


            # swap start and end if reverse in order
            if start_index > end_index:
                temp = start_index
                start_index = end_index
                end_index = temp

            TEST_CASE_FILE.write(str(start_index) + " " + str(end_index) + "\n")
            substring_len = end_index - start_index + 1

            substring = string[start_index:end_index]

            alphabets = list(set(substring))
            
            # Generate number of test cases for this
            k = randint(1,10)

            TEST_CASE_FILE.write(str(k) + "\n")

            # Generate k queries
            for j in range(k):
                query_type = random.choice(self.query_choices)
                pos = random.choice(range(1,substring_len))

                if query_type in ['S','R']:
                    character = random.choice(alphabets)
                    query_string = str(query_type) + " " + str(pos) + " " + str(character) + "\n"
                else:
                    query_string = str(query_type) + " " + str(pos) + "\n"

                TEST_CASE_FILE.write(query_string)


        TEST_CASE_FILE.close()


    def generate_increasing_testcases(self):

        # Output file 
        TEST_CASE_FILE = open('testcases.txt','w')


        OUTPUT_FILE_Naive = open('time_naive.txt','w')

        OUTPUT_FILE_wavelet = open('time_wavelet.txt','w')

        OUTPUT_FILE_wavelet_opt = open('time_wavelet_jacob.txt','w')


        #Input file
        input_file = FileRead('input.txt')
        input_file.read()
        string = input_file.data

        print(len(string))

        alphabet = list(set(input_file.data))

        
        length_of_string = 10
        start_indices = []
        end_indices = []
        for i in range(8):
            start_indices.append(i+1)
            end_indices.append(i+length_of_string)
            length_of_string *= 10
            print(length_of_string)

        rank_query_args = []
        letters = []
        for i in range(8):
            length_of_string = end_indices[i] - start_indices[i] + 1
            rank_query_arg = random.choice(range(1,length_of_string))
            rank_query_args.append(rank_query_arg)
            char = random.choice(['A','T','G','C'])
            letters.append(char)




        gc.collect()
        total_time = [0] * 10
        for j in range(4):
            for i in range(8):
                substring = string[start_indices[i]-1:end_indices[i]]

                pos= rank_query_args[i]

                # Naive query  
                start_t = time.time()
                ans = substring[pos-1]
                end_t = time.time()
                total_time[i] += end_t - start_t

        for j in range(8):
            print(total_time[j])
            #total_time_avg[j] = sum(total_time[j])/len(total_time[j])
            OUTPUT_FILE_Naive.write(str(total_time[j]/4)+ "\n")




        gc.collect()
            # Wavelet tree


        #f = open('tree-building-tinme.txt','w')    
        total_time = [0] * 8
        total_time_jacob = [0] * 8
        for j in range(4):
            for i in range(8):

                print(i)
                char = letters[i]
                rank_query_arg = rank_query_args[i]

                substring = string[start_indices[i]-1:end_indices[i]]


                start_t = time.time()
                tree = WaveletTree()
                alphabet = list(set(substring))
                tree.build(substring,alphabet)
                end_t = time.time()

                print("built tree")

                #f.write(str(end_t - start_t)+ "\n")
                #total_time = 0
                # for j in range(5):
                start_t = time.time()
                rank = tree.access(rank_query_arg)
                end_t = time.time()
                total_time[i] += end_t - start_t


                # start_t = time.time()
                # rank = tree.select(char,rank_query_arg)
                # end_t = time.time()
                # total_time_jacob[i] += end_t - start_t
                #OUTPUT_FILE_wavelet_opt.write(str(end_t - start_t) + "\n")

        for j in range(8):
            #total_time_avg[j] = sum(total_time[j])/len(total_time[j])
            OUTPUT_FILE_wavelet.write(str(total_time[j]/4) + "\n")
            #OUTPUT_FILE_wavelet_opt.write(str(total_time_jacob[j]/4) + "\n")

        #f.close()
        OUTPUT_FILE_wavelet.close()
        OUTPUT_FILE_Naive.close()
        #OUTPUT_FILE_wavelet_opt.close()
        # print(start_indices)
        # print(end_indices)

        #start_len = 10






if __name__== '__main__':
    input_generator = InputGenerator('input.txt',None)
    input_generator.generate_increasing_testcases()
    #input_generator.generate_test_cases()
