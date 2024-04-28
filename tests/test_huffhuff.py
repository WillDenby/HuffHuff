import os
import tempfile
import pytest
from huffhuff.main import encode, decode  # Adjust import according to your project structure.

@pytest.fixture
def sample_text():
    return "this is an example for huffman encoding"

@pytest.fixture
def binary_content():
    return bytes([0, 1, 2, 3, 255, 254, 253, 252])

@pytest.fixture
def create_temp_file():
    """Utility function to create a temp file with content and return its path."""
    def _create_temp_file(content):
        temp_fd, temp_path = tempfile.mkstemp()
        with os.fdopen(temp_fd, 'wb') as tmp:
            tmp.write(content)
        return temp_path
    return _create_temp_file

def test_encode_decode_simple_text(create_temp_file, sample_text):
    input_path = create_temp_file(sample_text.encode('utf-8'))
    encoded_path = create_temp_file(b'')
    decoded_path = create_temp_file(b'')

    encode(input_path, encoded_path)
    decode(encoded_path, decoded_path)

    with open(decoded_path, 'rb') as file:
        output = file.read()

    assert output.decode('utf-8') == sample_text

def test_empty_file(create_temp_file):
    input_path = create_temp_file(b'')
    encoded_path = create_temp_file(b'')
    decoded_path = create_temp_file(b'')

    encode(input_path, encoded_path)
    decode(encoded_path, decoded_path)

    with open(decoded_path, 'rb') as file:
        output = file.read()

    assert output == b''

def test_error_handling_nonexistent_file():
    with pytest.raises(FileNotFoundError):
        encode('/nonexistent/path/to/input.txt', '/nonexistent/path/to/output.encoded')

@pytest.mark.parametrize("text", ["a", "abc" * 1000, "👋🌍" * 100, "\n\t"])
def test_various_texts(create_temp_file, text):
    input_path = create_temp_file(text.encode('utf-8'))
    encoded_path = create_temp_file(b'')
    decoded_path = create_temp_file(b'')

    encode(input_path, encoded_path)
    decode(encoded_path, decoded_path)

    with open(decoded_path, 'rb') as file:
        output = file.read()

    assert output.decode('utf-8') == text
