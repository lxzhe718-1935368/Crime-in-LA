from cse163_utils import assert_equals
import data_processing as process


def test_area_name(la_crime_data, la_map):
    """
    takes la crime, la_map data
    test if processed data gives correct result as we expect,
    test if area name after change is match in la map and la crime data
    """
    assert_equals(sorted(la_crime_data["AREA NAME"].unique()),
                  sorted(la_map["APREC"].unique()))


def test_time(la_crime_data):
    """
    take head 5 of la_crime_data
    test if processed data gives correct result as we expect,
    test if time after change is correctly in int
    """
    whole_time, all_time = process.filter_time_data(la_crime_data)
    assert_equals([], list(whole_time["TIME OCC"]))
    assert_equals([30, 330, 415, 1730, 2230], list(all_time["TIME OCC"]))


def test_crime_count(la_crime_data, la_map):
    """
    take head 10 of la_crime_data and la map
    test if processed data gives correct result as we expect,
    test if crime count is correct
    """
    crime, location = process.join_map_crime(la_crime_data, la_map)
    assert_equals(["mission", "n hollywood", "southwest", "central"],
                  list(crime["APREC"]))
    assert_equals([1, 1, 1, 7], list(crime["count"]))
    assert_equals([2, 1, 1, 1, 1, 1, 1, 1, 1], list(location["count"]))


def main():
    la_map = process.get_LAmap()
    la_crime_data = process.get_LAcrime_geodata(la_map)
    test_area_name(la_crime_data, la_map)
    test_crime_count(la_crime_data.head(n=10), la_map)


if __name__ == '__main__':
    main()