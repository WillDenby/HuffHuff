# HuffHuff

**A Huffman encoder/decoder script for compressing non-binary files.**

**USAGE**

Compression: `python huffman.py encode UncompressedPath CompressedPath`

Expansion: `python huffman.py decode CompressedPath DecompressedPath`

There is a dependency on [bitarray](https://pypi.org/project/bitarray/)

Tests can be run with `pytest`. And `/sample_files` provides a sample text file, with a compressed and subsequently re-expanded version. 

**BACKGROUND**

This is my solution to the third of John Crickett's [Coding Challenges](https://codingchallenges.fyi/challenges/challenge-huffman)

The trickiest bit was building the Huffman Tree. [This](https://opendsa-server.cs.vt.edu/ODSA/Books/CS3/html/Huffman.html) was a great resource.
