from FileRead import FileRead
class OutputGenerator():
	def __init__(self,testcase_file):
		self.testcase_file = testcase_file


	def generate_actual_output(self):

		# Read input string
		input_file = FileRead('input.txt')
		input_file.read()

		text = input_file.data

		alphabet = list(set(input_file.data))

		TESTCASE_FILE = open(self.testcase_file,'r')


		OUTPUT_FILE = open('out.txt','w')

		number_of_test_cases = int(TESTCASE_FILE.readline())

		for i in range(number_of_test_cases):

			indices = TESTCASE_FILE.readline()
			indices = indices.split()

			start_index = int(indices[0])
			end_index = int(indices[1])

			# change to 0-indexed string
			start_index -= 1
			#end_index -=1 

			# extract substring
			string = text[start_index:end_index]


			#Read in number of queries
			number_of_queries = int(TESTCASE_FILE.readline())

			for j in range(number_of_queries):

				current_query = TESTCASE_FILE.readline()
				current_query_args = current_query.split()
				current_query_type = current_query_args[0]

				if current_query_type == 'R':
					pos = int(current_query_args[1])
					char = current_query_args[2]

					# Naive rank implementation
					count = 0
					alphabet = list(set(string))
					if char not in alphabet:
						count = -1
					else:
						for m in range(pos):
							if string[m]==char:
								count += 1
					OUTPUT_FILE.write(str(count) + "\n")
				elif current_query_type == 'S':
					occ = int(current_query_args[1])
					char = current_query_args[2]
					count = 0
					ans = - 1

					#Naive select implementation
					for m in range(len(string)):
						if string[m] == char:
							count += 1
							if count == occ:
								ans = m + 1
					OUTPUT_FILE.write(str(ans) + "\n")

				elif current_query_type == 'A':
					pos = int(current_query_args[1])

					# Naive Access implementation 
					OUTPUT_FILE.write(str(string[pos-1]) + "\n")

		OUTPUT_FILE.close()


if __name__ == '__main__':
	output = OutputGenerator('testcases.txt')
	output.generate_actual_output()


