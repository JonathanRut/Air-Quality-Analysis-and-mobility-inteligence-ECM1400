# This is a template. 
# You should modify the functions below to match
# the signatures determined by the project specification.
# 
# This module will access data from the LondonAir Application Programming Interface (API)
# The API provides access to data to monitoring stations. 
# 
# You can access the API documentation here http://api.erg.ic.ac.uk/AirQuality/help
#

import datetime
import requests
from utils import *


def get_live_data_from_api(site_code='MY1', species_code='NO2', start_date=None, end_date=None):
    """
    Return data from the LondonAir API using its AirQuality API.
    """
    start_date = datetime.date.today() if start_date is None else start_date
    end_date = start_date + datetime.timedelta(days=1) if end_date is None else end_date
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Data/SiteSpecies/SiteCode={site_code}/SpeciesCode={species_code}/StartDate={start_date}/EndDate={end_date}/Json"
    url = endpoint.format(
        site_code=site_code,
        species_code=species_code,
        start_date=start_date,
        end_date=end_date
    )
    res = requests.get(url)
    return res.json()


def get_current_station_codes():
    """
    This function returns a dictionary of London station codes and a corresponding bit of information about each station

    Returns:
        dict : A dictionary with station codes as keys and information of that station as values
    """
    # Data about the stations is retrieved from the API
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName={GroupName}/Json"
    url = endpoint.format(GroupName="London")
    res = requests.get(url)
    # A for loop iterates through each station that was returned in the API and creates a dictionary of required information
    station_codes = {}
    for i in res.json()['Sites']['Site']:
        # The keys are the station codes
        # and values are information of the station
        # the information includes the name of the station and the date that if opened and the date that it closed
        station_codes[i[
            '@SiteCode']] = f"{i['@SiteName'].lstrip('-').lstrip(' ')} open from {i['@DateOpened']} to {'current date' if i['@DateClosed'] == '' else i['@DateClosed']}"
    # Finally the dictionary of station codes is returned
    return station_codes


def get_pollutants_at_station(site_code):
    """
        This function returns a dictionary of pollutants at a station
        and a corresponding bit of information about each pollutant

        Returns:
            dict : A dictionary with pollutant codes as keys and information of that pollutant as values
        """
    # Data about the pollutants is retrieved from the API
    endpoint = "https://api.erg.ic.ac.uk/AirQuality/Information/MonitoringSiteSpecies/GroupName={GroupName}/Json"
    url = endpoint.format(GroupName="London")
    res = requests.get(url)
    data = res.json()['Sites']['Site']
    # A dictionary of possible pollutants at that station is made
    # This is done by iterating though the station info in the data from the API
    possible_pollutants = {}
    for station_info in data:
        # If the station code matches the current station code then this if statement is true
        if station_info['@SiteCode'] == site_code:
            # If the station only monitors 1 pollutant then that pollutant and its information is returns
            if type(station_info['Species']) == dict:
                return {station_info['Species'][
                            '@SpeciesCode']: f"{station_info['Species']['@SpeciesDescription']} measured from {station_info['Species']['@DateMeasurementStarted']} to {'current date' if station_info['Species']['@DateMeasurementFinished'] == '' else station_info['Species']['@DateMeasurementFinished']} "}
            # For each pollutant at the station it is added to the dictionary with the key being the pollutant code
            # and the information being a description of the pollutant and the dates which it was measured
            for pollutant in station_info['Species']:
                possible_pollutants[pollutant[
                    '@SpeciesCode']] = f"{pollutant['@SpeciesDescription']} measured from {pollutant['@DateMeasurementStarted']} to {'current date' if pollutant['@DateMeasurementFinished'] == '' else pollutant['@DateMeasurementFinished']} "
    return possible_pollutants


def graph_day(site_code, species_code, day):
    """
    This function graphs the values for each hour in a day

    Parameters:
        site_code (str) : This site that data will be retrieved from
        species_code (str) : The pollutant code for the pollutant that will be graphed
        day (timedelta) : The day that will be graphed

    Returns:
        string : The graph showing the data about the day
        list : The list of values recorded at each hour
        list : The list of the hours in the day
    """
    # Data about the day is retrieved from tha API
    res = get_live_data_from_api(site_code, species_code, day, day + datetime.timedelta(days=1))
    data = res['RawAQData']['Data']
    # The values and times are stored in list and taken from the data using a for loop
    empty = True
    values = []
    times = []
    for measurement in data:
        if measurement['@Value'] != '':
            values.append(float(measurement['@Value']))
            times.append(measurement['@MeasurementDateGMT'][11:13])
            # A test is made to see if there was data collected on the desired day
            empty = False
    # If no data was collected on the desired day then a string is returned relaying this information
    if empty:
        return "No data for that time", "", ""
    # The values recorded are sorted in descending order to help create the graph string and the max value is found
    values_sorted, times_sorted = merge_sort_descending(values, times)
    max_value = values_sorted[0]
    # Empty lines are created to be filled with the data
    lines = [" " * 3 * len(values_sorted) for _ in range(10, -1, -1)]
    # The values are iterated through to add the data to the lines
    for i in range(len(values_sorted)):
        # Data is scaled to the max value and represented as XXX
        graph_value = int((values_sorted[i] * 10) / max_value)
        lines[graph_value] = lines[graph_value][:3 * int(times_sorted[i])] \
                             + "XXX" + lines[graph_value][3 * int(times_sorted[i]) + 3:]
    # Finally the lines of the graph are put together using a for loop
    # and an f string is used to mark the y-axis of the graph
    graph = ""
    for i in range(10, -1, -1):
        graph += f'{max_value * i / 10:>7.2f}|{lines[i]}\n'
    graph += 8 * " "
    # A for loop is used here to label the x-axis of the graph
    for time in times:
        graph += time + "|"
    # Finally the graph its values and the times are returned
    return graph, values, times


def graph_monthly_average(site_code, species_code, year):
    """
    This function graphs the values for the averages of each month in a year

    Parameters:
        site_code (str) : This site that data will be retrieved from
        species_code (str) : The pollutant code for the pollutant that will be graphed
        year (str) : The year of the month that averages will be graphed

    Returns:
        string : The graph showing the data about the monthly averages
        list : The list of monthly averages
        list : The list of months in the year
    """

    # The data about the year is retrieved from the API
    res = get_live_data_from_api(site_code, species_code, datetime.date(int(year), 1, 1, ),
                                 datetime.date(int(year), 12, 31))
    data = res['RawAQData']['Data']

    # Initial values for variables are set
    empty = True
    monthly_averages = []
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_month = '01'
    month_sum = 0
    days = 0

    # The measurements are iterated through and the mean for each month is calculated
    for measurement in data:
        if measurement['@Value'] != '':
            # This if statements is true if the current month changes
            # When true it calculates the average for the month
            # and then updates the current month also resting the counters
            if current_month != measurement['@MeasurementDateGMT'][5:7]:
                if days == 0:
                    monthly_averages.append(0)
                else:
                    monthly_averages.append(month_sum / days)
                days = 0
                month_sum = 0
                current_month = f'{str(int(current_month) + 1):>02}'
            # The month values are summed and the days is incremented by 1
            month_sum += float(measurement['@Value'])
            days += 1
            empty = False
    # The empty test is used to tell if there is data for the selected year
    if empty:
        return "No data for that time", "", ""
    # The final average is added to the list
    monthly_averages.append(month_sum / days)

    # A list numerical values representing months is created
    month_dates = [i for i in range(12)]

    # The list of monthly averages is sorted in descending order for plotting the graph and the max value is found
    averages_sorted, months_sorted = merge_sort_descending(monthly_averages, month_dates)
    max_value = averages_sorted[0]

    # A list of empty lines is made for plotting the graph
    lines = [" " * 4 * len(averages_sorted) for _ in range(10, -1, -1)]

    # The averages are added to the lines in this for loop and the graph is scaled to the max value
    for i in range(len(averages_sorted)):
        graph_value = int((averages_sorted[i] * 10) / max_value)
        lines[graph_value] = lines[graph_value][: 4 * int(months_sorted[i])] + "XXXX" + lines[graph_value][4 * (
                int(months_sorted[i]) + 1):]

    # The lines are added to the graph in this for loop with the values and the y-axis is labeled
    graph = ""
    for i in range(10, -1, -1):
        graph += f'{max_value * i / 10:>7.2f}|{lines[i]}\n'

    # The x-axis is labeled with the months in this for loop
    graph += 8 * " "
    for month in months:
        graph += month + "|"

    # Finally the graph, monthly averages and a list of months is returned
    return graph, monthly_averages, months


def graph_month(site_code, species_code, month, year):
    """
        This function graphs the daily averages for each day in a month

        Parameters:
            site_code (str) : This site that data will be retrieved from
            species_code (str) : The pollutant code for the pollutant that will be graphed
            month (str) : The month which daily averages are found from
            year (str) : The year which the selected month is in

        Returns:
            string : The graph showing the data about the daily averages for the month
            list : The list of daily averages
            list : The list of days in the month
        """

    # The data about the month is retrieved from the API
    res = get_live_data_from_api(site_code, species_code, datetime.date(int(year), int(month), 1, ),
                                 datetime.date(int(year), int(month) + 1, 1))
    data = res['RawAQData']['Data']

    # Initial values for variables are set
    empty = True
    day_averages = []
    days = ['01']
    current_day = '01'
    hours = 0
    day_sum = 0
    # The measurements are iterated through and the mean for each day is calculated
    for measurement in data:
        if measurement['@Value'] != '':
            # This if statement is true if the current dat changes
            # When true it calculates the average for the day
            # and then updates the current day also resting the counters
            if current_day != measurement['@MeasurementDateGMT'][8:10]:
                days.append(measurement['@MeasurementDateGMT'][8:10])
                day_averages.append(day_sum / hours)
                hours = 0
                day_sum = 0
                current_day = f'{str(int(current_day) + 1):>02}'
            # The day values are summed in this for loop and the hours are incremented by 1
            day_sum += float(measurement['@Value'])
            hours += 1
            empty = False
    # If there is no data for the month then this information is returned
    if empty:
        return "No data for that time", "", ""
    # The final day average is added to the list
    day_averages.append(day_sum / hours)

    # The list of daily averages is sorted in descending order for plotting the graph and the max value is found
    values_sorted, days_sorted = merge_sort_descending(day_averages, days)
    max_value = values_sorted[0]

    # A list of empty lines is made for plotting the graph
    lines = [" " * 3 * len(values_sorted) for _ in range(10, -1, -1)]

    # The averages are added to the lines in this for loop and the graph is scaled to the max value
    for i in range(len(values_sorted)):
        graph_value = int((values_sorted[i] * 10) / max_value)
        lines[graph_value] = lines[graph_value][:3 * (int(days_sorted[i]) - 1)] + "XXX" + lines[graph_value][3 * (
                int(days_sorted[i]) - 1) + 3:]

    # The lines are added to the graph in this for loop with the values and the y-axis is labeled
    graph = ""
    for i in range(10, -1, -1):
        graph += f'{max_value * i / 10:>7.2f}|{lines[i]}\n'

    # The x-axis is labeled with the days in this for loop
    graph += 8 * " "
    for day in days:
        graph += day + "|"

    # Finally the graph, daily averages and a list of days is returned
    return graph, day_averages, days
