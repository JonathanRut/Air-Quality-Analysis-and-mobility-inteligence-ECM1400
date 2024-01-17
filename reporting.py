# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification

from utils import *


def daily_average(data, monitoring_station: str, pollutant: str):
    """
    A function that finds the daily average of a year for a given monitoring station and pollutant

    Parameters:
        data (dict) : a dictionary of the data read from the 3 csv files
        monitoring_station (str) : a string of a monitoring station
        pollutant (str) : a string of a pollutant

    Returns:
        list : a list containing the daily averages
    """
    # The station data and pollutant data are both grabbed from data
    station_data = data[monitoring_station]
    pollutant_data = station_data[pollutant]
    # The outer for loop iterates for each day in the year
    daily_averages = []
    for i in range(0, len(pollutant_data), 24):
        # The inner for loop sums the values for the hours in each day
        values_sum = 0
        for j in range(i, i + 24):
            # if there is no data it is ignored in calculations
            if pollutant_data[j] != 'No data':
                values_sum += pollutant_data[j]
        # The average for the day is added to the list of averages
        daily_averages.append(values_sum / 24)
    # The list of averages is returned
    return daily_averages


def daily_median(data, monitoring_station: str, pollutant: str):
    """
    A function that finds the daily medians of a year for a given monitoring station and pollutant

    Parameters:
        data (dict) : a dictionary of the data read from the 3 csv files
        monitoring_station (str) : a string of a monitoring station
        pollutant (str) : a string of a pollutant

    Returns:
        list : a list containing the daily medians
    """

    # The station data and pollutant data are both grabbed from data
    station_data = data[monitoring_station]
    pollutant_data = station_data[pollutant]

    # The outer for loop iterates for each day in the year
    daily_medians = []
    for i in range(0, len(pollutant_data), 24):
        # The inner for loop creates a list of the values recorded at each hour in the day
        values = []
        for j in range(i, i + 24):
            # If there is no data it is ignored in the calculations
            if pollutant_data[j] != 'No data':
                values.append(pollutant_data[j])
        # The list of the hour values is sorted
        values.sort()
        # If there is data for the day the position of the median is found
        # then the median for that day is added to the other list of medians
        if not values:
            continue
        elif len(values) % 2 == 0:
            median = (values[len(values)//2] + values[(len(values)//2) - 1])/2
            daily_medians.append(median)
        else:
            median = values[(len(values) - 1)//2]
            daily_medians.append(median)

    # Finally the daily median is returned
    return daily_medians


def hourly_average(data, monitoring_station, pollutant):
    """
    A function that finds the hourly average of a year for a given monitoring station and pollutant

    Parameters:
        data (dict) : a dictionary of the data read from the 3 csv files
        monitoring_station (str) : a string of a monitoring station
        pollutant (str) : a string of a pollutant

    Returns:
        list : a list containing the hourly averages
    """

    # The station data and pollutant data are both grabbed from data
    station_data = data[monitoring_station]
    pollutant_data = station_data[pollutant]

    # The outer for loop iterates through each hour in a day
    hourly_averages = []
    for i in range(24):
        # The values for the hour is summed in the inner for loop
        values_sum = 0
        for j in range(i, len(pollutant_data), 24):
            # No data entries are ignored in calculations
            if pollutant_data[j] != 'No data':
                values_sum += pollutant_data[j]
        # The average for the hour is added to the list of averages
        hourly_averages.append(values_sum / 365)
    # The list of hourly averages is returned
    return hourly_averages


def monthly_average(data, monitoring_station, pollutant):
    """
    A function that finds the monthly average of a year for a given monitoring station and pollutant

    Parameters:
        data (dict) : a dictionary of the data read from the 3 csv files
        monitoring_station (str) : a string of a monitoring station
        pollutant (str) : a string of a pollutant

    Returns:
        list : a list containing the monthly averages
    """

    # The station data and pollutant data are both grabbed from data
    station_data = data[monitoring_station]
    pollutant_data = station_data[pollutant]

    # The dates are grabbed from the station data
    dates = station_data["date"]

    # Variables required for calculation in initialised
    monthly_averages = []
    current_month = '01'
    month_sum = 0
    days = 0

    # The for loop iterates through the year
    for i in range(len(dates)):
        # If the current month has changed to the next month this if statement is true
        if current_month != dates[i][5:7]:
            # The monthly average is added to the list
            monthly_averages.append(month_sum / days)
            # Days and months are reset
            days = 0
            month_sum = 0
            # The current month is changed using an f string
            current_month = f'{str(int(current_month) + 1):>02}'

        # No data entries are ignored in calculations
        if pollutant_data[i] != 'No data':
            month_sum += pollutant_data[i]
            days += 1
    # The final monthly average is added to the list and the list is returned
    monthly_averages.append(month_sum / days)
    return monthly_averages


def peak_hour_date(data, date, monitoring_station, pollutant):
    """
    A function that finds the peak hour of a pollutant for a given date at a given monitoring station

    Parameters:
        data (dict) : a dictionary of the data read from the 3 csv files
        date (str) : a string in the format yyyy-mm-dd
        monitoring_station (str) : a string of a monitoring station
        pollutant (str) : a string of a pollutant

    Returns:
        tuple : a tuple containing peak hour and peak value
    """
    # The station data and pollutant data are both grabbed from data
    station_data = data[monitoring_station]
    pollutant_data = station_data[pollutant]
    # The dates and hours are taken from station data
    dates = station_data["date"]
    hours = station_data["time"]
    # A peak value and hour are defined
    peak_value = 0
    peak_hour = ''
    # The whole set of data for the monitoring station is iterated through in a linear search
    for i in range(len(dates)):
        # If the dates match and the value at that hour is greater than the current peak the if statement is true
        # No data entries are ignored
        if dates[i] == date and peak_value < pollutant_data[i] != 'No data':
            # The peak hour and peak value are updated to new peak value and hour
            peak_hour = hours[i]
            peak_value = pollutant_data[i]
    # The peak hour and peak value are returned
    return peak_hour, peak_value


def count_missing_data(data, monitoring_station, pollutant):
    """
    A function that count No data entries for a given monitoring station and pollutant

    Parameters:
        data (dict) : a dictionary of the data read from the 3 csv files
        monitoring_station (str) : a string of a monitoring station
        pollutant (str) : a string of a pollutant

    Returns:
        int : the number of No data entries
    """

    # The station data and pollutant data are both grabbed from data
    station_data = data[monitoring_station]
    pollutant_data = station_data[pollutant]

    # The count value utility function is used to count No data entries
    return countvalue(pollutant_data, 'No data')


def fill_missing_data(data, new_value, monitoring_station, pollutant):
    """
    A function fills the missing data entries with a new value for a given pollutant and monitoring station

    Parameters:
        data (dict) : a dictionary of the data read from the 3 csv files
        new_value (float) : a rational number value that will replace No data entries
        monitoring_station (str) : a string of a monitoring station
        pollutant (str) : a string of a pollutant

    Returns:
        dict : returns data with updated values
    """

    # The station data and pollutant data are both grabbed from data
    station_data = data[monitoring_station]
    pollutant_data = station_data[pollutant]

    # A for loop goes through the data to replace the No data entries with the new value
    for i in range(len(pollutant_data)):
        pollutant_data[i] = new_value if pollutant_data[i] == 'No data' else pollutant_data[i]
    # Finally the updated data is returned
    return data
