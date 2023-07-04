# MemoryDiary

The GoaL:

We have data files from a clinical interventional trial of PTSD patients, in which every patient is required to give a daily report of his intrusive memories and flashbacks via Qualtrics questionnaire while going through a five week treatment.
Our project allows the user to load that data file, insert the 5 treatment sessions dates and receive an analysis and visualizations of the data. 



Project Contents:

Main -> The key files of the project

errors.py - error file to be parsed when errors occure
flow_control.py - main hub file, controls flow of program executing all steps of the program in correct manner
requirements.txt - pip requirements for occasions where a new device runs the MemoryDiary
ui.py- The UI of the project, this file consists of architecture and functions that enable the quick and easy analysis of patient data

logics -> back-end files required for functioning of the MemoryDiary

__init__.py - initiallize project
excel_outputs.py - file that synthesizes a patient file and saves two separate organized data files 
filter_data.py- python file that synthesizes a patient file, cleans and orders it for later analysis and visualization
utils.py - python file responsible for code that creates unique id's to all files created from the analysis (output files 1 pdf, 2 excel)
validators.py - python file to validate inputs in ui so that analysis can occur and is functional
visualizations.py - python file containing code specifying graph instructions to visualize the filtered data from _filter_data

tests -> various tests for different components of the project

intrusions.xlsx - mock data
filtered_data_tests - tests for the filtering of the data
validators_test.py - test for the validation phases


How to Use the MemoryDiary:

1. run UI via IDE or shortcut
2. browse for patient data and upload file (xlsx,csv)
3. select output folder for output files after data manipulation and visualization
4. choose dates from list which correspond to patient treatment dates
5. press 'analyze' button
6. A window will open showing the graphs depicting the data
7. 2 excel files and a pdf file will be created in the chosen folder destination


Things to make sure before running the MemoryDiary:

1. make sure your file is an excel or csv
2. make sure the dates of treatment are valid and relate to the specific patient
3. make sure you have all libraries and packages needed for running the program









