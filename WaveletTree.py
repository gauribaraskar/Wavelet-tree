from WaveletTreeNode import WaveletTreeNode
import networkx as nx
import pydot
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt
import math
import time
from bisect import bisect_left


class WaveletTree:
	def __init__(self):
		self.root = None

	def build(self,string,alphabet):
		self.root = WaveletTreeNode(alphabet)
		#print(string)
		self.__build(self.root,alphabet,string)
	
	def rank(self, c, i,Jacobsons=False):
		if c not in self.root.alphabet:
			return -1
		if i > len(self.root.bit_vector):
			return -1
		return WaveletTree.__rank(self.root, c, i,Jacobsons)

	def access(self,i):
		if i > len(self.root.bit_vector):
			return -1
		return WaveletTree.__access(self.root,i-1)

	def select(self,c,occ_number,Optimized=False):
		if c not in self.root.alphabet:
			return -1
		return WaveletTree.__select(self.root,c,occ_number,Optimized)

	@staticmethod
	def __build(node,alphabet,string):

		#print(string)
	
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

		#print(node.bit_vector)

		# add for jacobsons rank
		block_size = math.ceil(math.log(N,2))
		num_blocks = math.ceil(N/block_size)

		#print(N,block_size,num_blocks)
		for i in range(0, N, block_size):
			chunk = string_to_bit[i:i+block_size]
			if not node.rank_chunk_0:
				node.rank_chunk_0.append((sum(1 for b in chunk if b=='0'),len(chunk)))			
			else:
				node.rank_chunk_0.append(((node.rank_chunk_0[-1][0] + sum(1 for b in chunk if b=='0')), node.rank_chunk_0[-1][1] + len(chunk)))

			# Build sub chunk ranks

			sub_block_size = math.ceil(block_size / 2)
			intermediate_list_0 = []
			#print(len(chunk))
			for j in range(0,len(chunk),sub_block_size):
				sub_block_start = i + j
				end_index = sub_block_start + sub_block_size
				#print("POOOOOOOO ",i,j,sub_block_start,end_index)
				if end_index  > i + block_size:
					end_index = i + block_size
				sub_chunk = node.bit_vector[sub_block_start:end_index]
				#print(sub_chunk)
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

		if not Jacobsons:
			new_i = WaveletTree.binary_rank(node.bit_vector[:i],bit_for_c)
		else:

			block_size = math.ceil((math.log(N,2)))
			sub_block_size = math.ceil(block_size / 2)

			if c_in_left_child:

				chunk_id = i // block_size
				#chunk_id -= 1

				if chunk_id==0:
					# search in sub blocks
					rank_sub_chunk_0 = node.rank_sub_chunk_0[0]
					sub_chunk_id = i // sub_block_size

					if sub_chunk_id == 0:

						#current_sub_block_size = rank_sub_chunk_0[0][1]
						bit_vector = node.bit_vector[0:i]
						current_rank = WaveletTree.binary_rank(bit_vector,bit_for_c)
						new_i = current_rank

					else:

						current_rank = rank_sub_chunk_0[sub_chunk_id-1][0]
						remaining = i - rank_sub_chunk_0[sub_chunk_id-1][1]

						start = rank_sub_chunk_0[sub_chunk_id-1][1]
						#end = rank_sub_chunk_0[sub_chunk_id][1]
						next_sub_chunk_bit_vector = node.bit_vector[start:start+remaining]

						current_rank += WaveletTree.binary_rank(next_sub_chunk_bit_vector,bit_for_c)
						new_i = current_rank
				else:

					current_rank = node.rank_chunk_0[chunk_id-1][0]
					remaining = i - node.rank_chunk_0[chunk_id-1][1]
					# search in sub chunks
					rank_sub_chunk_0 = node.rank_sub_chunk_0[chunk_id]
					sub_chunk_id = remaining // sub_block_size

					if sub_chunk_id == 0:

						start = node.rank_chunk_0[chunk_id-1][1]

						#current_sub_block_size = rank_sub_chunk_0[sub_chunk_id][1]
						bit_vector = node.bit_vector[start:start + remaining]
						current_rank += WaveletTree.binary_rank(bit_vector,bit_for_c)
						new_i = current_rank

					else:
						current_rank += rank_sub_chunk_0[sub_chunk_id-1][0]
						remaining -= rank_sub_chunk_0[sub_chunk_id-1][1]
						start = node.rank_chunk_0[chunk_id-1][1] + rank_sub_chunk_0[sub_chunk_id-1][1]
						#end = rank_sub_chunk_0[sub_chunk_id][1]
						next_sub_chunk_bit_vector = node.bit_vector[start:start+remaining]

						current_rank += WaveletTree.binary_rank(next_sub_chunk_bit_vector,bit_for_c)
						new_i =  current_rank
			else:
				chunk_id = i // block_size
				#chunk_id -= 1
				if chunk_id==0:
					# search in sub blocks
					rank_sub_chunk_1 = [(x[1]-x[0],x[1]) for x in node.rank_sub_chunk_0[0]]
					sub_chunk_id = i // sub_block_size
					if sub_chunk_id == 0:

						current_sub_block_size = rank_sub_chunk_1[sub_chunk_id][1]
						bit_vector = node.bit_vector[0:i]
						current_rank = WaveletTree.binary_rank(bit_vector,bit_for_c)
						new_i =  current_rank

					else:

						current_rank = rank_sub_chunk_1[sub_chunk_id-1][0]
						remaining = i - rank_sub_chunk_1[sub_chunk_id-1][1]

						start = rank_sub_chunk_1[sub_chunk_id-1][1]
						#end = rank_sub_chunk_0[sub_chunk_id][1]
						next_sub_chunk_bit_vector = node.bit_vector[start:start+remaining]

						current_rank += WaveletTree.binary_rank(next_sub_chunk_bit_vector,bit_for_c)
						new_i =  current_rank
				else:

					rank_chunk_1 = [(x[1]-x[0],x[1]) for x in node.rank_chunk_0]

					current_rank = rank_chunk_1[chunk_id-1][0]
					remaining = i - rank_chunk_1[chunk_id-1][1]
					# search in sub chunks
					rank_sub_chunk_1 = [(x[1]-x[0],x[1]) for x in node.rank_sub_chunk_0[chunk_id]]
					sub_chunk_id = remaining // sub_block_size
					if sub_chunk_id == 0:

						#current_sub_block_size = rank_sub_chunk_1[sub_chunk_id][1]
						start = rank_chunk_1[chunk_id-1][1]
						bit_vector = node.bit_vector[start:start + remaining]
						current_rank += WaveletTree.binary_rank(bit_vector,bit_for_c)
						new_i =  current_rank

					else:

						current_rank += rank_sub_chunk_1[sub_chunk_id-1][0]
						remaining -= rank_sub_chunk_1[sub_chunk_id-1][1]
						start =  rank_chunk_1[chunk_id-1][1] + rank_sub_chunk_1[sub_chunk_id-1][1]
						#end = rank_sub_chunk_1[sub_chunk_id][1]
						next_sub_chunk_bit_vector = node.bit_vector[start:start+remaining]

						current_rank += WaveletTree.binary_rank(next_sub_chunk_bit_vector,bit_for_c)
						new_i =  current_rank

		child = node.left if c_in_left_child else node.right

		return WaveletTree.__rank(child, c, new_i,Jacobsons)

	def binary_rank(bit_vector,bit):
		return sum(1 for b in bit_vector if b==bit)

	@staticmethod
	def __access(node,i):
		if len(node.alphabet) == 1:
			return node.alphabet[0]
		bit = node.bit_vector[i]
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
	def __select(node,c,occ_number,Optimized):

		leaf = WaveletTree.find_leaf(node,c)
		if leaf.parent:
			bit = '1' if (leaf.parent.right == leaf) else '0'
			return WaveletTree.__select_helper(leaf.parent,bit,occ_number,Optimized)
		else:
			# means there is only one alphabet
			return occ_number

	# clarks select


	def counting_bit_in_vector(bit_vector,num_occurence,bit):
		count = 0
		for i,b in enumerate(bit_vector):
			if b == bit:
				count += 1
				if count == num_occurence:
					return i+1
		return -1
	def binary_select(node,num_occurence,bit,Optimized):

		if Optimized:

			if bit == '0':
				number_of_0_found = 0
				block_no = bisect_left(node.rank_chunk_0,(num_occurence,))
				if block_no == 0:
					remaining_0 = num_occurence
					# binary search on the sub blocks of 0th list
					sub_block_no = bisect_left(node.rank_sub_chunk_0[0],(remaining_0,))
					if sub_block_no == 0:
						sub_block_size = node.rank_sub_chunk_0[0][0][1]
						position = WaveletTree.counting_bit_in_vector(node.bit_vector[0:sub_block_size],remaining_0,bit)
						return position
					else:
						remaining_0 = num_occurence - node.rank_sub_chunk_0[0][sub_block_no-1][0]
						position = node.rank_sub_chunk_0[0][sub_block_no-1][1]
						end = node.rank_sub_chunk_0[0][sub_block_no][1]
						position += WaveletTree.counting_bit_in_vector(node.bit_vector[position:end],remaining_0,bit)
						return position
				else:
					#number_of_0_found = node.rank_chunk_0[block_no-1][0]
					position = node.rank_chunk_0[block_no-1][1]
					
					remaining_0 = num_occurence - node.rank_chunk_0[block_no-1][0]
					if block_no == len(node.rank_chunk_0):
						return -1
					else:
						sub_block_no = bisect_left(node.rank_sub_chunk_0[block_no],(remaining_0,))
						if sub_block_no == 0:
							sub_block_size = node.rank_sub_chunk_0[block_no][0][1]
							position += WaveletTree.counting_bit_in_vector(node.bit_vector[position:position+sub_block_size],remaining_0,bit)
							return position
						else:
							sub_block_size = node.rank_sub_chunk_0[block_no][sub_block_no][1] - node.rank_sub_chunk_0[block_no][sub_block_no-1][1]
							remaining_0 -= node.rank_sub_chunk_0[block_no][sub_block_no-1][0]
							position += node.rank_sub_chunk_0[block_no][sub_block_no-1][1]
							end = position + sub_block_size
							position += WaveletTree.counting_bit_in_vector(node.bit_vector[position:end],remaining_0,bit)
							return position
			else:
				number_of_1_found = 0
				rank_chunk_1 = [(x[1]-x[0],x[1]) for x in node.rank_chunk_0]
				block_no = bisect_left(rank_chunk_1,(num_occurence,))
				if block_no == 0:
					remaining_1 = num_occurence
					# binary search on the sub blocks of 0th list
					rank_sub_chunk_1 = [(x[1]-x[0],x[1]) for x in node.rank_sub_chunk_0[block_no]]
					sub_block_no = bisect_left(rank_sub_chunk_1,(num_occurence,))
					if sub_block_no == 0:
						sub_block_size = rank_sub_chunk_1[0][1]
						position = WaveletTree.counting_bit_in_vector(node.bit_vector[0:sub_block_size],remaining_1,bit)
						return position
					else:
						remaining_1 = num_occurence - rank_sub_chunk_1[sub_block_no-1][0]
						position = rank_sub_chunk_1[sub_block_no-1][1]
						end = rank_sub_chunk_1[sub_block_no][1]
						position += WaveletTree.counting_bit_in_vector(node.bit_vector[position:end+1],remaining_1,bit)
						return position
				else:
					if block_no == len(node.rank_chunk_0):
						return -1
					rank_sub_chunk_1 = [(x[1]-x[0],x[1]) for x in node.rank_sub_chunk_0[block_no]]
					#number_of_0_found = node.rank_chunk_0[block_no-1][0]
					remaining_1 = num_occurence - rank_chunk_1[block_no-1][0]
					if block_no == len(rank_chunk_1):
						return -1
					else:
						sub_block_no = bisect_left(rank_sub_chunk_1,(remaining_1,))
						position = node.rank_chunk_0[block_no-1][1]
						if sub_block_no == 0:
							sub_block_size = rank_sub_chunk_1[0][1]
							position += WaveletTree.counting_bit_in_vector(node.bit_vector[position:position+sub_block_size],remaining_1,bit)
							return position
						else:
							sub_block_size = rank_sub_chunk_1[sub_block_no][1] - rank_sub_chunk_1[sub_block_no-1][1]
							remaining_1 -= rank_sub_chunk_1[sub_block_no-1][0]
							position += rank_sub_chunk_1[sub_block_no-1][1]
							end = position + sub_block_size
							position += WaveletTree.counting_bit_in_vector(node.bit_vector[position:end],remaining_1,bit)
							return position
		else:
			count = 0
			for i,b in enumerate(node.bit_vector):
				if b == bit:
					count += 1
					if count == num_occurence:
						return i+1
			return -1

	def __select_helper(node,bit,occ_number,Optimized):

		position = WaveletTree.binary_select(node,occ_number,bit,Optimized)
		if node.parent is None or position == -1:
			return position
		else:
			bit = '1' if (node.parent.right == node) else '0'
			return WaveletTree.__select_helper(node.parent,bit,position,Optimized)




