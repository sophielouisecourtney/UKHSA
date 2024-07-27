from dataclasses import dataclass
from typing import Optional
from datetime import date

@dataclass
class PatientRecord:
    ID: int
    FORENAME: str
    SURNAME: str
    DOB: date
    SEX: str
    HEIGHT_CM: float
    WEIGHT_KG: float
    BMI: float
    BP_LVL: str
    CHOL_LVL: int
    NOTES: Optional[str] = None

    def __post_init__(self):
        # Validate ID (should be a 6-digit number)
        if not (100000 <= self.ID <= 999999):
            raise ValueError("ID must be a 6-digit number")
        
        # Validate SEX (should be 'M' or 'F')
        if self.SEX not in {'M', 'F'}:
            raise ValueError("SEX must be 'M' or 'F'")
        
        # Validate BP_LVL (should be in acceptable formats; this is a placeholder validation)
        if not self._is_valid_bp_lvl(self.BP_LVL):
            raise ValueError("BP_LVL format is not valid")
        
        # Validate CHOL_LVL (assuming it's within a reasonable range, e.g., 0-300)
        if not (0 <= self.CHOL_LVL <= 300):
            raise ValueError("CHOL_LVL must be between 0 and 300")

        # Validate NOTES (should be one of the specific values or None)
        if self.NOTES not in {'Needs follow-up', 'Regular check-up', 'Medication prescribed', None}:
            raise ValueError("NOTES must be 'Needs follow-up', 'Regular check-up', 'Medication prescribed', or None")

    def _is_valid_bp_lvl(self, bp_lvl: str) -> bool:
        # Define acceptable blood pressure level formats here
        # This is just an example; I'm not a medical expert!
        acceptable_formats = {'120/80', '130/85', '140/90', '150/95','110/70'}
        return bp_lvl in acceptable_formats
