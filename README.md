# UKHSA_tech_assessment
This codebase is for technical assessment for the Data Engineer role at UKSHA. The codebase includes the production of dummy data, data validation, data manipulation, and data handling. **NOTE: THIS IS ENTIRELY DUMMY DATA - NO REAL MEDICAL RECORDS ARE USED IN THIS EXERCISE!** 

## Desk Instructions:
* *(Optional)* Navigate to **input -> data_generator.py** and input a new random number into line 22. Then run the script to generate a dataset. *Skip this step if you just want to keep running the same dataset repeatedly*
* Run the pipeline script **pipeline.py** to generate matched medical records
* Review error logs (**output -> error_log.csv**) to see why some medical records have been rejected
* Run **tests.py** to perform QA checks


## input
### data_generator.py
A standalone pipeline for creating dummy data which can be processed for the techincal task. *I have done this as I wanted to show some data linkage in my pipeline, as well as control the amount of missingness of the data. It also functions as a way to create a data dictionary to show which columns are disclosive*

The data generator generates the following files used within the technical task:
* ### medical.csv
* ### medical_data_dictionary.csv
* ### persons.csv
* ### persons_data_dictionary.csv

## output
### error_log.csv
Shows which ID numbers were unable to be processed successfully and why (*NOTE These are examples of data errors, not errors caused by bad code!*)

### merged_data.csv
Data which has been successfully linked by ID between the 2 input CSVs

### unmatched_data.csv
A list of ID numbers that were unable to be matched due to a missing matching ID in either the medical.csv or persons.csv file (*This is a simulated error*)

## planning
### schema_plan.png
A planned schema flowchart

### JIRA_tasks.jpg
A plan of tasks which I made on paper but would usually make in JIRA - for your interest!

## classes.py
A dataclass object for PatientRecord based on the schema_plan.

## functions.py
### log_error
Creates the error log in the output folder

### calculate_bmi
Data manipulation to calculate a patient's BMI based on their height and weight.

## pipeline.py
The main data pipeline, which takes matches the 2 input csvs, matches them, and creates the output files, executing the classes and functions I have written in the process.

## tests.py
**test_unique_ids_handling** Tests that all IDs within the data only appear once within the output files - as there should be no overlap between ID with match, do not match, and error

## extras:
### hashing.py
When it comes to security, the hope would be that this data was processed and stored within a limited access area with password protection and encryption, but to show a way to allow more users access to sensitive data I have also included a data hashing function with an example which can be run via extras
### clooud_config.py
I do not currently have access to a full premium AWS account but I do have experience with integrating pipelines with cloud services, and running code via Airflow scheduling. I have included example snippets of config code within this file, but decided not to integrate it with the main pipeline to keep the original local version running smoothly.
