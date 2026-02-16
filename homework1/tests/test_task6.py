from src import task6
import os, pytest

@pytest.mark.parametrize("full_path", ["/home/student/cs4300/homework1/task6_read_me.txt"])
class TestWordCount:
    def test_count_words(self, full_path):
        """ Check correct value is returned from reading the file. """
        # There are 104 words, 12 periods, and 11 commas.
        assert task6.count_words(full_path) == 104 + 12 + 11


    def test_count_words_no_punct(self, full_path):
        """ Check correct value is returned from reading the file, not including punctuation. """
        assert task6.count_words_no_punct(full_path) == 104

    @pytest.mark.parametrize("bad_path", ["/home/student/cs4300/homework1/task6_read_me.txt/src", "/home/student/cs4300/homework1/task10000_read_me.txt"])
    def test_invalid_path(self, full_path, bad_path):
        """ Check if invalid path entered and check if path is not for a file. """
        # Check invalid path and path does not give a file for count_words().
        with pytest.raises(FileNotFoundError):
            task6.count_words(bad_path)

        # Check invalid path and path does not give a file for count_words_no_punct().
        with pytest.raises(FileNotFoundError):
            task6.count_words_no_punct(bad_path)
