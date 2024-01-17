import pytest
import intelligence

def test_find_red_pixels():
    result = intelligence.find_red_pixels('map.png', 100, 50)
    assert result.shape == (1140, 1053, 3)

def test_find_cyan_pixels():
    result = intelligence.find_cyan_pixels('map.png', 100, 50)
    assert result.shape == (1140, 1053, 3)

@pytest.mark.parametrize("IMG, expected_result", [
    (intelligence.find_red_pixels('map.png'), (1140, 1053) ),
    (intelligence.find_cyan_pixels('map.png'), (1140, 1053) )
])
def test_detect_connected_components(IMG, expected_result):
    result = intelligence.detect_connected_components(IMG)
    assert result.shape == expected_result

@pytest.mark.parametrize("mark, expected_result", [
    (intelligence.detect_connected_components(intelligence.find_red_pixels('map.png')), None ),
    (intelligence.detect_connected_components(intelligence.find_cyan_pixels('map.png')), None )
])
def test_detect_connected_components_sorted(mark, expected_result):
    result = intelligence.detect_connected_components_sorted(mark)
    assert result == expected_result

