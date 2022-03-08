"""
Xiaozhe(Jack) Liu, Jieyun(Ellie) Xie
2022/3/08
This file is a part of implemention of cse 163 final project.
This file is data processing part, do not have main()
provide method that process la crime and la map data
in order to let final_project.py can use them to make data analysis.
"""
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
Crime_FILE_PATH = "C:/Users/718/Desktop/cse163/crime_in_la.csv"
LA_FILE_PATH = "C:/Users/718/Desktop/cse163/LAPD_map/LAPD_Divisions.shp"


def get_LAcrime_geodata(la_map):
    """
    process original la crime data and return as geodata set,
    took la_map to make sure their .crs location is same.
    Use return data in all the part of project.
    Ignore all the row that lat is 0.0 (did not provide location)
    Sometimes, we will use this data as dataFrame instead of geoDataFrame
    """
    la_crime_data = pd.read_csv(Crime_FILE_PATH)
    la_crime_data = la_crime_data.loc[la_crime_data["LAT"] != 0]
    # Add count column with value 1 help to count occurrence when use dissolve
    la_crime_data["count"] = 1
    geometry = [Point(xy) for xy in zip(la_crime_data['LON'],
                                        la_crime_data['LAT'])]
    la_crime_data.crs = la_map.crs
    # convert time colume to int so make it easier to use later
    la_crime_data["TIME OCC"] = la_crime_data["TIME OCC"]\
                                .str.replace(":", "").astype(int)
    la_crime_data["AREA NAME"] = la_crime_data["AREA NAME"].str.lower()
    return gpd.GeoDataFrame(la_crime_data, geometry=geometry)

def get_LAmap():
    """
    Process la map data that make area name match with
    la crime data. Return after process data.
    Make area name is consist,
    we can join la map data to crime data after processing.
    We use it for all the part of project.
    """
    la_map = gpd.read_file(LA_FILE_PATH)
    la_map["APREC"] = la_map["APREC"].str.lower()
    la_map["APREC"] = la_map["APREC"].replace(
        ["north hollywood", "west los angeles"], ["n hollywood", "west la"])
    return la_map

def filter_time_data(la_crime_data):
    """
    Helper method for plot_crime_count.
    take la crime data and
    return dataFrame data that filtered la crime data to only crime
    happend at whole time(1AM, 2AM .ect) and
    dataFrame that contain all the happened crime
    """
    process_data = la_crime_data.groupby("TIME OCC", as_index=False)["count"].sum()
    process_data = process_data[["TIME OCC", "count"]]
    return (process_data[(process_data["TIME OCC"] % 100 == 0)],
            process_data)


def join_map_crime(la_crime_data, la_map):
    """
    Helper method for crime_in_map,
    Take both la crime data and la map data,
    return geoData that join those data together with
    count of crime, and processed data for plot top 15 crime took place.
    """
    crime_count = la_crime_data.groupby("AREA NAME", as_index=False)["count"].sum()
    # Choice any other column will work because we use count
    crime_count = crime_count[["AREA NAME", "count"]]
    # put la_map in left will keep data in geoData
    # I try to use sjoint with dissolve(instead of groupby)
    # but it took so long to run the dissolve funciton
    # so I come up this alternate way to process data
    location_count = la_crime_data.groupby("Premis Desc",
                                           as_index=False)["count"].sum()
    location_count.sort_values(by=["count"], ascending=False, inplace=True)
    location_count = location_count.head(n=15)
    # put la_map in left keep merge return geoDataframe
    # since we use grouby instead of disslove, we can't use sjoin here
    merged = la_map.merge(crime_count, left_on="APREC", right_on="AREA NAME", how="inner")
    return merged, location_count


def crime_type_data(la_crime_data):
    """
    Helper method for crime_type_analysis()
    Takes la crime data return dataFrame that use to plot the
    relationship. The size > 3000 simply control Premises shows in y axis.
    because it filter out premises that have low crime count.
    """
    # select top happend crime type
    check = la_crime_data.groupby("Crm Cd Desc", as_index=False)["count"].sum()
    check.sort_values(by=["count"], ascending=False, inplace=True)
    check = check["Crm Cd Desc"].head(n=7)

    crime_type_data = la_crime_data[la_crime_data["Crm Cd Desc"].isin(check.tolist())]
    crime_type_data = crime_type_data.groupby(["Crm Cd Desc", "Premis Desc"],
                                            as_index=False).size()
    return crime_type_data[crime_type_data["size"] > 3000]


def wapon_data_process(la_crime_data):
    """
    Helper method for wapon_used()
    Takes la crime data and return dataFrame that contains
    top 10 wapon that involved in crime
    """
    wapon_data = la_crime_data[la_crime_data["Weapon Used Cd"] != 500.0]
    wapon_data = wapon_data.groupby("Weapon Desc", as_index=False)["count"].sum()
    wapon_data.sort_values(by=["count"], ascending=False, inplace=True)
    return wapon_data.head(n=10)

def wapon_map_process(la_crime_data, la_map):
    """
    Helper method for wapon_in_map()
    Takes la crime and la map data and
    return geodataFrame that contains processed data about
    crime that involve strong arm and crime that involve pistol
    """
    # data involved strong arm
    wapon_strong_arm = la_crime_data[la_crime_data["Weapon Desc"] ==
        "STRONG-ARM (HANDS, FIST, FEET OR BODILY FORCE)"]
    wapon_strong_arm = wapon_strong_arm.groupby("AREA NAME",
                                                as_index=False)["count"].sum()
    wapon_strong_arm = la_map.merge(wapon_strong_arm, left_on="APREC",
                                    right_on="AREA NAME", how="inner")
    # data involved pistol
    wapon_pistol = la_crime_data[la_crime_data["Weapon Desc"].isin(
                                ["HAND GUN", "SEMI-AUTOMATIC PISTOL"])]
    wapon_pistol = wapon_pistol.groupby("AREA NAME", as_index=False)["count"].sum()
    wapon_pistol = la_map.merge(wapon_pistol, left_on="APREC",
                                right_on="AREA NAME", how="inner")
    return wapon_strong_arm, wapon_pistol


def victims_data(la_crime_data):
    """
    Helper method for victims_analysis()
    Takes la crime and return filtered geoData contains valid information
    about victims's sex and age. Only use it as dataFrame.
    """
    victims = la_crime_data[(la_crime_data["Vict Sex"] != "X") &
                            (la_crime_data["Vict Age"] > 0) &
                            (la_crime_data["Vict Sex"] != "H")]
    return victims
