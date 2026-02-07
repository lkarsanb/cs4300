from src import task5

def test_list():
    """ Tests if list slicing returned correct values and only 3 items. """
    my_list = task5.first_three(task5.books_list)
    assert my_list == [("The Great Gatsby", "F. Scott Fitzgerald"), 
                ("The Book Thief", "Markus Zusak"), 
                ("To Kill a Mockingbird", "Harper Lee")]
    assert isinstance(my_list, list)
    assert len(my_list) == 3
    assert my_list[0][1] == "F. Scott Fitzgerald"
    assert my_list[2][0] == "To Kill a Mockingbird"


def test_dictionary():
    """ Tests if dictionary was created and if values can be accessed. """
    my_dict = task5.students
    assert isinstance(my_dict, dict)
    assert len(my_dict) == 4
    assert my_dict["Peter Parker"] == 2222
    assert "Tony Stark" in my_dict
    assert "b" not in my_dict
