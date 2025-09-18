import hashlib
import zlib

import pytest

from diffpy.srxconfutils import tools


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file with known content."""
    file_path = tmp_path / "testfile.txt"
    content = b"Hello world!\nThis is a test.\n"
    file_path.write_bytes(content)
    return file_path, content


def test_check_md5(temp_file):
    file_path, content = temp_file
    expected_md5 = hashlib.md5(content).hexdigest()
    result = tools.check_md5(file_path)
    assert result == expected_md5


def test_check_crc32(temp_file):
    """Test the check_crc32 function."""
    file_path, content = temp_file
    val = tools.check_crc32(file_path)
    expected = zlib.crc32(content)
    assert val == expected
