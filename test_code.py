from cse163_utils import assert_equals
import data_processing as process

def test_code(la_crime_data, la_map):
    assert_equals(sorted(la_crime_data["AREA NAME"].unique()),
                  sorted(la_map["LON"].unique()))

def main():
    la_map = process.get_LAmap()
    la_crime_data = process.get_LAcrime_geodata(la_map)
    test_code(la_crime_data, la_map)
