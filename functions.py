import os
import csv
from datetime import datetime
from typing import Optional

ERROR_LOG_PATH = 'logging/error_log.csv'

def log_error(id: int, error_message: str):
    # Ensure the logging directory exists
    os.makedirs(os.path.dirname(ERROR_LOG_PATH), exist_ok=True)
    
    # Open the CSV file in append mode
    with open(ERROR_LOG_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the header if the file is new
        if os.stat(ERROR_LOG_PATH).st_size == 0:
            writer.writerow(['date', 'time', 'ID', 'error_message'])
        # Write the error entry
        now = datetime.now()
        writer.writerow([now.date(), now.time().strftime('%H:%M:%S'), id, error_message])


## Calculate BMI using Height and Weight where possible
def calculate_bmi(weight: Optional[float], height: Optional[float]) -> Optional[int]:
    if weight is not None and height is not None and weight > 0 and height > 0:
        bmi = weight / ((height / 100) ** 2) # BMI = weight (kg)/height (m^2)
        return round(bmi)
    return None
