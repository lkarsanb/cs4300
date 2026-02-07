from src import task6
import os, pytest

def test_count_words():
    """ Check correct value is returned from reading the file. """
    # There are 104 words, 12 periods, and 11 commas.
    my_path = "/home/student/cs4300/homework1/task6_read_me.txt"
    assert task6.count_words(my_path) == 104 + 12 + 11


def test_count_words_no_punct():
    """ Check correct value is returned from reading the file, not including punctuation. """
    my_path = "/home/student/cs4300/homework1/task6_read_me.txt"
    assert task6.count_words_no_punct(my_path) == 104

def test_invalid_path():
    """ Check if invalid path entered and check if path is not for a file. """
    # Path does not give a file.
    my_path = "/home/student/cs4300/homework1/task6_read_me.txt/src"
    with pytest.raises(FileNotFoundError):
        task6.count_words(my_path)

    # Check for count_words_no_punct too.
    with pytest.raises(FileNotFoundError):
        task6.count_words_no_punct(my_path)

    # Invalid path.
    my_path = "/home/student/cs4300/homework1/task10000_read_me.txt"
    with pytest.raises(FileNotFoundError):
        task6.count_words(my_path)

    # Check for count_words_no_punct too.
    with pytest.raises(FileNotFoundError):
        task6.count_words_no_punct(my_path)

