import sys
import heapq
from collections import Counter
import pickle
from bitarray import bitarray

class HuffmanNode:
    def __init__(self, character=None, freq=0, left=None, right=None):
        self.character = character
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def generate_codes(node, code="", huffman_codes=None):
    if huffman_codes is None:
        huffman_codes = {}
    if node is not None:
        if node.character is not None:
            huffman_codes[node.character] = code if code else "0"
        generate_codes(node.left, code + "0", huffman_codes)
        generate_codes(node.right, code + "1", huffman_codes)
    return huffman_codes

def encode(input_file_name, output_file_name):
    with open(input_file_name, 'r', encoding='utf-8') as file:
        text = file.read()

    if not text:
        with open(output_file_name, 'wb') as out_file:
            out_file.write(b'')
        return

    frequency = Counter(text)
    priority_queue = [HuffmanNode(ch, freq) for ch, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, left.freq + right.freq, left, right)
        heapq.heappush(priority_queue, merged)

    root = priority_queue[0]
    huffman_codes = generate_codes(root)

    encoded_text = bitarray()
    encoded_text.encode({char: bitarray(code) for char, code in huffman_codes.items()}, text)

    with open(output_file_name, 'wb') as file:
        pickle.dump((huffman_codes, len(encoded_text), encoded_text), file)

def decode(input_file_name, output_file_name):
    with open(input_file_name, 'rb') as file:
        try:
            huffman_codes, bit_length, encoded_text = pickle.load(file)
        except EOFError:
            with open(output_file_name, 'wb') as out_file:
                out_file.write(b'')
            return

    reverse_codes = {v: k for k, v in huffman_codes.items()}
    decoded_text = ""

    current_bits = bitarray()
    for bit in encoded_text:
        current_bits.append(bit)
        if current_bits.to01() in reverse_codes:
            decoded_text += reverse_codes[current_bits.to01()]
            current_bits.clear()

    with open(output_file_name, 'w', encoding='utf-8') as file:
        file.write(decoded_text)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Please provide the following arguments `encode/decode` `inputPath` `outputPath`.")
        sys.exit()

    mode, input_file_name, output_file_name = sys.argv[1:4]

    if mode.lower() == 'encode':
        encode(input_file_name, output_file_name)
    elif mode.lower() == 'decode':
        decode(input_file_name, output_file_name)
    else:
        print("Invalid mode. Please choose 'encode' or 'decode'.")
