from enum import Enum

class ArrestsColumns(str, Enum):
    APPREHENSION_DATE = "Apprehension Date"  # date
    APPREHENSION_STATE = "Apprehension State"  # categorical
    # APPREHENSION_COUNTY = "Apprehension County"  # (entirely missing)
    APPREHENSION_AOR = "Apprehension AOR"  # categorical. AOR: "Area of Responsibility"
    FINAL_PROGRAM = "Final Program"  # categorical. e.g., "ERO Criminal Area Program"
    # FINAL_PROGRAM_GROUP = "Final Program Group"  # categorial. e.g., ICE
    APPREHENSION_METHOD = "Apprehension Method"  # categorical 
    APPREHENSION_CRIMINALITY = "Apprehension Criminality"
    CASE_STATUS = "Case Status"
    CASE_CATEGORY = "Case Category"
    DEPARTED_DATE = "Departed Date"
    DEPARTURE_COUNTRY = "Departure Country"
    FINAL_ORDER_YES_NO = "Final Order Yes No"  # boolean
    FINAL_ORDER_DATE = "Final Order Date"
    # BIRTH_DATE = "Birth Date"  # redacted
    BIRTH_YEAR = "Birth Year"
    CITIZENSHIP_COUNTRY = "Citizenship Country"
    GENDER = "Gender"  # boolean
    APPREHENSION_SITE_LANDMARK = "Apprehension Site Landmark"
    # ALIEN_FILE_NUMBER = "Alien File Number"  # redacted
    # EID_CASE_ID = "EID Case ID"  # redacted
    # EID_SUBJECT_ID = "EID Subject ID"  # redacted
    UNIQUE_IDENTIFIER = "Unique Identifier"
