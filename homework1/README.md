# Homework 1

## Overview of Project
In this project, I was able to interact with Python and write tests for each file I created. This project explores basic Python syntax, datatypes, and control structures as well as more advanced topics such as implementing an algorihtm, using file handing, and implementing tests to check the code.

### Project Structure
```text
.
├── bar_chart.jpg
└── homework1
    ├── README.md
    ├── bar_chart.jpg
    ├── src
    │   ├── __init__.py
    │   ├── __pycache__
    │   ├── task1.py
    │   ├── task2.py
    │   ├── task3.py
    │   ├── task4.py
    │   ├── task5.py
    │   ├── task6.py
    │   └── task7.py
    ├── task6_read_me.txt
    └── tests
        ├── __init__.py
        ├── __pycache__
        ├── test_task1.py
        ├── test_task2.py
        ├── test_task3.py
        ├── test_task4.py
        ├── test_task5.py
        ├── test_task6.py
        └── test_task7.py

6 directories, 21 files
```

## How to Run
#### 1) Open a terminal and create a virtual environment.
```
python3 -m <name_of_virtual_environment> --system-site-packages
source <name_of_virtual_environment>/bin/activate
```
* Note: The project contains absolute paths in task6.py, task7.py, test_task6.py, and test_task7.py so these instructions are best suited for an environment in DevEdu.

#### 2) Install pytest, pandas, and matplotlib.
```
python3 -m pip install pytest, pandas, matplotlib
```

#### 3) Clone the repository to /home/student
```
cd /home/student
git clone git@github.com:lkarsanb/cs4300.git 
```
Now, you should see a directory /home/student/cs4300.

#### 4) cd into the new directory.
```
cd cs4300
```

#### 5) From here, you can run a certain python file. If you would like to run the tests, skip to step 6.
```
cd homework1/src
python3 <name_of_python_file>
```

#### 6) To run all tests, use the following command.
```
pytest
```
* Note: If you would like to see more information about the tests, use the -v option.

#### 7) To run some tests, use the following commands from the homework1 directory (to get to homework1 directory, use cd /home/student/cs4300/homework1.
```
pytest tests/<python_test_file>
```

