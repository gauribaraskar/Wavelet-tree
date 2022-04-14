'''
    WaveletNode class represents one node in Wavelet tree data structure.
'''
class WaveletTreeNode:

    def __init__(self, alphabet, parent=None):
        self.bit_vector = ''
        self.alphabet = alphabet
        self.left = None
        self.right = None
        self.parent = parent

    def add_bit(self,bit):
        self.bit_vector += bit
