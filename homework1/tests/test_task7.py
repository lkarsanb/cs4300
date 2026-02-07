import os
from src import task7

def test_check_data():
    """ Test if the data entered is correct and the structure of the data frame is correct. """
    assert len(task7.students) == 3
    assert task7.table.loc[0].student == "Tony"
    assert task7.table.shape == (4, 3)
    assert list(task7.table) == ["student", "id", "grade"]


def test_chart_generated():
    """ Test if the file was the chart was created. """
    assert os.path.exists("/home/student/cs4300/homework1/bar_chart.jpg")