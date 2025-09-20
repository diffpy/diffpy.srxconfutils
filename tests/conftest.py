import pytest


@pytest.fixture
def temp_file(tmp_path):
    """Create a temporary file with known content."""
    file_path = tmp_path / "testfile.txt"
    content = b"Hello world!\nThis is a test.\n"
    file_path.write_bytes(content)
    return file_path, content
