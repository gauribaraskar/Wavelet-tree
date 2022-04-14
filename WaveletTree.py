from WaveletTreeNode import WaveletTreeNode

'''
Wavelet tree data structure:
1. Characteristics
	a.
2. Methods
	a. 
'''

class WaveletTree:
	def __init__(self):
		self.root = None

	def build(self,string,alphabet):
		#print(string)
		self.root = WaveletTreeNode(alphabet)
		self.__build(self.root,alphabet,string)
	
	@staticmethod
	def __build(node,alphabet,string):
		if len(alphabet) in range(2):
			return

		half = len(alphabet) // 2
		left_alphabet = alphabet[:half]
		right_alphabet = alphabet[half:]

		string_to_bit = []
		print(string)
		[string_to_bit.append('0' if c in left_alphabet else '1') for c in string]
		print(''.join(string_to_bit))
		node.add_bit(''.join(string_to_bit))

		# Split data for left and right node
		left_data = []
		right_data = []
		for bit in string:
			if bit in left_alphabet:
				left_data.append(bit)
			else:
				right_data.append(bit)

		# Create left && right node and build recursively
		node.left = WaveletTreeNode(left_alphabet, node)
		WaveletTree.__build(node.left, left_alphabet, left_data)
		node.right = WaveletTreeNode(right_alphabet, node)
		WaveletTree.__build(node.right, right_alphabet, right_data)

	def preorder_traversal(self):
		self.__preorder(self.root)

	@staticmethod
	def __preorder(node):
		if node is None:
			return
		else:
			print(node.bit_vector,node.alphabet)
			WaveletTree.__preorder(node.left)
			WaveletTree.__preorder(node.right)

