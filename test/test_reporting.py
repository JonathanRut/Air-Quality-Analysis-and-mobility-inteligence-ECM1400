import pytest
import reporting

@pytest.mark.parametrize("data, monitoring_station, pollutant, expected_result", [
    ({"MyStation": {"Gas": [i for i in range(24)]}}, "MyStation", "Gas", [11.5])
])
def test_daily_average(data, monitoring_station, pollutant, expected_result):
    result = reporting.daily_average(data, monitoring_station, pollutant)
    assert result == expected_result

@pytest.mark.parametrize("data, monitoring_station, pollutant, expected_result", [
    ({"MyStation": {"Gas": [i for i in range(24)]}}, "MyStation", "Gas", [11.5])
])
def test_daily_median(data, monitoring_station, pollutant, expected_result):
    result = reporting.daily_median(data, monitoring_station, pollutant)
    assert result == expected_result

@pytest.mark.parametrize("data, monitoring_station, pollutant, expected_result", [
    ({"MyStation": {"Gas": [i for i in range(48)]}}, "MyStation", "Gas", [(2 * i + 24) / 365 for i in range(24)])
])
def test_hourly_average(data, monitoring_station, pollutant, expected_result):
    result = reporting.hourly_average(data, monitoring_station, pollutant)
    assert result == expected_result

@pytest.mark.parametrize("data, monitoring_station, pollutant, expected_result", [
    ({"MyStation": {"Gas": [i for i in range(48)], "date":[f'2001-{(i + 24)//24:>02}' for i in range(48)]}}, "MyStation", "Gas",
     [11.5, 35.5])
])
def test_monthly_average(data, monitoring_station, pollutant, expected_result):
    result = reporting.monthly_average(data, monitoring_station, pollutant)
    assert result == expected_result

@pytest.mark.parametrize("data, date, monitoring_station, pollutant, expected_result", [
    ({"MyStation": {"Gas": [i for i in range(24)], "date": [f'2001-02-01' for i in range(24)],
                    "time": [f"{i:>02}:00:00" for i in range(24)]}}, "2001-02-01", "MyStation", "Gas", ('23:00:00', 23))
])
def test_peak_hour_date(data, date, monitoring_station, pollutant, expected_result):
    result = reporting.peak_hour_date(data, date, monitoring_station, pollutant)
    assert result == expected_result

@pytest.mark.parametrize("data, monitoring_station, pollutant, expected_result", [
    ({"MyStation": {"Gas": ['No data' if i % 6 == 0 else i for i in range(24)]}}, "MyStation", "Gas", 4)
])
def test_count_missing_data(data, monitoring_station, pollutant, expected_result):
    result = reporting.count_missing_data(data, monitoring_station, pollutant)
    assert result == expected_result

@pytest.mark.parametrize("data, new_value, monitoring_station, pollutant, expected_result", [
    ({"MyStation": {"Gas": ['No data' if i % 6 == 0 else i for i in range(24)]}}, 0, "MyStation", "Gas",
     {"MyStation": {"Gas": [0 if i % 6 == 0 else i for i in range(24)]}})
])
def test_fill_missing_data(data, new_value, monitoring_station, pollutant, expected_result):
    result = reporting.fill_missing_data(data, new_value, monitoring_station, pollutant)
    assert result == expected_result
