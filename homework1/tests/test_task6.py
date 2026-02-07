from src import task6
import os, pytest

def test_count_words():
    """ Check correct value is returned from reading the file. """
    # There are 104 words, 12 periods, and 11 commas.
    full_path = os.path.join(".", 'src/task6_read_me.txt')
    assert task6.count_words(full_path) == 104 + 12 + 11


def test_count_words_no_punct():
    """ Check correct value is returned from reading the file, not including punctuation. """
    full_path = os.path.join(".", 'src/task6_read_me.txt')
    assert task6.count_words_no_punct(full_path) == 104

def test_invalid_path():
    """ Check if invalid path entered and check if path is not for a file. """
    # Path does not give a file.
    full_path = os.path.join(".", 'src/')
    with pytest.raises(FileNotFoundError):
        task6.count_words(full_path)

    # Check for count_words_no_punct too.
    with pytest.raises(FileNotFoundError):
        task6.count_words_no_punct(full_path)

    # Invalid path.
    full_path = os.path.join(".", 'src/task1000_read_me.txt')
    with pytest.raises(FileNotFoundError):
        task6.count_words(full_path)

    # Check for count_words_no_punct too.
    with pytest.raises(FileNotFoundError):
        task6.count_words_no_punct(full_path)

