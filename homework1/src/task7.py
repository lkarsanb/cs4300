# Chosen package: pandas and matplotlib
import pandas as pd
import matplotlib.pyplot as plt

# Create data
students = {
    "student": ["Tony", "Peter", "Steve", "Scott"],
    "id": [1111, 2222, 3333, 4444],
    "grade": [100, 95, 90, 85]}

# Display data as table
table = pd.DataFrame(students)
print(table)

# Return values from index 0 of table.
print("\nIndex 0:")
print(table.loc[0])

# Print information about the data in the table.
print("\nInfo about data in table:")
print(table.info())

# Display the student and their grade in a bar chart.
plt.bar(table["student"], table["grade"])
plt.title("Student Grades")
plt.xlabel("Students")
plt.ylabel("Grades (percentage)")
plt.savefig("/home/student/cs4300/homework1/bar_chart.jpg")