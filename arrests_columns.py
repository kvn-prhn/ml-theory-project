from enum import Enum

class ArrestsColumns(Enum):
    APPREHENSION_DATE = ("Apprehension Date", "", False, False)
    APPREHENSION_STATE = ("Apprehension State", "", False, False)
    APPREHENSION_COUNTY = ("Apprehension County", "", False, True)
    APPREHENSION_AOR = ("Apprehension AOR", "", False, False)
    FINAL_PROGRAM = ("Final Program", "", False, False)
    FINAL_PROGRAM_GROUP = ("Final Program Group", "", False, True)
    APPREHENSION_METHOD = ("Apprehension Method", "", False, False)
    APPREHENSION_CRIMINALITY = ("Apprehension Criminality", "", False, False)
    CASE_STATUS = ("Case Status", "", False, False)
    CASE_CATEGORY = ("Case Category", "", False, False)
    DEPARTED_DATE = ("Departed Date", "", False, False)
    DEPARTURE_COUNTRY = ("Departure Country", "", False, False)
    FINAL_ORDER_YES_NO = ("Final Order Yes No", "YES/NO depending on whether final order date is defined", False, True)
    FINAL_ORDER_DATE = ("Final Order Date", "date of removal order or a non-appealed order", False, False)
    BIRTH_DATE = ("Birth Date", "", True, False)
    BIRTH_YEAR = ("Birth Year", "", False, False)
    CITIZENSHIP_COUNTRY = ("Citizenship Country", "", False, False)
    GENDER = ("Gender", "", False, False)
    APPREHENSION_SITE_LANDMARK = ("Apprehension Site Landmark", "", False, False)
    ALIEN_FILE_NUMBER = ("Alien File Number", "", True, False)
    EID_CASE_ID = ("EID Case ID", "", True, False)
    EID_SUBJECT_ID = ("EID Subject ID", "", True, False)
    UNIQUE_IDENTIFIER = ("Unique Identifier", "derived from alien registration number", False, False)

    def __init__(self, column_name, description, redacted, bad_data):
        self.column_name = column_name
        # self.table = table
        self.description = description
        self.redacted = redacted
        self.bad_data = bad_data
        self.useable = not redacted and not bad_data
