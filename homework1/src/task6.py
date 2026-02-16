import re, os

def count_words(file):
    """ Given an input file, return the number of words in the file, including punctuation."""
    # Check if file exists and is a file.
    curr_loc = os.path.dirname(__file__)
    full_path = os.path.join(curr_loc, "../", file)
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise FileNotFoundError(f"No such file exists.")

    count = 0
    # Open the file and count number of words per line (including punctuation).
    with open(full_path, 'r') as f:
        for line in f:
            line = line.split()
            count += len(line)

    return count

def count_words_no_punct(file):
    """ Given an input file, return the number of words in the file, not including punctuation. """
    # Check if file exists and is a file.
    curr_loc = os.path.dirname(__file__)
    full_path = os.path.join(curr_loc, "../", file)
    if not os.path.exists(full_path) or not os.path.isfile(full_path):
        raise FileNotFoundError(f"No such file exists.")

    with open(full_path, 'r') as f:
        words = f.read()
    
    # Use a Regex to find only items with letters.
    pattern = r"\w+" 
    count = len(re.findall(pattern, words))

    return count