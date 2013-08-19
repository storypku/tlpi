from collections import defaultdict
from priority_queue import HeapPriorityQueue
from linked_binary_tree import LinkedBinaryTree

class HuffmanCoding:
    """A Huffman coding system."""

    def __init__(self, text):
        self.text = text
        self._ht_tree = self._compose_ht_tree(text)
        self.codes = self.encodings()

    def _compute_chr_freq(self, text):
        """Compute the frequency of each character in text.

        Return a a (freq, character) generator.
        """
        freqdict = defaultdict(int)
        for lett in text:
            freqdict[lett] += 1
        for lett, freq in freqdict.items():
            yield (freq, lett)

    def _compose_ht_tree(self, text):
        """Huffman tree construction for text."""
        freq_table = self._compute_chr_freq(text)
        ht_queue = HeapPriorityQueue()
        for freq, lett in freq_table:
            ht_tree = LinkedBinaryTree()
            ht_tree._add_root((freq, lett))
            ht_queue.add(freq, ht_tree)

        while len(ht_queue) > 1:
            (freq1, subtree1) = ht_queue.remove_min()
            (freq2, subtree2) = ht_queue.remove_min()
            freq = freq1 + freq2
            ht_tree = LinkedBinaryTree()
            ht_tree._add_root((freq, None))
            ht_tree._attach(ht_tree.root(), subtree1, subtree2)
            ht_queue.add(freq, ht_tree)
        _, ht_tree = ht_queue.remove_min()
        return ht_tree

    def encodings(self):
        """Return character -> pseudo-bits mappings."""
        codes = {}
        ht_tree = self._ht_tree
        for pos in ht_tree.positions():
            if ht_tree.is_leaf(pos):
                ht_code = []
                walk = pos
                parent = ht_tree.parent(walk)
                while parent is not None:
                    if ht_tree.left(parent) == walk:
                        ht_code.append("0")
                    else:
                        ht_code.append("1")
                    walk = parent
                    parent = ht_tree.parent(walk)
                character = pos.element()[1]
                codes[character] = "".join(reversed(ht_code))
        return codes

    def encode(self):
        """Encode text into bits stream."""
        return "".join(self.codes[lett] for lett in self.text)

    def _decode_binary(self, bitstream):
        """Helper method to return the decoded text for bitstream, or raise
        ValueError if bitstream corrupted."""
        ht_tree = self._ht_tree
        text = []
        pos = ht_tree.root()
        for bit in bitstream:
            if bit == "0":
                pos = ht_tree.left(pos)
            else:
                pos = ht_tree.right(pos)
            if ht_tree.is_leaf(pos):
                text.append(pos.element()[1])
                pos = ht_tree.root()
        if ht_tree.is_root(pos):
            return text
        else:
            raise ValueError("Binary stream invalid")

    def decode(self, bitstream):
        """Decode pseudo-bitstream into text. Raise ValueError if bitstream
        corrupted."""
        return "".join(self._decode_binary(bitstream))

if __name__ == "__main__":
    from pprint import pprint
    with open("huffman_text.txt") as f:
        text_ = f.read()
    huffman = HuffmanCoding(text_)
    pprint(huffman.codes)
    bitstream_ = huffman.encode()
    print (bitstream_)
    print (huffman.decode(bitstream_))
