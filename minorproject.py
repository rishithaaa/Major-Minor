# Auxiliary function (a): What is the length of the string?
def get_length(string):
    return len(string)

# Auxiliary function (b): Is a specified character in the string?
def contains_char(string, char):
    return char in string

# Auxiliary function (c): What character is at a specific location in the string?
def char_at_location(string, location):
    return string[location]

# Auxiliary function (d): What is the location in the string of a specific character?
def location_of_char(string, char):
    return string.index(char)

# Auxiliary function (e): How many of a specific character are in the string?
def count_char_occurrences(string, char):
    return string.count(char)

# Auxiliary function (f): How can a string be split into smaller sub-strings?
def split_string(string, separator):
    return string.split(separator)

# Main function for email validation
def ValidateEmail(TestString):
    # Rule 1: Is the character '@' in the string?
    if not contains_char(TestString, '@'):
        return "INVALID -- No '@' symbol found"

    # Rule 2: If '@' is in the string, check if there is only one '@'?
    if count_char_occurrences(TestString, '@') != 1:
        return "INVALID -- More than one '@' symbol found"

    # Rule 3: Check that '@' is not the first character or in a position less than 6 from the end
    index_of_at = location_of_char(TestString, '@')
    if index_of_at == 0 or (get_length(TestString) - index_of_at) <= 6:
        return "INVALID -- '@' is in an invalid position"

    # Additional rules can be added here...

    # If no invalid conditions are met, the email is considered valid
    return "VALID -- " + TestString

# Example usage in an interactive mode
user_input = input("Enter an email address: ")
result = ValidateEmail(user_input)
print(result)
