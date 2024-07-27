import pandas as pd

def test_unique_ids_handling():
    # Load the input CSV files
    medical_df = pd.read_csv('input/medical.csv')
    persons_df = pd.read_csv('input/persons.csv')
    
    # Extract unique IDs from input files
    medical_ids = set(medical_df['id'].unique())
    persons_ids = set(persons_df['id'].unique())
    all_ids = medical_ids.union(persons_ids)
    
    # Load the output CSV files
    merged_df = pd.read_csv('output/merged_data.csv')
    error_log_df = pd.read_csv('output/error_log.csv')
    unmatched_df = pd.read_csv('output/unmatched_ids.csv')
    
    # Extract unique IDs from output files
    merged_ids = set(merged_df['ID'].unique())
    unmatched_ids = set(unmatched_df['ID'].unique())
    error_log_ids = set(error_log_df['ID'].unique())
    
    # Combine IDs from output files
    combined_output_ids = merged_ids.union(error_log_ids).union(unmatched_ids)
    
    # Check that each ID appears exactly once across the three output files
    assert len(all_ids) == len(combined_output_ids), "Mismatch in the total number of unique IDs between input and output files."
    assert all_ids == combined_output_ids, "Some IDs are missing or duplicated in the output files."

    print("Test passed! Each ID appears exactly once in one of the output files.")

# Run the test
test_unique_ids_handling()
