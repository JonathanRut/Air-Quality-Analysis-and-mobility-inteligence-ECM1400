import pytest
import utils
import numpy as np


@pytest.mark.parametrize("number, expected_result",[
    (1.2, None),
    (12, None),
    (-1, None),
    (-1.2, None)
])
def test_testFloat_valid(number, expected_result):
    result = utils.isFloat(number, "Error")
    assert result == expected_result


@pytest.mark.parametrize("number", [
    "one",
    "-2",
    "1.2",
    "1"
])
def test_testFloat_invalid(number):
    with pytest.raises(ValueError):
        utils.isFloat(number, "Error")


@pytest.mark.parametrize("values, expected_result", [
    ([1, 2, 3], 6),
    ([9], 9),
    ([9, 3.2, 6.4, 7, 12], 37.6),
    ([2, -1, 8, 5.2], 14.2)
])
def test_sumvalues_valid(values, expected_result):
    result = utils.sumvalues(values)
    assert result == expected_result

@pytest.mark.parametrize("values", [
    (['a', 'b', 3]),
    ([9, '0', 2]),
    (['-1', 's', '2.2'])
])
def test_sumvalues_invalid(values):
    with pytest.raises(ValueError):
        utils.sumvalues(values)


@pytest.mark.parametrize("values, expected_result", [
    ([1, 2, 3], 2),
    ([9], 0),
    ([9, 3.2, 6.4, 7, 12], 4),
    ([2, -1, 8, 5.2], 2)
])
def test_maxvalue_valid(values, expected_result):
    result = utils.maxvalue(values)
    assert result == expected_result


@pytest.mark.parametrize("values", [
    (['a', 'b', 3]),
    ([9, '0', 2]),
    (['-1', 's', '2.2'])
])
def test_maxvalue_invalid(values):
    with pytest.raises(ValueError):
        utils.maxvalue(values)


@pytest.mark.parametrize("values, expected_result", [
    ([1, 2, 3], 0),
    ([9], 0),
    ([9, 3.2, 6.4, 7, 12], 1),
    ([2, -1, 8, 5.2], 1)
])
def test_minvalue_valid(values, expected_result):
    result = utils.minvalue(values)
    assert expected_result == result


@pytest.mark.parametrize("values", [
    (['a', 'b', 3]),
    ([9, '0', 2]),
    (['-1', 's', '2.2'])
])
def test_minvalue_invalid(values):
    with pytest.raises(ValueError):
        utils.minvalue(values)


@pytest.mark.parametrize("values, expected_result", [
    ([1, 2, 3], 2),
    ([9], 9),
    ([9, 3.2, 6.4, 7, 12], 7.5200000000000005),
    ([2, -1, 8, 5.2], 3.55)
])
def test_meanvalue_valid(values, expected_result):
    result = utils.meannvalue(values)
    assert result == expected_result


@pytest.mark.parametrize("values", [
    (['a', 'b', 3]),
    ([9, '0', 2]),
    (['-1', 's', '2.2'])
])
def test_minvalue_invalid(values):
    with pytest.raises(ValueError):
        utils.meannvalue(values)


@pytest.mark.parametrize("values, value, expected_result", [
    ([1.1, 1.1, 2, 3, 1.1, 3], 1.1, 3),
    (['Apple', 'Banana', 'Apple', 'Cucumber'], 'Banana', 1),
    (['Car', 'Bike', 'Bus', 'Tram', 'Scooter'], 'Plane', 0),
    ([-1, 2, 3, 12, 99], 6, 0)
])
def test_countvalue(values, value, expected_result):
    result = utils.countvalue(values, value)
    assert result == expected_result


def test_file_reader_valid():
    result = utils.file_reader(__file__.replace('\\', '/').rstrip('/test/test_util.py') + "t/data/Pollution-London Harlington.csv")
    assert type(result) == dict


def test_file_reader_invalid():
    with pytest.raises(FileNotFoundError):
        utils.file_reader("Here")


@pytest.mark.parametrize("number, expected_result", [
    ('1.1', 1.1),
    ('1', 1),
    ('-1', -1),
    ("one", "one")
])
def test_tryfloatcast(number, expected_result):
    result = utils.tryfloatcast(number)
    assert result == expected_result


def test_getdata():
    result = utils.get_data()
    assert type(result) == dict


@pytest.mark.parametrize("position, image, expected_neighbours",[
    (np.array([0, 0]), np.zeros([9, 9]), np.array([[0,1], [1,0], [1,1]])),
    (np.array([1, 1]), np.zeros([9, 9]), np.array([[1, 2],[2, 1],[2,2],[1,0],[0,1],[0,0],[2,0],[0,2]]))
])
def test_find_8_neighbours(position, image, expected_neighbours):
    result = utils.find_8_neighbours(position, image)
    assert (result == expected_neighbours).all()


@pytest.mark.parametrize("left_half, right_half, left_indexes, right_indexes, expected_result",[
    ([2], [9], [1], [0], ([9, 2], [0, 1])),
    ([12, 9, 8], [14, 2], [i for i in range(3)], [i + 3 for i in range(2)], ([14, 12, 9, 8, 2], [3, 0, 1, 2, 4]))
])
def test_merge_descending(left_half, right_half, left_indexes, right_indexes, expected_result):
    result = utils.merge_descending(left_half, right_half, left_indexes, right_indexes)
    assert result == expected_result


@pytest.mark.parametrize("items, items_indexes, expected_result", [
    ([8, 12, 3, 4, 2], [i for i in range(5)], ([12, 8, 4, 3, 2], [1, 0, 3, 2, 4])),
    ([6.2, 7, 9.3, 1.1], [i for i in range(4)], ([9.3, 7, 6.2, 1.1], [2, 1, 0, 3])),
    ([9], [0], ([9], [0]))
])
def test_merge_sort_descending(items, items_indexes, expected_result):
    result = utils.merge_sort_descending(items, items_indexes)
    assert result == expected_result
