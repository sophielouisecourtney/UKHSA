"""
WHAT IT DOES:
* Creates a dummy dataset of randomly generated health data to use in techincal exercise
* Creates a data dictionary showing which columns contain disclosive information
* Creates a schema for the final data to use when creating the ETL pipeline

OUTPUTS:
* input/dummy_health_data.csv
* input/data_dictionary.csv
* input/schema.csv

AUTHOR: Sophie-Louise Courtney
LAST UPDATED: 27/07/2024
LANGUAGE: Python
"""
## 0. Inputs ##
import pandas as pd
import numpy as np

## 1. Create Random-ness ##
# Set random seed for reproducibility while testing
np.random.seed(12)

# Helper function to generate random dates
def random_dates(start, end, n):
    start_u = start.value // 10**9
    end_u = end.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

# Helper function to create a mismatch in ids of 95%
def create_mismatch(df1, df2, match_ratio=0.95):
    # Calculate the number of matching ids
    num_matches = int(len(df1) * match_ratio)
    
    # Shuffle and split ids for mismatch
    shuffled_ids = np.random.permutation(df1['id'].values)
    match_ids = shuffled_ids[:num_matches]
    mismatch_ids = shuffled_ids[num_matches:]
    
    # Ensure there are enough mismatch ids to replace
    extra_ids = np.random.choice(df1['id'].unique(), size=len(mismatch_ids), replace=False)
    
    # Update df2 with mismatched ids
    df2.loc[df2.index.isin(df1.index[:len(mismatch_ids)]), 'id'] = extra_ids
    
    return df1, df2

## 2. Generate Data
# Generate initial data
data = {
    'id': np.random.randint(100000, 999999, size=100).astype(str),
    'forename': np.random.choice(['Alice', 'Bob', 'Charlie', 'David', 'Eva', 'Grace', 'Henry', 'Isabella', 'Jack', 'Liam'], 100),
    'surname': np.random.choice(['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor'], 100),
    'date_of_birth': random_dates(pd.to_datetime('1930-01-01'), pd.to_datetime('2006-12-31'), 100),  # Keep as datetime initially
    'sex': np.random.choice(['M', 'F'], 100),
    'age': np.random.randint(18, 90, size=100),
    'height': np.random.randint(150, 200, size=100),
    'weight': np.random.randint(50, 100, size=100),
    'blood_pressure': np.random.choice(['120/80', '130/85', '140/90', '110/70', '160/100'], 100),
    'Notes': np.random.choice(['', 'Needs follow-up', 'Regular check-up', 'Medication prescribed', ''], 100),
    'cholestrol_lvl': np.random.randint(150, 300, size=100),
    }

# Create DataFrames
df_persons = pd.DataFrame({
    'id': data['id'],
    'forename': data['forename'],
    'surname': data['surname'],
    'date_of_birth': data['date_of_birth'], 
    'sex': data['sex']
})

df_medical = pd.DataFrame({
    'id': data['id'],
    'age': data['age'],
    'height': data['height'],
    'weight': data['weight'],
    'blood_pressure': data['blood_pressure'],
    'cholestrol_lvl': data['cholestrol_lvl'],
    'Notes': data['Notes']
})

# Convert date_of_birth column to date format
df_persons['date_of_birth'] = df_persons['date_of_birth'].dt.date

## 3. Simulate data errors ##
# Introduce missingness of 5%
def introduce_missingness(df, col, missing_ratio=0.05):
    if col in df.columns:
        if df[col].dtype == 'bool':
            df.loc[df.sample(frac=missing_ratio).index, col] = pd.NA
        else:
            df.loc[df.sample(frac=missing_ratio).index, col] = np.nan

# Apply missingness to columns that exist in each DataFrame
for col in ['forename', 'surname', 'date_of_birth', 'sex']:
    introduce_missingness(df_persons, col)

for col in ['age', 'height', 'weight', 'blood_pressure', 'Notes']:
    introduce_missingness(df_medical, col)

# Create mismatched ids
df_persons, df_medical = create_mismatch(df_persons, df_medical)

# Introduce some messiness in the 'Notes' column
df_medical.loc[df_medical.sample(frac=0.05).index, 'Notes'] = 'irregular entry'

## 4. Produce data dictionaries to show disclosive columns ##
# Create Data Dictionary for 'persons' table
data_dictionary_persons = {
    'Variable': ['id', 'forename', 'surname', 'date_of_birth', 'sex'],
    'Description': [
        'Unique identifier for each entry',
        'First name of the individual',
        'Last name of the individual',
        'Date of birth of the individual',
        'Birth-assigned sex of the individual'
    ],
    'Disclosive': [True, True, True, True, True]
}

df_data_dictionary_persons = pd.DataFrame(data_dictionary_persons)

# Create Data Dictionary for 'medical' table
data_dictionary_medical = {
    'Variable': ['id', 'age', 'height', 'weight', 'blood_pressure', 'Notes'],
    'Description': [
        'Unique identifier for each entry',
        'age of the individual',
        'height of the individual in centimeters',
        'weight of the individual in kilograms',
        'Blood pressure readings of the individual',
        'Additional notes with some messiness'
    ],
    'Disclosive': [True, False, False, False, False, True]
}

df_data_dictionary_medical = pd.DataFrame(data_dictionary_medical)

## 5. Save DataFrames and Data Dictionaries to CSV ##
# Set path locations
csv_persons_path = 'input/persons.csv'
csv_medical_path = 'input/medical.csv'
data_dictionary_persons_path = 'input/persons_data_dicitonary.csv'
data_dictionary_medical_path = 'input/medical_data_dictionary.csv'

#Save CSVs
df_persons.to_csv(csv_persons_path, index=False)
df_medical.to_csv(csv_medical_path, index=False)
df_data_dictionary_persons.to_csv(data_dictionary_persons_path, index=False)
df_data_dictionary_medical.to_csv(data_dictionary_medical_path, index=False)
