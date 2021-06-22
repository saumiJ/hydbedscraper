from enum import Enum
from typing import Dict


class Label(Enum):
    HOSPITAL_NAME = "hospital_name"
    HOSPITAL_ADDRESS = "hospital_address"
    HOSPITAL_CATEGORY = "hospital_category"
    DISTRICT = "district"
    AREA = "area"
    CONTACT_NUMBER = "contact_number"

    OFFICER_NAME = "officer_name"
    OFFICER_DESIGNATION = "officer_designation"

    CHARGES_TYPE = "charges_type"

    ISOLATION_NON_OXYGEN_OCCUPIED_BEDS = "isolation_non_oxygen_occupied_beds"
    ISOLATION_NON_OXYGEN_VACANT_BEDS = "isolation_non_oxygen_vacant_beds"

    ISOLATION_OXYGEN_OCCUPIED_BEDS = "isolation_oxygen_occupied_beds"
    ISOLATION_OXYGEN_VACANT_BEDS = "isolation_oxygen_vacant_beds"

    HIGH_DEPENDENCY_UNIT_OCCUPIED_BEDS = "high_dependency_unit_occupied_beds"
    HIGH_DEPENDENCY_UNIT_VACANT_BEDS = "high_dependency_unit_vacant_beds"

    ICU_NON_VENTILATOR_OCCUPIED_BEDS = "icu_non_ventilator_occupied_beds"
    ICU_NON_VENTILATOR_VACANT_BEDS = "icu_non_ventilator_vacant_beds"

    ICU_VENTILATOR_OCCUPIED_BEDS = "icu_ventilator_occupied_beds"
    ICU_VENTILATOR_VACANT_BEDS = "icu_ventilator_vacant_beds"

    FEE_REGULATED_BEDS = "fee_regulated_beds"

    LAST_UPDATED_DATE = "last_updated_date"
    LAST_UPDATED_TIME = "last_updated_time"


str_to_label_map: Dict[str, Label] = {
    "hospital name": Label.HOSPITAL_NAME,
    "hospital address": Label.HOSPITAL_ADDRESS,
}


def str_to_label(_str: str) -> Label:
    return str_to_label_map[_str.strip().lower()]
