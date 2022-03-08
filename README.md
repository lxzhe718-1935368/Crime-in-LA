# CSE 163 final project - Crime in LA
## How to run the code
1. First need to download all the data set:<br>
    - la map data: at https://geohub.lacity.org/datasets/lahub::lapd-divisions/about, click the download and choose Shapefile.<br>
    unzip all the file and put it in one folder. We will import .shp file but all other file is necessary Should be 206.2KB
    - la crime data: https://www.kaggle.com/hemil26/crime-in-los-angeles?select=crime_in_la.csv to download the csv file and unzip it
2. In the final_project.py, change the **Crime_FILE_PATH** where you download la crime csv data and **LA_FILE_PATH** to where you download la map .shp data. Those can be found at data_processing.py<br>
3. Use cse 163 environment so that all the package is install, more details in https://courses.cs.washington.edu/courses/cse163/software/<br>
    - Need to select the environment after cse 163 environment is being download. In vs code, use ctrl+shift+p and type **select interpreter**
    - Also use **pip install plotly** to install plotly packge. You can run it at juypter nootbook
4. To run test code, you need to have cse163_utils.py file in the same folder as test_code.py
5. Change **FIG_PATH** to where you want to store result graph in top of final_project.py

### IF you download the full holder I upload, thing you need to do is change **Crime_FILE_PATH** and **LA_FILE_PATH** to where you download the folder and set up environment correct