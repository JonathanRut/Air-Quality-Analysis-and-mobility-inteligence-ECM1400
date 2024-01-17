# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

from utils import *
from reporting import *
from intelligence import *
from monitoring import *
import re
import datetime


def main_menu():
    """
    This function displays a main menu and get the user to chose what module they want to access
    """

    # The while loop runs until the user chooses to quit the program
    while True:
        # A title is displayed
        print("""
 AQUA - Air Quality Analytics
==============================
        """)

        # The user picks the module they want to access and the input is stored in option
        option = get_selection(["r", "i", "m", "a", "q"],
"""
What would you like to do?
R - Access the PR module
I - Access the MI module
M - Access the RM module
A - Print the About text
Q - Quit the application

Enter your option here: """,
                               "\nYou have entered an invalid option enter the letter"
                               "\nFor example enter 'R' to access the PR module\n"
                               )

        # The corresponding module menu is run based off user input
        if option == "r":
            reporting_menu()
        elif option == "i":
            intelligence_menu()
        elif option == "m":
            monitoring_menu()
        elif option == "a":
            about()
        elif option == "q":
            quit()


def reporting_menu():
    """
    This function displays the menu for reporting allowing the user to create statistics on the data
    """

    # The csv data is gotten by using the get_data function
    data = get_data()
    # The menu runs until the user chooses to return to main menu
    while True:
        # A title is displayed for the menu
        print("\nPollution Reporting" +
              "\n===================\n")

        # The user selects the station that they want to create statistics on
        selected_station = get_selection(["london harlington", "london marylebone road", "london n kensington", "b"],
                                         """
What monitoring station would you like to generate statistics on?
- London Harlington
- London Marylebone Road
- London N Kensington

Or if you would like to return to main menu type 'B'
Enter your option here: """,
                                         "\nYou have entered an invalid option enter the name of the station"
                                         "\nFor example enter 'London Harlington' to select London Harlington\n"
                                         )

        # The corresponding shorthand is assigned to selected_station
        if selected_station == "london harlington":
            selected_station = "Harlington"
        elif selected_station == "london marylebone road":
            selected_station = "Marylebourne Road"
        elif selected_station == "london n kensington":
            selected_station = "N Kensington"
        elif selected_station == "b":
            break

        # This menu runs until the user chooses to go back to the station selection
        while True:
            # The user selects the pollutant they want to generate statistics on
            selected_pollutant = get_selection(["no", "pm10", "pm25", "b"],
                                               """
What pollutant would you like to generate stats for?
- no
- pm10
- pm25

Or if you would like to go back to station selection type 'B'
Enter your option here: """,

                                               "\nYou have entered an invalid option enter the name of the pollutant"
                                               "\nFor example enter 'no' to select the no pollutant\n"
                                               )
            # If the user has chosen b the the while loop is broken from
            if selected_pollutant == "b":
                break
            # This while loops runs until the user chooses to return to pollutant selection
            while True:
                # The user selects the task they would like to perform on the data
                selected_task = get_selection(["da", "dm", "ha", "ma", "ph", "cmd", "fmd", "b"],
                                              """
What stats would you like to generate?
DA - Calculate daily average for a pollutant
DM - Calculate daily median for a pollutant
HA - Calculate hourly average for a pollutant
MA - Calculate monthly average for a pollutant
PH - Find the peak hour on a data for a pollutant
CMD - Count the missing data for a pollutant
FMD - Fill the missing data for a pollutant

Or if you would like to go back to pollutant selection type 'B'
Enter your option here: """,
                                              "\nYou have entered an invalid option enter the task you would like to perform"
                                              "\nFor example enter 'DA' to find the daily average\n"
                                              )
                # The corresponding task is performed in this if statment
                if selected_task == "b":
                    break
                elif selected_task == "da":
                    # The daily averages are found and displayed via a for loop
                    results = daily_average(data, selected_station, selected_pollutant)
                    print("\nThe averages for each day in the year are: ")
                    for i in range(len(results)):
                        print(f'{data[selected_station]["date"][i * 24]}: {results[i]}')
                elif selected_task == "dm":
                    # The daily medians are found and displayed via a for loop
                    results = daily_median(data, selected_station, selected_pollutant)
                    print("\nThe medians for each day in the year are: ")
                    for i in range(len(results)):
                        print(f'{data[selected_station]["date"][i * 24]}: {results[i]}')
                elif selected_task == "ha":
                    # The hourly averages are found and displayed via a for loop
                    results = hourly_average(data, selected_station, selected_pollutant)
                    print("\nThe hourly averages for the year are: ")
                    for i in range(len(results)):
                        print(f'{data[selected_station]["time"][i]}: {results[i]}')
                elif selected_task == "ma":
                    # The monthly averages are found and displayed via a for loop
                    results = monthly_average(data,selected_station,selected_pollutant)
                    print("\nThe average for each month are: ")
                    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
                    for i in range(len(results)):
                        print(f'{months[i]}: {results[i]}')
                elif selected_task == "ph":
                    # The user inputs the date that they want to find the peak hour for
                    selected_date = get_selection(data[selected_station]["date"],
                                                  """
What date would you like the peak hour
                                                
Enter your date here: """,
                                                  "\nYou have entered an invalid date"
                                                  "\nYour date must be in the format YYYY-MM-DD\n"
                                                  )
                    # The peak hour and it's value are found and displayed
                    peak_hour, peak_value = peak_hour_date(data, selected_date, selected_station, selected_pollutant)
                    print(f"\nThe peak hour on {selected_date} is {peak_hour} with a reading of {peak_value}")
                elif selected_task == 'cmd':
                    # The missing data is counted and displayed
                    missing_data = count_missing_data(data, selected_station, selected_pollutant)
                    print(f"\nThere are {missing_data} 'No Data' entries")
                elif selected_task == 'fmd':
                    # This while loop runs until a valid value is inputted
                    while True:
                        # A fill value is gotten from the user
                        fill_value = input("""
What value would you like to replace 'No data' entries?
                        
Enter your value here: """)
                        # A test is made to see if the value is a float or not
                        # If it is then the while loop is broken
                        try:
                            fill_value = float(fill_value)
                            break
                        except ValueError:
                            print("\nYou have entered an invalid value"
                                  "\nYou must enter a number\n")
                    # Finally the missing data is filled
                    data = fill_missing_data(data, fill_value, selected_station, selected_pollutant)


def monitoring_menu():
    """
    This function displays the menu for monitoring allowing the user to create statistics on the live data
    """

    # The possible station codes are gotten using the function from the monitoring module
    station_codes = get_current_station_codes()
    # The loop runs until the user chooses to go back to main menu
    while True:
        # A title for the module is displayed
        print("\nReal-time Monitoring"
              "\n====================\n")
        # Valid codes and station info is generated for input
        valid_codes = [i.lower() for i in list(station_codes)]
        station_info = list(station_codes.values())

        # The selection string is made using the valid codes and station info
        selection_string = "\nWhat station would you generate stats for?"
        for i in range(len(station_info)):
            selection_string += f"\n{valid_codes[i].upper()} - {station_info[i]}"
        selection_string += "\n\nOr if you want to go back to main menu type 'B'" \
                            "\nEnter your option here: "
        valid_codes.append('b')

        # The user inputs what station they would like to generate stats on
        selected_station = get_selection(valid_codes, selection_string, "\nInvalid input for station"
                                                                        f"\nFor example enter '{valid_codes[0]}' for {station_info[0]}")
        # If the user wants to go back to main menu then the while loop is broken
        if selected_station == "b":
            break
        else:
            # The possible pollutants and information about them is gotten using the function in monitoring
            pollutants = get_pollutants_at_station(selected_station.upper())
            # This while loop runs until the user chooses to go back to station selection
            while True:
                # Valid pollutant codes and information about them is generated for user input
                valid_pollutant = [i.lower() for i in list(pollutants)]
                pollutant_info = list(pollutants.values())

                # The selection string is made using the pollutant codes and the information on the pollutant
                selection_string = "\nWhat pollutant do you want stats?"
                for i in range(len(valid_pollutant)):
                    selection_string += f"\n{valid_pollutant[i].upper()} - {pollutant_info[i]}"
                selection_string += "\n\nOr if you want to go back to station selection type 'B'" \
                                    "\nEnter your option here: "
                valid_pollutant.append('b')

                # The user inputs what pollutant they would like to generate stats for
                selected_pollutant = get_selection(valid_pollutant, selection_string, "\nInvalid input for pollutant"
                                                                                      f"\nFor example enter '{valid_pollutant[0]} for {pollutant_info[0]}'")

                # If the user chooses to got back to station selection the loop is broken
                if selected_pollutant == 'b':
                    break
                else:
                    # The option for task the user wants to perform is gotten
                    option = get_selection(["d", "ma", "da", 'b'],
                                            """
What would you like to do?
D - Graph a day
MA - Graph the monthly averages of a year
DA - Graph the daily averages of a month

Or if you want to go back to pollutant selection type 'B'
Enter your option here: """,
                                            "\nInvalid input for option"
                                            "\nFor example enter 'D' to graph a day\n")

                # The corresponding task is performed for the user
                if option == 'b':
                    break
                elif option == 'd':
                    date = ""
                    # If the user wants to display data for day they have to enter a date
                    # This while loop ensure that the date is valid
                    while True:
                        # The date is gotten from the user
                        date = input("""
What date would you like a graph for?

Enter the date here: """)
                        # A regex string is used to see if the date is valid if it is the while loop is broken
                        if re.match("\d{4}[-]\d{2}[-]\d{2}", date):
                            break
                        else:
                            print("\nInvalid date entered"
                                  "\nFor example enter '2022-01-02' for 2nd January 2022")

                    # The date is formatted so it is of type timedelta
                    date = datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))

                    # The graph, values and hours for the day are found
                    graph, values, hours = graph_day(selected_station.upper(), selected_pollutant.upper(), date)

                    # The graph is displayed and the values are displayed underneath with a for loop
                    print(graph)
                    for i in range(len(values)):
                        print(f"{hours[i]}:00 - {values[i]}")
                elif option == "ma":
                    year = ""
                    # If the user wants to display the monthly averages they must input a year
                    # This while loop ensure the year they input is valid
                    while True:
                        # The year is gotten from the user
                        year = input("""
Enter the year you would like to graph monthly averages?

Enter the year here: """)
                        # A regex string is used to see if the year is valid if it is then the while loop is broken
                        if re.match("\d{4}", year):
                            break
                        else:
                            print("\nInvalid date entered"
                                  "\nFor example enter '2021' for monthly averages in 2021")

                    # It takes a while to process and get the data so this is displayed
                    print("Getting data...")

                    # The graph, monthly averages and the months are gotten a
                    graph, values, month = graph_monthly_average(selected_station.upper(), selected_pollutant.upper(), year)

                    # The graph is the displayed and the monthly averages are displayed using a for loop
                    print(graph)
                    for i in range(len(values)):
                        print(f"{month[i]} - {values[i]}")
                elif option == "da":
                    year = ""
                    month = ""
                    # If the user wants to display the daily averages they must input the month and the year
                    # The while loop is used to ensure their inputs are valid
                    while True:
                        # The year and month are both gotten from the user
                        year = input("""
Enter the year and month you would like to graph the daily averages for a month?

Enter the year here: """)
                        month = input("Enter the month here: ")

                        # A regex string is used to see if month and year are valid if they are the loop is broken
                        if re.match("\d{4}", year) and re.match("\d{1}|\d{2}",month):
                            break
                        else:
                            print("\nInvalid date entered"
                                  "\nFor example enter '2021' for year and '1' for daily averages in January 2021")

                    # The graph, daily averages and days are gotten
                    graph, values, days = graph_month(selected_station.upper(), selected_pollutant.upper(), month, year)

                    # The graph is displayed and the daily averages are displayed underneath
                    print(graph)
                    for i in range(len(values)):
                        print(f"{days[i]} - {values[i]}")


def intelligence_menu():
    """
    This function displays the menu for intelligence allowing the user to process a map to find paths and measure walkability
    """

    # The upper and lower thresholds are given their default values
    upper_threshold = 100
    lower_threshold = 50
    # This menu runs until the user chooses to go back to main menu
    while True:
        # A title is displayed for the menu
        print("\nMobility Intelligence module"
              "\n============================\n")

        # The task that the user wants to perform is gotten
        option = get_selection(["r", "c", "cc", "ccs", "u", "l", "b"],
                               """
What would you like to do?
R - Detect red pixels in the map
C - Detect cyan pixels in the map
U - Change the upper threshold
L - Change the lower threshold
CC - Find connected components
CCS - Find 2 longest connected components and get a descending list of components

Or if you would like to go back to main menu type 'B'
Enter your option here: """,
                               "\nYou have entered an invalid option"
                               "\nFor example enter 'R' to find red pixels on the map\n"
                               )
        # The corresponding task is performed
        if option == "r":
            # This string is displayed as it takes a while for function to run
            print("\nFinding red pixels in map... ")

            # The function is runs and a message is displayed letting the user know that an image has been generated
            # highlighting red pixels
            find_red_pixels('map.png', upper_threshold, lower_threshold)
            print("\nThe new image highlighting the red pixels can be found in the data folder as 'map-red-pixels.jpg'")
        elif option == "c":
            # This string is displayed as it takes a while for function to run
            print("\nFinding cyan pixels in map... ")

            # The function is runs and a message is displayed letting the user know that an image has been generated
            # highlighting cyan pixels
            find_cyan_pixels('map.png', upper_threshold, lower_threshold)
            print("\nThe new image highlighting the cyan pixels can be found in the data folder as 'map-cyan-pixels.jpg'")
        elif option == "u":
            # If the user chooses to change the upper threshold a list of valid thresholds is made
            valid_options = [str(i) for i in range(256)]
            valid_options.append('c')

            # The new threshold is gotten from the user
            new_threshold = get_selection(valid_options,
                                          f"""
What would you like the new upper threshold to be for detection it is currently {upper_threshold}?

Or if you would like to cancel this type 'C'
Enter you new value here: """,
                                          "\nYou have entered an invalid value"
                                          "\nYou must enter a value in the range 0-255 or the 'C'")

            # If user didn't want to cancel the task then the new upper threshold is set
            if new_threshold != "c":
                upper_threshold = int(new_threshold)

        elif option == "l":
            # If the user chooses to change the lower threshold a list of valid thresholds is made
            valid_options = [str(i) for i in range(256)]
            valid_options.append('c')

            # The new threshold is gotten from the user
            new_threshold = get_selection(valid_options,
                                          f"""
What would you like the new lower threshold to be for detection it is currently {lower_threshold}?

Or if you would like to cancel this type 'C'
Enter you new value here:  """,
                                          "\nYou have entered an invalid value"
                                          "\nYou must enter a value in the range 0-255 'C'")

            # If the user didn't want to cancel the task then the new lower threshold is set
            if new_threshold != "c":
                lower_threshold = int(new_threshold)
        elif option == "cc":
            # The colour of connected components that the user wants to find is gotten
            colour_selection = get_selection(["r", "c", "b"],
                                             """
What colour would you like to find the connected components for?
R - Red
C - Cyan

Or if you want to return to the mobility intelligence selection type 'B'
Enter your option here: """,
                                             "\nYou have entered an invalid option"
                                             "\nFor example enter 'R' to detect red components")

            # The corresponding colour connected components is found
            if colour_selection == "r":
                # This string is displayed as it takes a while for function to run
                print("\nFinding red pixels in map... ")

                # The red pixels are highlighted then the connected components are found
                # and message is displayed letting the user know where the list of components are
                red_map = find_red_pixels('map.png', upper_threshold, lower_threshold)
                detect_connected_components(red_map)
                print("\nThe number of pixels inside each connected component region is writen into the text file 'cc-output-2a.txt' in the data folder")
            elif colour_selection == "c":
                # This string is displayed as it takes a while for function to run
                print("\nFinding cyan pixels in map... ")

                # The cyan pixels are highlighted then the connected components are found
                # and message is displayed letting the user know where the list of components are
                cyan_map = find_cyan_pixels('map.png', upper_threshold, lower_threshold)
                detect_connected_components(cyan_map)
                print("\nThe number of pixels inside each connected component region is writen into the text file 'cc-output-2a.txt' in the data folder")
        elif option == "ccs":

            # The colour of connected components that the user wants to find and sort is gotten
            colour_selection = get_selection(["r", "c", "b"],
                                             """
What colour would you like to find the 2 longest connected components for?
R - Red
C - Cyan

Or if you want to return to the mobility intelligence selection type 'B'
Enter your option here: """,
                                             "\nYou have entered an invalid option"
                                             "\nFor example enter 'R' to detect red components")

            # The corresponding colour connected components is found and sorted
            if colour_selection == "r":
                # This string is displayed as it takes a while for function to run
                print("\nFinding red pixels in map... ")

                # The red pixels are highlighted then the connected components are found and sorted
                # and message is displayed letting the user know where the list of components are
                # and the image with top 2 components
                red_map = find_red_pixels('map.png', upper_threshold, lower_threshold)
                mark = detect_connected_components(red_map)
                detect_connected_components_sorted(mark)
                print("\nAll connected components in decreasing order are writen into the text file 'cc-output-2b.txt' in the data folder")
                print("The two longest connected components are saved to 'cc-top-2.jpg' in the data folder")
            elif colour_selection == "c":
                # This string is displayed as it takes a while for function to run
                print("\nFinding cyan pixels in map... ")

                # The cyan pixels are highlighted then the connected components are found and sorted
                # and message is displayed letting the user know where the list of components are
                # and the image with top 2 components
                cyan_map = find_cyan_pixels('map.png', upper_threshold, lower_threshold)
                mark = detect_connected_components(cyan_map)
                detect_connected_components_sorted(mark)
                print("\nAll connected components in decreasing order are writen into the text file 'cc-output-2b.txt' in the data folder")
                print("The two longest connected components are saved to 'cc-top-2.jpg' in the data folder")
        elif option == "b":
            break


def about():
    """
    This function prints out the module code and my candidate number
    """
    # My module code and candidate number are printed
    print("\nModule code: ECM1400")
    print("Candidate Number: 242270\n")


def quit():
    """
    This function raises SystemExit causing the program to quit
    """

    # SystemExit is raised halting the program
    raise SystemExit


if __name__ == '__main__':
    main_menu()
