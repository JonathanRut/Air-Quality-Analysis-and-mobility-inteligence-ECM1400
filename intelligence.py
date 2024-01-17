# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

from matplotlib import pyplot as mat_plot
from utils import *


def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    This function finds the red path pixels in the map and returns a map with the red paths highlighted
    the map is also saved into a jpg

    Parameters:
        map_filename (str) : The filename of the map that is to be processed
        upper_threshold (int) : The upper threshold used to detect red pixels
        lower_threshold (int) : The lower threshold used to detect red pixels

    Returns:
        ndarray : An array that represents the map with the red pixels highlighted
    """
    # First the map is read and scaled up so the rgb values are in the range 0-255
    rgb_img = mat_plot.imread(__file__.replace('\\', '/').rstrip('intelligence.py') + "data/" + map_filename)
    rgb_img = rgb_img * 255
    # A new empty image of zeros is created using the dimensions of the map
    img_w = rgb_img.shape[0]
    img_h = rgb_img.shape[1]
    new_image = np.zeros((img_w, img_h, 3))
    # A nested for loop is used to traverse the image in search of red pixels
    for x in range(img_w):
        for y in range(img_h):
            # This if statement is true if a red pixel is detected
            # The pixel is red if there is enough red in the pixel and not too much blue or green
            # If the pixel is red then a white pixel is placed in the same position of the new image otherwise the new
            # image pixel is black
            if rgb_img[x, y, 0] > upper_threshold and rgb_img[x, y, 1] < lower_threshold \
                    and rgb_img[x, y, 2] < lower_threshold:
                new_image[x, y] = np.array([255, 255, 255])
            else:
                new_image[x, y] = np.array([0, 0, 0])
    # The image with the highlighted pixels values are changed to be integers
    # then saved to the data folder and returned
    mat_plot.imsave(__file__.replace('\\', '/').rstrip('intelligence.py') + "data/map-red-pixels.jpg",
                    np.uint8(new_image))
    return new_image


def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    This function finds the cyan path pixels in the map and returns a map with the cyan paths highlighted
    the map is also saved into a jpg

    Parameters:
        map_filename (str) : The filename of the map that is to be processed
        upper_threshold (int) : The upper threshold used to detect cyan pixels
        lower_threshold (int) : The lower threshold used to detect cyan pixels

    Returns:
        ndarray : An array that represents the map with the cyan pixels highlighted
    """

    # First the map is read and scaled up so the rgb values are in the range 0-255
    rgb_img = mat_plot.imread(__file__.replace('\\', '/').rstrip('intelligence.py') + "data/" + map_filename)
    rgb_img = rgb_img * 255

    # A new empty image of zeros is created using the dimensions of the map
    img_w = rgb_img.shape[0]
    img_h = rgb_img.shape[1]
    new_image = np.zeros((img_w, img_h, 3))

    # A nested for loop is used to traverse the image in search of red pixels
    for x in range(img_w):
        for y in range(img_h):
            # This if statement is true if a cyan pixel is detected
            # The pixel is cyan if there is enough blue and green in the pixel and not too much red
            # If the pixel is cyan then a white pixel is placed in the same position of the new image otherwise the new image pixel is black
            if rgb_img[x, y, 0] < lower_threshold and rgb_img[x, y, 1] > upper_threshold and rgb_img[x, y, 2] > upper_threshold:
                new_image[x, y] = np.array([255, 255, 255])
            else:
                new_image[x, y] = np.array([0, 0, 0])
    # The image with the highlighted pixels values are changed to be integers
    # then saved to the data folder and returned
    mat_plot.imsave(__file__.replace('\\', '/').rstrip('intelligence.py') + "data/map-cyan-pixels.jpg", np.uint8(new_image))
    return new_image


def detect_connected_components(IMG):
    """
    This function detects connected components in one of the highlighted images and saves a list them to a text file

    Parameters:
        IMG (ndarray) : A image of the either cyan or red paths highlighted

    Returns:
        ndarray : Returns a 2D array of connected components marked
    """

    # A 2D array of zeros is made using the dimensions of the image
    mark = np.zeros((IMG.shape[0], IMG.shape[1]))
    # An empty queue is made and the counter and string for connected components are set to their starting values
    queue = np.empty([0, 2])
    current_component = 1
    write_string = ""
    # A nested for loop is used to traverse the image in search of connected components
    for x in range(mark.shape[0]):
        for y in range(mark.shape[1]):
            # If a highlighted pixel is found then this if statement is true
            if (IMG[x, y] == np.array([255, 255, 255])).all() and (mark[x, y] == 0).all():
                # The pixel is marked as visited and added to the queue
                mark[x, y] = current_component
                queue = np.append(queue, np.array([[x, y]]), axis=0)
                # A count is started for the number of pixels in the component
                num_pixels = 1
                # This for loop runs while the queue is not empty
                while len(queue) != 0:
                    # The first item in the queue is dequeued and stored as pixel
                    pixel = queue[0]
                    queue = queue[1:]
                    # The 8 neighbours of the pixel are iterated through to find if they are highlighted pixels too
                    for neighbour in find_8_neighbours(pixel, IMG):
                        # If the neighbour is highlighted and unvisited then the if statement is true
                        # When true the neighbour is marked as visited and added to the queue
                        # The number of pixels in the component is incremented
                        if (IMG[neighbour[0], neighbour[1]] == np.array([255, 255, 255])).all() and (mark[neighbour[0], neighbour[1]] == 0).all():
                            mark[neighbour[0], neighbour[1]] = current_component
                            queue = np.append(queue, [neighbour], axis=0)
                            num_pixels += 1
                # When the connected component is fully found then it is added to the write string and the number of connected components is incremented
                write_string += f"Connected Component {current_component}, number of pixels = {num_pixels}\n"
                current_component += 1
    # The final line of the write string is the total number of connected components in the image
    write_string += f"Total number of connected components = {current_component - 1}"
    # The text file is open written to then closed
    file = open(__file__.replace('\\', '/').rstrip('intelligence.py') + "data/cc-output-2a.txt", 'w')
    file.write(write_string)
    file.close()
    # Finally the array of the marked connected components is returned
    return mark


def detect_connected_components_sorted(mark):
    """
    This function sorts the connected components in descending order saved the results to a text file
    and then saves the two longest components to a jpg

    Parameters:
        mark (ndarray) : This is a 2D array representing the connected components in an image
    """

    # A dictionary of connected components and their length is made
    components_dict = {}
    # A nested for loop is made to traverse mark in search of connected components
    for x in range(mark.shape[0]):
        for y in range(mark.shape[1]):
            # This if statement is true when part of a connected component is found
            # If true then an attempt is made to increment the length of the component in the dictionary
            # if this attempt fails to the component not being in the dictionary it is added
            if mark[x,y] != 0:
                try:
                    components_dict[int(mark[x,y])] += 1
                except KeyError:
                    components_dict[int(mark[x, y])] = 1

    # The numbers for each component and the length of each component is extracted from the dictionary
    components_numbers = list(components_dict)
    components_counts = list(components_dict.values())

    # The components lengths are sorted in descending order and their identity numbers remain intact
    components_counts_sorted, components_numbers_sorted = merge_sort_descending(components_counts, components_numbers)

    # A string is created using a for loop to list the connected components in descending order
    write_string = ""
    for i in range(len(components_counts_sorted)):
        write_string += f"Connected Component {components_numbers_sorted[i]}, number of pixels = {components_counts_sorted[i]}\n"

    # The final line of the string is the total number of components
    write_string += f"Total number of connected components = {len(components_numbers)}"

    # A text file is opened, written to and then closed to save the components in descending order
    file = open(__file__.replace('\\', '/').rstrip('intelligence.py') + "data/cc-output-2b.txt", 'w')
    file.write(write_string)
    file.close()

    # The identifier of the top 2 components are saved into a list
    top_components = [components_numbers_sorted[0], components_numbers_sorted[1]]

    # A new image of only the top 2 components is created
    top_2 = np.zeros((mark.shape[0], mark.shape[1], 3))

    # A nested for loop is used to traverse mark is search of the position of the top 2 components
    for x in range(mark.shape[0]):
        for y in range(mark.shape[1]):
            # If a pixel of one of the top 2 components is found then it is highlighted in this new image
            if int(mark[x,y]) in top_components:
                top_2[x,y] = np.array([255,255,255])
    # Finally the new image with the two top components is saved as a jpg
    mat_plot.imsave(__file__.replace('\\', '/').rstrip('intelligence.py') + "data/cc-top-2.jpg", np.uint8(top_2))


