import datetime
import pytest
import monitoring


def test_get_current_station_codes():
    result = monitoring.get_current_station_codes()
    assert type(result) == dict


@pytest.mark.parametrize("station_code, expected_result", [
    ("WM9", {"NO2": "Nitrogen Dioxide measured from 2016-08-08 14:00:00 to 2017-09-20 00:00:00 "}),
    ("CT6", {"CO": "Carbon Monoxide measured from 2007-04-01 00:00:00 to 2010-04-08 00:00:00 ",
             "NO2": "Nitrogen Dioxide measured from 2008-01-01 00:00:00 to current date ",
             "O3": "Ozone measured from 2009-04-09 00:00:00 to 2013-01-31 00:00:00 "})
])
def test_get_pollutants_at_station(station_code, expected_result):
    result = monitoring.get_pollutants_at_station(station_code)
    assert result == expected_result


@pytest.mark.parametrize("station_code, pollutant_code, date, expected_result", [
    ("CT6", "NO2", datetime.date(2022, 10, 31), ("""  93.00|                                             XXX                        
  83.70|                        XXX   XXX               XXXXXX                  
  74.40|                     XXX   XXX   XXXXXXXXXXXX         XXX               
  65.10|                                                                        
  55.80|                  XXX                                    XXXXXX         
  46.50|                                                                        
  37.20|XXX            XXX                                             XXXXXX   
  27.90|   XXX      XXX                                                         
  18.60|      XXXXXX                                                         XXX
   9.30|                                                                        
   0.00|                                                                        
        00|01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|""",
                                                 [43.1, 33.2, 27.7, 23.1, 29.2, 42.7, 57.7, 80.2, 86.3, 77.7, 87.0, 78.3, 80.5, 78.2, 80.5, 93.0, 87.4, 87.8, 74.5, 57.8, 56.1, 40.7, 40.4, 24.6],
                                                 ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23'])),
    ("CT6", "NO2", datetime.date(2004, 2, 8), ("No data for that time", "", ""))

])
def test_graph_day(station_code, pollutant_code, date, expected_result):
    result = monitoring.graph_day(station_code, pollutant_code, date)
    assert result == expected_result


@pytest.mark.parametrize("station_code, pollutant_code, year, expected_result", [
    ("CT6", "NO2", '2021', ("""  60.70|                                XXXX            
  54.63|                                    XXXX        
  48.56|                                        XXXXXXXX
  42.49|    XXXX    XXXXXXXXXXXXXXXX                    
  36.42|XXXX    XXXX                XXXX                
  30.35|                                                
  24.28|                                                
  18.21|                                                
  12.14|                                                
   6.07|                                                
   0.00|                                                
        Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec|""",
                                                 [39.199253731343276, 43.115615141955836, 41.093487109905006, 45.83333333333332, 45.61738544474392, 43.55320334261835, 46.28025210084034, 38.67081081081078, 60.7032549728752, 54.65862533692705, 51.267642956764305, 50.78720445062587],
                                                 ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])),
    ("CT6", "NO2", '2004', ("No data for that time", "", ""))

])
def test_graph_monthly_average(station_code, pollutant_code, year, expected_result):
    result = monitoring.graph_monthly_average(station_code, pollutant_code, year)
    assert expected_result == result


@pytest.mark.parametrize("site_code, species_code, month, year, expected_result", [
    ("CT6", "NO2", '10', '2021', ("""  78.10|                                             XXX                                             
  70.29|                        XXX                                       XXX                        
  62.48|                  XXXXXX                                                XXX      XXXXXX      
  54.67|         XXX                        XXX   XXX   XXXXXX                     XXXXXX      XXX   
  46.86|XXXXXX         XXX                     XXX               XXX   XXX   XXX                     
  39.05|            XXX            XXXXXXXXX                        XXX                              
  31.24|                                                      XXX                                 XXX
  23.43|      XXX                                                                                    
  15.62|                                                                                             
   7.81|                                                                                             
   0.00|                                                                                             
        01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31|""",
                            [53.10833333333335, 47.508333333333326, 23.47083333333333, 58.916666666666636, 42.595833333333346, 46.916666666666664, 67.34166666666667, 65.16250000000001, 71.45416666666668, 40.01666666666667, 43.974999999999994, 46.421739130434794, 58.82083333333333, 54.179166666666674, 56.220833333333324, 78.09583333333333, 55.8375, 59.449999999999996, 38.62916666666667, 49.754166666666656, 43.70416666666666, 53.79583333333332, 72.10833333333333, 53.25000000000001, 62.9086956521739, 59.57916666666666, 59.36666666666667, 69.84583333333335, 67.7375, 58.80833333333334, 35.43750000000001],
                            ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
)),
    ("CT6", "NO2", '02', '2004', ("No data for that time", "", ""))
])
def test_graph_month(site_code, species_code, month, year, expected_result):
    result = monitoring.graph_month(site_code, species_code, month, year)
    assert expected_result == result
