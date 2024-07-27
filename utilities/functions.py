# functions/functions.py
from typing import Optional
from datetime import datetime
import csv
import os

## Error Logging ##
ERROR_LOG_PATH = 'logging/error_log.csv'

def log_error(id: int, error_message: str):
    file_exists = os.path.isfile(ERROR_LOG_PATH)
    with open(ERROR_LOG_PATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['date', 'time', 'ID', 'error_message'])
        now = datetime.now()
        writer.writerow([now.date(), now.time().strftime('%H:%M:%S'), id, error_message])

## Calculate BMI using Height and Weight where possible
def calculate_bmi(weight: Optional[float], height: Optional[float]) -> Optional[int]:
    if weight is not None and height is not None and weight > 0 and height > 0:
        bmi = weight / ((height / 100) ** 2) # BMI = weight (kg)/height (m^2)
        return round(bmi)
    return None
