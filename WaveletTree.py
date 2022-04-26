from WaveletTreeNode import WaveletTreeNode
import networkx as nx
import pydot
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import math
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
	
	def rank(self, c, i):
		return WaveletTree.__rank(self.root, c, i)

	def access(self,i):
		return WaveletTree.__access(self.root,i)

	def select(self,c,occ_number):
		return WaveletTree.__select(self.root,c,occ_number)

	@staticmethod
	def __build(node,alphabet,string):
		if len(alphabet) in range(2):
			return

		half = math.ceil(len(alphabet) / 2)
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

	def set_node_sizes(g):
		sizes = []
		for node in g.nodes():
			#print(node)
			sizes.append(len(node)*100)
		return sizes

	## change to do  better
	def visualize_tree(self):
		G = nx.DiGraph()
		G = self.__add_edges(self.root,G)
		pos = graphviz_layout(G, prog='dot')
		sizes = WaveletTree.set_node_sizes(G)
		#print(edges)
		nx.draw_networkx_nodes(G, pos,node_shape='s',edgecolors='black')
		# # Set edge color to red
		
# 		nodes.set_edgecolor('r')
		nx.draw_networkx_edges(G,pos) # draw edges
		nx.draw_networkx_labels(G,pos) # draw node labels
		plt.show()	

	@staticmethod
	def __rank(node, c, i):
		# Check if we have reachead leaf
		if len(node.alphabet) == 1:
			return i

		c_in_left_child = c in node.left.alphabet

		bit_for_c = '0' if c_in_left_child else '1'

		# binary rank calculation
		# count the number of bit until this point
		# try jacobsons rank for faster query times
		i_parent = sum(1 for bit in node.bit_vector[:i] if bit==bit_for_c)
	
		#print(i_parent)

		child = node.left if c_in_left_child else node.right

		return WaveletTree.__rank(child, c, i_parent)

	def binary_rank(bit_vector,bit):
		return sum(1 for b in bit_vector if b==bit)

	@staticmethod
	def __access(node,i):

		if len(node.alphabet) == 1:
			return node.alphabet[0]

		bit = node.bit_vector[i]
		if bit == '1':
			child = node.right
			rank = WaveletTree.binary_rank(node.bit_vector,1)
		else:
			child = node.left
			rank = WaveletTree.binary_rank(node.bit_vector,0)

		return WaveletTree.__access(child,rank)

	def find_leaf(node,c):
		if len(node.alphabet) == 1:
			return node
		child = node.left if c in node.left.alphabet else node.right

		return WaveletTree.find_leaf(child,c)

	@staticmethod
	def __select(node,c,occ_number):
		leaf = WaveletTree.find_leaf(node,c)
		#print(leaf.parent is None)
		if leaf.parent:
			bit = 1 if (leaf.parent.right == leaf) else 0
			return WaveletTree.__select_helper(leaf.parent,bit,occ_number)
		else:
			return occ_number
			
	# clarks select
	def binary_select(bit_vector,num_occurence,bit):
		count = 0
		for i,b in enumerate(bit_vector):
			if b == bit:
				count += 1
				if count == num_occurence:
					return i

	def __select_helper(node,bit,occ_number):
		position = WaveletTree.binary_select(node.bit_vector,occ_number,bit)

		if node.parent is None:
			return position
		else:
			bit = 1 if (node.parent.right == node) else 0
			return WaveletTree.__select_helper(node.parent,bit,position)




