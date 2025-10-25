from tables import Tables
from enum import Enum, auto

class Columns(Enum):
    DEPARTED_DATE = ("Departed Date", Tables.REMOVALS, "", False, False)
    PORT_OF_DEPARTURE = ("Port of Departure", Tables.REMOVALS, "", False, False)
    DEPARTURE_COUNTRY = ("Departure Country", Tables.REMOVALS, "", False, False)
    DOCKET_AOR = ("Docket AOR", Tables.REMOVALS, "", False, False)
    APPREHENSION_STATE = ("Apprehension State", Tables.REMOVALS, "", False, False)
    APPREHENSION_COUNTY = ("Apprehension County", Tables.REMOVALS, "", False, False)
    CASE_STATUS = ("Case Status", Tables.REMOVALS, "", False, False)
    GENDER = ("Gender", Tables.REMOVALS, "", False, False)
    BIRTH_COUNTRY = ("Birth Country", Tables.REMOVALS, "", False, False)
    CITIZENSHIP_COUNTRY = ("Citizenship Country", Tables.REMOVALS, "", False, False)
    BIRTH_DATE = ("Birth Date", Tables.REMOVALS, "", True, False)
    BIRTH_YEAR = ("Birth Year", Tables.REMOVALS, "", False, False)
    ENTRY_DATE = ("Entry Date", Tables.REMOVALS, "", False, False)
    ENTRY_STATUS = ("Entry Status", Tables.REMOVALS, "", False, False)
    MSC_NCIC_CHARGE = ("MSC NCIC Charge", Tables.REMOVALS, "", False, False)
    MSC_NCIC_CHARGE_CODE = ("MSC NCIC Charge Code", Tables.REMOVALS, "", True, False)
    MSC_CHARGE_DATE = ("MSC Charge Date", Tables.REMOVALS, "", False, False)
    MSC_CRIMINAL_CHARGE_STATUS = ("MSC Criminal Charge Status", Tables.REMOVALS, "", False, False)
    MSC_CRIMINAL_CHARGE_STATUS_CODE = ("MSC Criminal Charge Status Code", Tables.REMOVALS, "", True, False)
    MSC_CONVICTION_DATE = ("MSC Conviction Date", Tables.REMOVALS, "", False, False)
    CASE_THREAT_LEVEL = ("Case Threat Level", Tables.REMOVALS, "", False, False)
    CASE_CRIMINALITY = ("Case Criminality", Tables.REMOVALS, "", False, False)
    FELON = ("Felon", Tables.REMOVALS, "", False, False)
    PROCESSING_DISPOSITION = ("Processing Disposition", Tables.REMOVALS, "", False, False)
    CASE_CATEGORY = ("Case Category", Tables.REMOVALS, "", False, False)
    FINAL_PROGRAM = ("Final Program", Tables.REMOVALS, "", False, False)
    FINAL_PROGRAM_CODE = ("Final Program Code", Tables.REMOVALS, "", True, False)
    CASE_CATEGORY_TIME_OF_ARREST = ("Case Category Time of Arrest", Tables.REMOVALS, "", True, False)
    LATEST_ARREST_PROGRAM_CURRENT = ("Latest Arrest Program Current", Tables.REMOVALS, "", False, False)
    LATEST_ARREST_PROGRAM_CURRENT_CODE = ("Latest Arrest Program Current Code", Tables.REMOVALS, "", True, False)
    LATEST_PERSON_APPREHENSION_DATE = ("Latest Person Apprehension Date", Tables.REMOVALS, "", False, False)
    FINAL_ORDER_YES_NO = ("Final Order Yes No", Tables.REMOVALS, "", False, False)
    FINAL_ORDER_DATE = ("Final Order Date", Tables.REMOVALS, "", False, False)
    FINAL_CHARGE_CODE = ("Final Charge Code", Tables.REMOVALS, "", True, False)
    FINAL_CHARGE_SECTION_CODE = ("Final Charge Section Code", Tables.REMOVALS, "", True, False)
    PRIOR_DEPORT_YES_NO = ("Prior Deport Yes No", Tables.REMOVALS, "", False, False)
    LATEST_PERSON_DEPARTED_DATE = ("Latest Person Departed Date", Tables.REMOVALS, "", False, False)
    ALIEN_FILE_NUMBER = ("Alien File Number", Tables.REMOVALS, "", True, False)
    EID_CASE_ID = ("EID Case ID", Tables.REMOVALS, "", True, False)
    EID_SUBJECT_ID = ("EID Subject ID", Tables.REMOVALS, "", True, False)
    UNIQUE_IDENTIFIER = ("Unique Identifier", Tables.REMOVALS, "", False, False)


    def __init__(self, column_name, table, description, redacted, bad_data):
        self.column_name = column_name
        self.table = table
        self.description = description
        self.redacted = redacted
        self.bad_data = bad_data
        self.useable = not redacted and not bad_data

if __name__ == "__main__":
    depared_date_column = Columns.DEPARTED_DATE
    print(f"column name: {depared_date_column.column_name}")
    print(f"table: {depared_date_column.table}")
    print(f"useable: {depared_date_column.useable}")
