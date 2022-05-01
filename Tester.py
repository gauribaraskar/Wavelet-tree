import sys
from WaveletTree import WaveletTree
from FileRead import FileRead

class Tester():
    def __init__(self,input_file,testcases_file,output_file,generated_output_file):
        self.input_file = input_file
        self.testcase_file = testcases_file
        self.output_file = output_file
        self.generated_output_file = generated_output_file

    def test(self):

        output_file = open(self.generated_output_file,'w')
        
        input_file = FileRead(self.input_file)
        input_file.read()

        string = input_file.data

        alphabet = list(set(input_file.data))

        #print("string ",string)

        testcase_file = open(self.testcase_file,'r')

        number_of_test_cases = int(testcase_file.readline())

        for i in range(number_of_test_cases):
            start_index, end_index = testcase_file.readline().split()

            #print(start_index,end_index)

            start_index = int(start_index)
            end_index = int(end_index)
            
            substring = string[start_index-1:end_index]
            #print(substring)
            alphabet = list(set(substring))

            #print(substring)
            # only for debugging
            alphabet.sort()

            #print(alphabet)

            tree = WaveletTree()
            tree.build(substring,alphabet)

            #tree.visualize_tree()

            number_of_queries = int(testcase_file.readline())

            for j in range(number_of_queries):

                #print("Query number: ",j)
                current_query = testcase_file.readline()
                current_query_args = current_query.split()
                current_query_type = current_query_args[0]

                if current_query_type == 'R':
                    pos = int(current_query_args[1])
                    char = current_query_args[2]
                    rank = tree.rank(char,pos,True)
                    output_file.write(str(rank) + "\n")
                elif current_query_type == 'S':
                    occ = int(current_query_args[1])
                    char = current_query_args[2]
                    select = tree.select(char,occ,True)
                    output_file.write(str(select) + "\n")
                elif current_query_type == 'A':
                    pos = int(current_query_args[1])
                    access = tree.access(pos)
                    output_file.write(str(access) + "\n")

        output_file.close()


    def diff(self):

        actual_output = open(self.output_file,'r')
        generated_output = open(self.generated_output_file,'r')

        line_1 = actual_output.readline()
        line_2 = generated_output.readline()


        testcases_count = 0
        failed = 0
        while line_1 or line_2:

            if line_1 != line_2:
                #print(line_1,line_2)
                failed += 1

            line_1 = actual_output.readline()
            line_2 = generated_output.readline()

            testcases_count += 1

        print("%d test cases failed out of %d."  % (failed,testcases_count))




if __name__ == '__main__':
    tester = Tester('input.txt','testcases.txt','out.txt','wavelet-out.txt')
    tester.test()
    tester.diff()




    



    
