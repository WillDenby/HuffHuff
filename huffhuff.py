"""A Huffman encoder/decoder script for compressing non-binary files.

Compression: python huffman.py encode UncompressedPath CompressedPath
Expansion: python huffman.py decode CompressedPath DecompressedPath

Dependencies: bitarray
"""

# Standard library imports
import sys
import heapq
import pickle
from typing import Optional
from collections import Counter

# Third party imports
from bitarray import bitarray


class HuffmanNode:
    """A class for representing a node in the Huffman tree.

    Attributes:
        character: The character this node represents.
        freq: The frequency of the character.
        left: The left child node.
        right: The right child node.
    """

    def __init__(
        self,
        character: Optional[str] = None,
        freq: int = 0,
        left: Optional["HuffmanNode"] = None,
        right: Optional["HuffmanNode"] = None,
    ):
        self.character = character
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "HuffmanNode") -> bool:
        """Less-than comparison method for heap ordering.

        Args:
            other: Another node to compare.

        Returns:
            True if this node's frequency is less than the other node's frequency.
        """
        return self.freq < other.freq


def generate_codes(
    node: Optional[HuffmanNode],
    code: str = "",
    huffman_codes: Optional[dict[str, str]] = None,
) -> dict[str, str]:
    """Generates Huffman codes for each character based on the given Huffman tree.

    Args:
        node: The root node of the Huffman tree.
        code: The current Huffman code string.
        huffman_codes: Storage for the Huffman codes.

    Returns:
        The Huffman codes for each character.
    """
    if huffman_codes is None:
        huffman_codes = {}
    if node is not None:
        if node.character is not None:
            huffman_codes[node.character] = code if code else "0"
        generate_codes(node.left, code + "0", huffman_codes)
        generate_codes(node.right, code + "1", huffman_codes)
    return huffman_codes


def encode(input_file_name: str, output_file_name: str) -> None:
    """Encodes the input file and writes to the named output.

    Args:
        input_file_name: The path of the input file.
        output_file_name: The path of the output (encoded) file.
    """
    with open(input_file_name, "r", encoding="utf-8") as file:
        text = file.read()

    if not text:
        with open(output_file_name, "wb") as out_file:
            out_file.write(b"")
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
    encoded_text.encode(
        {char: bitarray(code) for char, code in huffman_codes.items()}, text
    )

    with open(output_file_name, "wb") as file:
        pickle.dump((huffman_codes, len(encoded_text), encoded_text), file)


def decode(input_file_name: str, output_file_name: str) -> None:
    """Decodes an encoded input file and writes to the named output

    Args:
        input_file_name: The path of the input (encoded) file.
        output_file_name: The path of the output file.
    """
    with open(input_file_name, "rb") as file:
        try:
            huffman_codes, bit_length, encoded_text = pickle.load(file)
        except EOFError:
            with open(output_file_name, "wb") as out_file:
                out_file.write(b"")
            return

    reverse_codes = {v: k for k, v in huffman_codes.items()}
    decoded_text = ""

    current_bits = bitarray()
    for bit in encoded_text:
        current_bits.append(bit)
        if current_bits.to01() in reverse_codes:
            decoded_text += reverse_codes[current_bits.to01()]
            current_bits.clear()

    with open(output_file_name, "w", encoding="utf-8") as file:
        file.write(decoded_text)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            "Please provide the following arguments `encode/decode` `inputPath` `outputPath`."
        )
        sys.exit()

    mode, input_file_name, output_file_name = sys.argv[1:4]

    if mode.lower() == "encode":
        encode(input_file_name, output_file_name)
    elif mode.lower() == "decode":
        decode(input_file_name, output_file_name)
    else:
        print("Invalid mode. Please choose 'encode' or 'decode'.")
