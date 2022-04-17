from WaveletTreeNode import WaveletTreeNode
import networkx as nx
import pydot
#xfrom networkx import to_agraph
#from networkx.drawing.nx_pydot import spring_layout
import matplotlib.pyplot as plt

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
		#print(string)
		[string_to_bit.append('0' if c in left_alphabet else '1') for c in string]
		#print(''.join(string_to_bit))
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

	@staticmethod
	def __add_edges(node,g):
		if node and node.bit_vector!='':
			g.add_node(str(node.bit_vector))
			if node.parent:
				g.add_edge(str(node.parent.bit_vector),str(node.bit_vector))
			#print(node.bit_vector,node.alphabet)
			WaveletTree.__add_edges(node.left,g)
			WaveletTree.__add_edges(node.right,g)
		return g

	def visualize_tree(self):
		G = nx.DiGraph()
		G = self.__add_edges(self.root,G)
		#print(edges)
		A = nx.nx_agraph.to_agraph(G)
		nx.draw(G, node_size=600, node_color='w', alpha=0.4, node_shape='d')
		A.layout('dot', args='-Nfontsize=10 -Nwidth=".2" -Nheight=".2" -Nmargin=0 -Gfontsize=8')
		A.draw('test.png')

