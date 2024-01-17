# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification
import numpy as np


def isFloat(number, exception_message):
    """
    This function tests if a number is a float
    if it is not a float an exception is raised with a custom message

    Parameters:
        number (float, int or string) : The number to be tested is either a float, int or a string
        exception_message (string) : A custom exception message that is displayed if the test fails
    """

    # This if statement is true if the number is not a float or integer
    if type(number) != float and type(number) != int:
        # A value error exception is raised and the custom message is shown
        raise ValueError(exception_message)


def sumvalues(values):
    """
    A function that sums the values in a list

    Parameters:
        values (list) : A list of rational values

    Returns:
        int : the sum of the values in the list
    """

    # The sum of the values is instantiated at 0
    valueSum = 0

    # The for loop iterates through the elements in values summing them
    for i in values:
        # A test is made to see if you are trying to sum a non number
        isFloat(i, "Tried to sum a list with a non number in")
        valueSum += i
    # The sum of the values is returned
    return valueSum


def maxvalue(values):
    """
    A function that find the index of the max value in a list

    Parameters:
        values (list) : A list of rational values

    Returns:
        int : the index of the max value in the list
    """

    # The max value and max index are originally 0
    maxValue = 0
    maxindex = 0

    # A for loop iterates through the elements in values
    for i in range(len(values)):
        # A test is made to ensure that the list contains only rational numbers
        isFloat(values[i], "Tried to find the max of list with a non number")
        # If a new max value is found the index and max value are updated
        if values[i] > maxValue:
            maxindex = i
            maxValue = values[i]
    # Finally the max index is returned
    return maxindex


def minvalue(values):
    """
    A function that find the index of the minimum value in a list

    Parameters:
        values (list) : A list of rational values

    Returns:
        int : the index of the minimum value in the list
    """

    # The minimum value is set to the first element in the list and the minimum index is set to 0
    min_value = values[0]
    minindex = 0

    # A for loop iterates through the elements in values
    for i in range(len(values)):
        # A test is make to ensure the list only contains rational numbers
        isFloat(values[i], "Tried to find the minimum of a list with a non number")

        # If a new minimum is found then the minimum value and minimum index are updated
        if values[i] < min_value:
            minindex = i
            min_value = values[i]
    # Finally the index of the minimum value is returned
    return minindex


def meannvalue(values):
    """
    A function that the mean value of a list

    Parameters:
        values (list) : A list of rational values

    Returns:
        int : the mean value of the list
    """

    # The sum is originally 0
    valueSum = 0
    # The for loop iterates through the elements in values summing them
    for i in values:
        # A test is made to see if the list contains only rational numbers
        isFloat(i, "Tried to find mean of a list with a non number in")
        valueSum += i
    # Finally the mean is calculated and returned
    return valueSum / len(values)


def countvalue(values, x):
    """
    A function that counts the amount of times a value appears in a list

    Parameters:
        values (list) : A list of rational values
        x : The value that its number of appearances in the values is counted

    Returns:
        int : the number of times x appears in values
    """

    # The count is originally 0
    count = 0

    # The elements in values are iterated through using a for loop and counted using an if statement
    for i in values:
        if i == x:
            count += 1
    # Finally the count is returned
    return count


def file_reader(file_path):
    """
    A function that reads the csv data files from a given file path

    Parameters:
        file_path (string) : the file path to the csv file

    Returns:
        dict : a dictionary that has the data that was stored in the csv files
    """

    # The file is opened in read mode
    file = open(
        file_path,
        'r')

    # The headings of the csv file is saved to keys array
    keys = file.readline().rstrip('\n').split(',')

    # A record dictionary is instantiated
    record = {}

    # The headings of the csv file are set as the keys of the record dictionary via a for loop
    for key in keys:
        record[key] = []

    # A while statement is used to read all the rows of the csv file
    while True:
        # First the \n are removed from the end of the row and the values in the row are split into a list
        data = file.readline().rstrip('\n').split(',')

        # If the end of the file is reached the while loop is broken from
        if data == ['']:
            break

        # The date and times are left as string but the measurements are attempted to be cast as floats
        record[keys[0]].append(data[0])
        record[keys[1]].append(data[1])
        record[keys[2]].append(tryfloatcast(data[2]))
        record[keys[3]].append(tryfloatcast(data[3]))
        record[keys[4]].append(tryfloatcast(data[4]))

    # Finally the file is closed and the record is returned
    file.close()
    return record


def tryfloatcast(number):
    """
    This function tries to cast number to a float if it fails then the original value of number is returned

    Parameters:
        number : A possible float that is attempted to be cast to a float

    Returns:
        float or other : if successful cast then a number as a float is returned if not then number is returned
    """

    # Number is tried to be cast as a float if a ValueError occurs then number is returned otherwise the sucessfull cast is returned
    try:
        return float(number)
    except ValueError:
        return number


def get_data():
    """
    This function returns the data that is used in the reporting module

    Returns:
        dict : a dictionary containing the data from the 3 csv files
    """

    # The 3 csv files are read using the file reader function and the final data dictionary is returned
    return {"Harlington": file_reader(
        __file__.replace('\\', '/').rstrip('utils.py') + "data/Pollution-London Harlington.csv")
        , "Marylebourne Road": file_reader(
            __file__.replace('\\', '/').rstrip('utils.py') + 'data/Pollution-London Marylebone Road.csv')
        , "N Kensington": file_reader(
            __file__.replace('\\', '/').rstrip('utils.py') + 'data/Pollution-London N Kensington.csv')}


def find_8_neighbours(position, image):
    """
    This function find all the pixels that surround a pixel in an image

    Parameters:
        position (ndarray) : this is the position of the pixel that the neighbours will be found for
        image (ndarray) : this is the image that contain the pixel and its neighbours

    Returns:
        list : returns a list containing the position of the neighbour pixels
    """

    # All 8 possible neighbour directions are stored in a list
    directions = [[0, 1], [1, 0], [1, 1], [0, -1], [-1, 0], [-1, -1], [1, -1], [-1, 1]]

    # The neighbours list starts off as empty
    neighbours = []

    # The list of directions is iterates through and tested to see if it exists
    for direction in directions:
        # If the neighbour does exist then it is added to the neighbours list
        if 0 <= position[0] + direction[0] < image.shape[0] and 0 <= position[1] + direction[1] < image.shape[1]:
            neighbours.append(np.array([int(position[0] + direction[0]), int(position[1] + direction[1])]))

    # Finally the neighbours array is returned
    return neighbours


def merge_descending(left_half, right_half, left_indexes, right_indexes):
    """
    This function merges two list together in descending order

    Parameters:
        left_half (list) : A list of numbers that is to be sorted with a right half
        right_half (list) : A list of number that is to be sorted with a left half
        left_indexes (list) : A list of indexes that will be merged with the right indexes
        right_indexes (list): A list of indexes that will be merged with the left indexes

    Returns:
        list : A list of the two halves sorted in descending order
        list : A list of the original indexes of the sorted numbers
    """

    # The merged list and indexes start as empty lists and left and right indexes start at 0
    merged_list = []
    merged_indexes = []
    left_index = 0
    right_index = 0

    # While there is still items in both lists this while loop repeats
    while left_index < len(left_half) and right_index < len(right_half):
        # If the current item in the left half is greater than the current item in the right half it is then added to the merged list
        # and the left index is incremented by 1
        if left_half[left_index] >= right_half[right_index]:
            merged_list.append(left_half[left_index])
            merged_indexes.append(left_indexes[left_index])
            left_index += 1
        # Otherwise the current right item is added to the merged list and the right index is incremented by 1
        else:
            merged_list.append(right_half[right_index])
            merged_indexes.append(right_indexes[right_index])
            right_index += 1

    # While there are sill items left in one of either the left or right lists they are added to the merged list
    while left_index < len(left_half):
        merged_list.append(left_half[left_index])
        merged_indexes.append(left_indexes[left_index])
        left_index += 1

    while right_index < len(right_half):
        merged_list.append(right_half[right_index])
        merged_indexes.append(right_indexes[right_index])
        right_index += 1

    # Finally the merged list and list of indexes is returned
    return merged_list, merged_indexes


def merge_sort_descending(items, items_indexes):
    """
    This function performs a merge sort on a list in descending order using recursion

    Parameters:
        items (list) : A list of items to be sorted
        items_indexes (list) : A list of indexes to be sorted in order of the items sorted

    Returns:
        list : A list of items sorted in descending order
        list : A list of indexes sorted in the order items is sorted into
    """

    # If items is only 1 item or no item then items and indexes is returned
    # This is the base case
    if len(items) <= 1:
        return items, items_indexes
    else:
        # The midpoint of items is found and is used to split the lists into a left are right half
        midpoint = len(items) // 2
        left_half = items[:midpoint]
        right_half = items[midpoint:]
        left_indexes = items_indexes[:midpoint]
        right_indexes = items_indexes[midpoint:]

        # A recursive call is made on both of the halves to continue splitting them until they are a single item
        left_half, left_indexes = merge_sort_descending(left_half, left_indexes)
        right_half, right_indexes = merge_sort_descending(right_half, right_indexes)

        # Both halves of the lists are sorted and finally the merged lists are returned
        merged_items, merged_indexes = merge_descending(left_half, right_half, left_indexes, right_indexes)
    return merged_items, merged_indexes


def get_selection(valid_options, input_string, invalid_string):
    """
    This function gets a valid input selection from the user

    Parameters:
        valid_options (list) : A list that contains possible valid inputs
        input_string (str) : A string that is used to ask the user for an input
        invalid_string (str) : A string the is used to tell the user that they have entered an invalid string

    Returns:
        string : the valid user input is returned
    """

    # The user input starts off as nothing and invalid starts as True
    user_input = ""
    invalid = True

    # This while loop keeps repeating until a valid string is inputted
    while invalid:
        # A user input is gotten using the input string
        user_input = input(input_string).lower()

        # If the user input is valid then the while loop is stopped otherwise the invalid string is displayed
        if user_input in valid_options:
            invalid = False
        else:
            print(invalid_string)
    # Finally the valid user input is returned
    return user_input

