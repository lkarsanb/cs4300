def first_three(my_list):
    return my_list[:3]


books_list = [("The Great Gatsby", "F. Scott Fitzgerald"), 
                ("The Book Thief", "Markus Zusak"), 
                ("To Kill a Mockingbird", "Harper Lee"),
                ("The Alchemist", "Paulo Coelho")]

# Print out the first 3 books in the list using list slicing.
print(first_three(books_list))


# Create a dictionary with student names and ids.
students = {"Tony Stark": 1111,
            "Peter Parker": 2222,
            "Steve Rogers": 3333,
            "Scott Lang": 4444}

print(students)