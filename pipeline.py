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
# Imports 
import pandas as pd
from datetime import datetime
from functions import calculate_bmi, log_error
from classes import PatientRecord

# Paths to the input CSV files
MEDICAL_CSV_PATH = 'input/medical.csv'
PERSONS_CSV_PATH = 'input/persons.csv'
OUTPUT_CSV_PATH = 'output/merged_data.csv'
UNMATCHED_CSV_PATH = 'output/unmatched_ids.csv'

def main():
    # Load the CSV files
    medical_df = pd.read_csv(MEDICAL_CSV_PATH)
    persons_df = pd.read_csv(PERSONS_CSV_PATH)
    
    # Get unique IDs from both files
    medical_ids = set(medical_df['id'].unique())
    persons_ids = set(persons_df['id'].unique())
    
    # Find unmatched IDs
    unmatched_in_medical = list(medical_ids - persons_ids)
    unmatched_in_persons = list(persons_ids - medical_ids)
    total_unmatched = unmatched_in_persons + unmatched_in_medical
  
    # Combine unmatched IDs into a DataFrame
    unmatched_df = pd.DataFrame({
        'ID': total_unmatched,
    })
    
    # Save unmatched IDs to CSV
    unmatched_df.to_csv(UNMATCHED_CSV_PATH, index=False)
    
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
                FORENAME=row['forename'],
                SURNAME=row['surname'],
                DOB=datetime.strptime(row['date_of_birth'], '%Y-%m-%d').date() if not pd.isna(row['date_of_birth']) else None,
                SEX=row['sex'],
                HEIGHT_CM=row['height'],
                WEIGHT_KG=row['weight'],
                BMI=bmi,
                BP_LVL=row['blood_pressure'],
                CHOL_LVL=row['cholestrol_lvl'],
                NOTES=row['Notes']
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
