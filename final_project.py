"""
Xiaozhe(Jack) Liu, Jieyun(Ellie) Xie
2022/3/08
This file is a part of implemention of cse 163 final project.
This file is runable part of the project,
provide some data analysis method to investgate
crime happend in LA from 2020 to now.
Generate and save some graphs in local folder,
read README to see more details about how to run this code.
"""
import data_processing as process
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns
import plotly.express as px

FIG_PATH = "./result_img/"


def plot_crime_count(la_crime_data):
    """
    takes la crime data and genetate graph of
    relationship between crime count and time
    save the figure as png at given dir with name:"crime_count_Vs_time.png"
    """
    whole_time, all_time = process.filter_time_data(la_crime_data)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(25, 17))
    # plot crime happened only at whole time
    ax1.set_xticks(np.arange(0, 2400, 100))
    ax1.tick_params(labelsize=20)
    ax1.plot(whole_time["TIME OCC"], whole_time["count"], "--bo")
    ax1.set_xlabel("Time(in 24H scale)", fontsize=26)
    ax1.set_ylabel("Crime count", fontsize=26)
    ax1.set_title("Crime Aappend At Each Time", fontsize=35)

    # plot all crime happened
    ax2.set_xticks(np.arange(0, 2400, 100))
    graph = sns.histplot(data=all_time, x="TIME OCC", weights="count",
                         kde=True, binwidth=100, binrange=(0, 2400), ax=ax2)
    graph.axes.set_title("Count of crime respect to time", fontsize=35)
    graph.set_xlabel("Time", fontsize=26)
    graph.set_ylabel("Count of crime", fontsize=26)
    graph.tick_params(labelsize=20)
    plt.tight_layout(pad=1.5)
    fig.savefig(os.path.join(FIG_PATH, "Crime_Vs_time.png"))


def crime_in_map(la_crime_data, la_map):
    """
    takes la crime and la map data,
    genetate 2 graph of how crime distribut in LA
    save one figure as png at given dir with name:"crime_in_map.png",
    one in HTML "details_crime_Distribute.html"
    which allow you hover mouse in the graph to see more detail.
    """
    crime_count, location_count = process.join_map_crime(la_crime_data, la_map)

    fig = plt.figure(figsize=(30, 25), constrained_layout=True)
    spec = fig.add_gridspec(2, 2)
    # set figure place.
    ax1 = fig.add_subplot(spec[0, 0])
    ax2 = fig.add_subplot(spec[0, 1])
    ax3 = fig.add_subplot(spec[1, :])
    # do not need axis for map graph
    ax1.axis('off')
    ax2.axis('off')
    # ax1 shows every crime happened in la
    la_map.plot(ax=ax1)
    la_crime_data.plot(ax=ax1, color="red")
    ax1.set_title("Overall Crime Happened In LA", fontsize=35)
    # ax2 shows how crime distribute in different area
    la_map.plot(ax=ax2, color="#EEEEEE")
    crime_count.plot(ax=ax2, column="count", legend=True)
    ax2.set_title("Area Crime Distribution", fontsize=35)
    # ax3 shows top 15 of crime happened in different location.
    graph = sns.histplot(data=location_count, y="Premis Desc",
                         weights="count", ax=ax3)
    graph.tick_params(labelsize=26)
    graph.set_xlabel("count", fontsize=26)
    graph.set_ylabel("location that crime took place", fontsize=26)
    ax3.set_title("Top 15 places that crime took place", fontsize=35)
    fig.savefig(os.path.join(FIG_PATH, "crime_in_map.png"))
    # plot more detail of graph in ax2, which is crime density in la
    figure = px.choropleth_mapbox(crime_count, geojson=crime_count.geometry,
                                  locations=crime_count.index,
                                  mapbox_style="open-street-map",
                                  color="count", opacity=0.5,
                                  hover_data=["count", "AREA NAME"],
                                  center={"lat": 34.0522, "lon": -118.2437},
                                  title="Area Crime Distribution in Detail")
    figure.write_html(os.path.join(FIG_PATH, "details_crime_Distribute.html"))


def crime_type_analysis(la_crime_data):
    """
    takes la crime data
    genetate a graph about what type of crimes happened in different location.
    save figure in HTML in "crime_type_analysis.html"
    which allow you hover mouse in the graph to see more detail.
    """
    crime_type = process.crime_type_data(la_crime_data)
    fig = px.bar(crime_type, x="size", y="Premis Desc",
                 color="Crm Cd Desc", text_auto=True)
    fig.write_html(os.path.join(FIG_PATH, "crime_type_analysis.html"))


def wapon_used(la_crime_data):
    """
    take la crime data
    genetate a graph about how wapon involved in crime
    save one figure as png at given dir with name:"wapon_use_analysis.png",
    """
    wapon_data = process.wapon_data_process(la_crime_data)
    plt.figure(figsize=(20, 15))
    graph = sns.histplot(data=wapon_data, y="Weapon Desc",
                         weights="count", color="purple")
    graph.tick_params(labelsize=26)
    graph.set_xlabel("count", fontsize=26)
    graph.set_ylabel("location that crime took place", fontsize=26)
    # add value of each histogram
    labels = [f" ({i})" for i in wapon_data["count"].tolist()]
    rects = graph.patches
    for rect, label in zip(rects, labels):
        graph.text(
            0, rect.get_y() + (rect.get_height() / 2 + 0.1), label,
            fontsize="26")
    plt.title("Count of Incidents and Weapon Description", fontsize=30)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_PATH, "wapon_use_analysis.png"))


def wapon_in_map(la_crime_data, la_map):
    """
    takes la crime and la map data
    genetate a graph about how strong arm and pistol involved in crimes
    save figure in HTML in "wapon_involved.html"
    which allow you hover mouse in the graph to see more detail.
    """
    # fig_arm_title help to reduce length in mapbox()
    fig_arm_title = "Distribution of crime invoded strong arm"
    wapon_arm, wapon_pistol = process.wapon_map_process(la_crime_data, la_map)
    fig_arm = px.choropleth_mapbox(wapon_arm,
                                   geojson=wapon_arm.geometry,
                                   locations=wapon_arm.index,
                                   mapbox_style="carto-positron", zoom=9,
                                   color="count", height=700, opacity=0.7,
                                   hover_data=["count", "AREA NAME"],
                                   center={"lat": 34.0522, "lon": -118.2437},
                                   title=fig_arm_title)
    # fig_pistol_title help to reduce length in mapbox()
    fig_pistol_title = "Distribution of crime invoded strong arm"
    fig_pistol = px.choropleth_mapbox(wapon_pistol,
                                      geojson=wapon_pistol.geometry,
                                      locations=wapon_pistol.index, height=700,
                                      mapbox_style="carto-positron",
                                      color="count", opacity=0.7, zoom=9,
                                      hover_data=["count", "AREA NAME"],
                                      center={"lat": 34.0522,
                                              "lon": -118.2437},
                                      title=fig_pistol_title)
    with open(os.path.join(FIG_PATH, "wapon_involved.html"), "w") as f:
        f.write(fig_pistol.to_html(full_html=False, include_plotlyjs='cdn'))
        f.write(fig_arm.to_html(full_html=False, include_plotlyjs='cdn'))


def victims_analysis(la_crime_data):
    """
    takes la crime
    genetate a graph about victims's age and sex
    save figure in HTML in "wapon_involved.html"
    which allow you hover mouse in the graph to see more detail.
    """
    victims = process.victims_data(la_crime_data)
    fig = px.histogram(victims, x="Vict Age", y="count",
                       color="Vict Sex", barmode="group",
                       height=800)
    fig.update_layout(title_text="Count Crime by Victims Sex",
                      xaxis=dict(
                        tickmode='array',
                        tickvals=list(range(0, 100, 10))))
    fig.write_html(os.path.join(FIG_PATH, "victims_analysis.html"))


def main():
    la_map = process.get_LAmap()
    la_crime_data = process.get_LAcrime_geodata(la_map)
    plot_crime_count(la_crime_data)
    crime_in_map(la_crime_data, la_map)
    crime_type_analysis(la_crime_data)
    wapon_used(la_crime_data)
    wapon_in_map(la_crime_data, la_map)
    victims_analysis(la_crime_data)


if __name__ == '__main__':
    main()