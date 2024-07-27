"""
WHAT IT DOES:
* Merges 2 CSV files: medical.csv and persons.csv on ID
* Calculates BMI for each patient using BMI function
* Creates a patient record using PatientRecord class
* Records errors using error logging function

OUTPUTS:
* output/merged_data.csv
* logging/error_log.csv

AUTHOR: Sophie-Louise Courtney
LAST UPDATED: 27/07/2024
LANGUAGE: Python
"""

import pandas as pd
from datetime import datetime
from functions import calculate_bmi, log_error
from classes import PatientRecord

# Paths to the input CSV files
MEDICAL_CSV_PATH = 'input/medical.csv'
PERSONS_CSV_PATH = 'input/persons.csv'
OUTPUT_CSV_PATH = 'output/merged_data.csv'

def main():
    # Load the CSV files
    medical_df = pd.read_csv(MEDICAL_CSV_PATH)
    persons_df = pd.read_csv(PERSONS_CSV_PATH)
    
    # Merge the DataFrames on 'id'
    merged_df = pd.merge(medical_df, persons_df, on='id', how='left')
    
    # Process each row to create PatientRecord instances
    records = []
    for _, row in merged_df.iterrows():
        try:
            # Calculate BMI
            weight = row['weight'] if not pd.isna(row['weight']) else None
            height = row['height'] if not pd.isna(row['height']) else None
            bmi = calculate_bmi(weight, height) if weight and height else None
            
            # Create PatientRecord
            record = PatientRecord(
                ID=int(row['id']),
                FORENAME=row['forename'] if not pd.isna(row['forename']) else '',
                SURNAME=row['surname'] if not pd.isna(row['surname']) else '',
                DOB=datetime.strptime(row['date_of_birth'], '%Y-%m-%d').date() if not pd.isna(row['date_of_birth']) else None,
                SEX=row['sex'] if not pd.isna(row['sex']) else '',
                HEIGHT_CM=int(row['height']) if not pd.isna(row['height']) else None,
                WEIGHT_KG=int(row['weight']) if not pd.isna(row['weight']) else None,
                BMI=bmi,
                BP_LVL=row['blood_pressure'] if not pd.isna(row['blood_pressure']) else '',
                CHOL_LVL=int(row['cholestrol_lvl']) if not pd.isna(row['cholestrol_lvl']) else None,
                NOTES=row['Notes'] if not pd.isna(row['Notes']) else None
            )
            records.append(record)
        
        except Exception as e:
            log_error(int(row['id']), str(e))
    
    # Convert records to DataFrame
    output_df = pd.DataFrame([record.__dict__ for record in records])
    
    # Save to CSV
    output_df.to_csv(OUTPUT_CSV_PATH, index=False)

if __name__ == '__main__':
    main()
