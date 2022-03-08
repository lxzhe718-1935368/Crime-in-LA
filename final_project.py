"""
This file is the implemention of cse 163 final project.
This file is runable part of the project, 
"""
import data_processing as process
import matplotlib.pyplot as plt
import os
import numpy as np
import seaborn as sns
import plotly.express as px

FIG_PATH = "C:/Users/718/Desktop/cse163/result_img/"

def plot_crime_count(la_crime_data):
    """
    plot the crime count vs time graph,
    save the figure as png at given dir with name:"crime_count_Vs_time.png"
    """
    whole_time, all_time = process.filter_time_data(la_crime_data)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(25,17))
    # plot crime happened only at whole time
    ax1.set_xticks(np.arange(0, 2400, 100))
    ax1.tick_params(labelsize= 20)
    ax1.plot(whole_time["TIME OCC"], whole_time["count"], "--bo")
    ax1.set_xlabel("Time(in 24H scale)", fontsize=26)
    ax1.set_ylabel("Crime count", fontsize=26)
    ax1.set_title("Crime Aappend At Each Time", fontsize=35)

    # plot all crime happened
    ax2.set_xticks(np.arange(0, 2400, 100))
    graph = sns.histplot(data=all_time, x="TIME OCC", weights="count",
                 kde=True, binwidth=100, binrange=(0,2400), ax=ax2)
    graph.axes.set_title("Count of crime respect to time",fontsize=35)
    graph.set_xlabel("Time",fontsize=26)
    graph.set_ylabel("Count of crime",fontsize=26)
    graph.tick_params(labelsize=20)
    plt.tight_layout(pad=1.5)
    fig.savefig(os.path.join(FIG_PATH, "Crime_Vs_time.png"))



def crime_in_map(la_crime_data, la_map):
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
    graph = sns.histplot(data=location_count, y="Premis Desc", weights="count", ax=ax3)
    graph.tick_params(labelsize=26)
    graph.set_xlabel("count",fontsize=26)
    graph.set_ylabel("location that crime took place",fontsize=26)
    ax3.set_title("Top 15 places that crime took place", fontsize=35)
    fig.savefig(os.path.join(FIG_PATH, "crime_in_map.png"))
    # plot more detail of graph in ax2, which is crime density in la
    figure = px.choropleth_mapbox(crime_count, geojson=crime_count.geometry,
                locations=crime_count.index,
                mapbox_style="open-street-map", color="count",
                opacity=0.5, hover_data=["count", "AREA NAME"],
                center={"lat": 34.0522, "lon": -118.2437},
                title="Area Crime Distribution in Detail")
    figure.write_html(os.path.join(FIG_PATH, "details_crime_Distribute.html"))



def crime_type_analysis(la_crime_data):
    """
    Types of Crimes at different Premises,
    gives more details on how crime distribute in different place
    """
    crime_type = process.crime_type_data(la_crime_data)
    fig = px.bar(crime_type, x="size", y="Premis Desc",
                 color="Crm Cd Desc", text_auto=True)
    fig.write_html(os.path.join(FIG_PATH, "crime_type_analysis.html"))


def wapon_used(la_crime_data, la_map):
    wapon_data = process.wapon_data_process(la_crime_data)
    plt.figure(figsize=(20, 15))
    graph = sns.histplot(data=wapon_data, y="Weapon Desc", weights="count", color="purple")
    graph.tick_params(labelsize=26)
    graph.set_xlabel("count",fontsize=26)
    graph.set_ylabel("location that crime took place",fontsize=26)
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
    plot strong-arm and hand gan distribution in LA map
    """
    wapon_arm, wapon_pistol = process.wapon_map_process(la_crime_data, la_map)
    fig, ax = plt.subplots(2, figsize=(20, 15))
    la_map.plot(ax=ax[0], color="red")
    wapon_arm.plot(column="count", ax=ax[0], legend=True)
    la_map.plot(ax=ax[1], color="red")
    wapon_pistol.plot(column="count", ax=ax[1], legend=True)
    ax[0].set_title("Distribution of crime invoded strong arm", fontsize=30)
    ax[1].set_title("Distribution of crime invoded pistol", fontsize=30)
    fig.savefig(os.path.join(FIG_PATH, "armed_crime_LA.png"))


def victims_analysis(la_crime_data):
    victims = process.victims_data(la_crime_data)
    fig = px.histogram(victims, x="Vict Age", y="count",
                color="Vict Sex", barmode="group",
                height=400)
    fig.update_layout(title_text="Count Crime by Victims Sex",
                    xaxis = dict(
                        tickmode = 'array',
                        tickvals = list(range(0, 100, 10))))
    fig.write_html(os.path.join(FIG_PATH, "victims_analysis.html"))


def main():
    la_map = process.get_LAmap()
    la_crime_data = process.get_LAcrime_geodata(la_map)
    plot_crime_count(la_crime_data)
    crime_in_map(la_crime_data, la_map)
    crime_type_analysis(la_crime_data)
    wapon_used(la_crime_data, la_map)
    wapon_in_map(la_crime_data, la_map)
    victims_analysis(la_crime_data)

if __name__ == '__main__':
    main()