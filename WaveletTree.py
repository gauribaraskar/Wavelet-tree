from WaveletTreeNode import WaveletTreeNode
import networkx as nx
import pydot
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import math
import time


class WaveletTree:
	def __init__(self):
		self.root = None

	def build(self,string,alphabet):
		#print(string)
		self.root = WaveletTreeNode(alphabet)
		self.__build(self.root,alphabet,string)
	
	def rank(self, c, i,Jacobsons=False):
		return WaveletTree.__rank(self.root, c, i,Jacobsons)

	def access(self,i):
		return WaveletTree.__access(self.root,i-1)

	def select(self,c,occ_number):
		return WaveletTree.__select(self.root,c,occ_number)

	@staticmethod
	def __build(node,alphabet,string):
	
		N = len(string) 

		if len(alphabet) in range(2):
			# store for frequency
			node.add_bit(''.join('0'for c in string))
			return

		half = math.ceil(len(alphabet) / 2)
		left_alphabet = alphabet[:half]
		right_alphabet = alphabet[half:]

		string_to_bit = []
		[string_to_bit.append('0' if c in left_alphabet else '1') for c in string]
		node.add_bit(''.join(string_to_bit))

		# add for jacobsons rank
		block_size = math.ceil(math.log(N,2))
		num_blocks = math.ceil(N/block_size)


		for i in range(0, N, block_size):
			chunk = string_to_bit[i:i+block_size]
			if not node.rank_chunk_0:
				node.rank_chunk_0.append((sum(1 for b in chunk if b=='0'),len(chunk)))			
			else:
				node.rank_chunk_0.append(((node.rank_chunk_0[-1][0] + sum(1 for b in chunk if b=='0')), node.rank_chunk_0[-1][1] + len(chunk)))

			# Build sub chunk ranks

			sub_block_size = math.ceil(block_size / 2)
			intermediate_list_0 = []
			for j in range(0,len(chunk),sub_block_size):
				block_start = i + j * sub_block_size
				sub_chunk = string_to_bit[block_start:block_start+sub_block_size]
				if not intermediate_list_0:
					intermediate_list_0.append((sum(1 for b in sub_chunk if b=='0'),len(sub_chunk)))
				else:
					s = intermediate_list_0[-1][0] + sum(1 for b in sub_chunk if b=='0')
					intermediate_list_0.append((s,intermediate_list_0[-1][1] + len(sub_chunk)))

			node.rank_sub_chunk_0.append(intermediate_list_0)
		# print(node.alphabet)
		# print(node.rank_chunk_0)
		# print(node.rank_sub_chunk_0)
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
		nx.draw_networkx_edges(G,pos) # draw edges
		nx.draw_networkx_labels(G,pos) # draw node labels
		plt.show()	

	@staticmethod
	def __rank(node, c, i,Jacobsons):
		# Check if we have reachead leaf
		if len(node.alphabet) == 1:
			return i

		c_in_left_child = c in node.left.alphabet

		bit_for_c = '0' if c_in_left_child else '1'

		N = len(node.bit_vector)

		# binary rank calculation
		# count the number of bit until this point
		# try jacobsons rank for faster query times
		if not Jacobsons:
			new_i = WaveletTree.binary_rank(node.bit_vector[:i],bit_for_c)
		else:
			block_size = math.ceil((math.log(N,2)))
			chunk_id = i // block_size
			sub_block_size = math.ceil(block_size / 2)
			#print(chunk_id)
			chunk_id = chunk_id - 1

			# print("HELLO")
			# print(chunk_id)
			if chunk_id > 0:		
				product = (chunk_id+1) * block_size
				remaining = i - product

				#print("Remaining ",remaining)
				sub_block_id = remaining // sub_block_size
				sub_block_id -= 1


				#print(sub_block_id)
				
				# TODO: Make last addition a lookup 

				block_sum = node.rank_chunk_0[chunk_id][0]
				current_block_size = node.rank_chunk_0[chunk_id][1]
				sub_block_sum = node.rank_sub_chunk_0[chunk_id+1][sub_block_id][0]
				current_sub_block_size = node.rank_sub_chunk_0[chunk_id+1][sub_block_id][1]

				# print("WHATS1")
				#print("PLSSS ",node.rank_chunk_0[chunk_id][0],node.rank_chunk_0[chunk_id][1])
				# print(sub_block_sum,sub_block_size)

				if sub_block_id > 0:

					remaining = remaining - sub_block_size * (sub_block_id+1)
					product += sub_block_size * (sub_block_id+1)
					remaining_chunk = node.bit_vector[product:product+remaining]
					
					if c_in_left_child:
						#print("here1")
						new_i = block_sum + sub_block_sum + sum(1 for b in remaining_chunk if b=='0')
					else:
						#print("here2")
						new_i = current_block_size - block_sum + current_sub_block_size - sub_block_sum + sum(1 for b in remaining_chunk if b=='1')
				else:

					remaining_chunk = node.bit_vector[product:product+remaining]

					if c_in_left_child:			
						new_i = block_sum + sum(1 for b in remaining_chunk if b=='0')
					else:
						#print("WRONG ",block_size - block_sum)	
						new_i = current_block_size - block_sum + sum(1 for b in remaining_chunk if b=='1')
			else:
				# in first block	
				#print("geggegeg")
				sub_block_id = i // sub_block_size
				sub_block_id -= 1
				product = 0 
				if sub_block_id > 0:

					product += sub_block_size * (sub_block_id+1)
					remaining = i - product
					remaining_chunk = node.bit_vector[product:product+remaining]
					sub_block_sum = node.rank_sub_chunk_0[0][sub_block_id][0]
					current_sub_block_size = node.rank_sub_chunk_0[0][sub_block_id][1]
					#print(sub_block_sum,sub_block_size)
					if c_in_left_child:
						new_i = sub_block_sum + sum(1 for b in remaining_chunk if b=='0')
					else:
						new_i = current_sub_block_size - sub_block_sum + sum(1 for b in remaining_chunk if b=='1')
				else:
					remaining_chunk = node.bit_vector[:i]
					if c_in_left_child:
						new_i = sum(1 for b in remaining_chunk if b=='0')
					else:
						new_i = sum(1 for b in remaining_chunk if b=='1')


		child = node.left if c_in_left_child else node.right

		#print(new_i)
		return WaveletTree.__rank(child, c, new_i,Jacobsons)

	def binary_rank(bit_vector,bit):
		return sum(1 for b in bit_vector if b==bit)

	@staticmethod
	def __access(node,i):
		if len(node.alphabet) == 1:
			return node.alphabet[0]
		bit = node.bit_vector[i]
		#print(bit)
		if bit == '1':
			child = node.right
			rank = WaveletTree.binary_rank(node.bit_vector[:i],'1')
		else:
			child = node.left
			rank = WaveletTree.binary_rank(node.bit_vector[:i],'0')

		return WaveletTree.__access(child,rank)

	def find_leaf(node,c):
		if len(node.alphabet) == 1:
			return node
		child = node.left if c in node.left.alphabet else node.right

		return WaveletTree.find_leaf(child,c)

	@staticmethod
	def __select(node,c,occ_number):

		leaf = WaveletTree.find_leaf(node,c)
		if leaf.parent:
			bit = '1' if (leaf.parent.right == leaf) else '0'
			return WaveletTree.__select_helper(leaf.parent,bit,occ_number)
		else:
			# means there is only one alphabet
			return occ_number

	# clarks select
	def binary_select(bit_vector,num_occurence,bit):
		count = 0
		for i,b in enumerate(bit_vector):
			#print(i,b)
			if b == bit:
				count += 1
				if count == num_occurence:
					return i+1

	def __select_helper(node,bit,occ_number):

		position = WaveletTree.binary_select(node.bit_vector,occ_number,bit)
		if node.parent is None:
			return position
		else:
			bit = '1' if (node.parent.right == node) else '0'
			return WaveletTree.__select_helper(node.parent,bit,position)




