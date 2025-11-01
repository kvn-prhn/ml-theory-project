from enum import Enum

class DetentionsColumns(Enum):
    STAY_BOOK_IN_DATE_TIME = ("Stay Book In Date Time", "start of total detention time", False, False)
    BOOK_IN_DATE_TIME = ("Book In Date Time", "start of detention at particular facility", False, False)
    DETENTION_FACILITY = ("Detention Facility", "redundant with detention facility code", False, True)
    DETENTION_FACILITY_CODE = ("Detention Facility Code", "", False, False)
    DETENTION_BOOK_OUT_DATE_TIME = ("Detention Book Out Date Time", "", False, False)
    STAY_BOOK_OUT_DATE_TIME = ("Stay Book Out Date Time", "book out of entire detention", False, False)
    DETENTION_RELEASE_REASON = ("Detention Release Reason", "", False, False)
    STAY_BOOK_OUT_DATE = ("Stay Book Out Date", "book out at particular facility", False, False)
    STAY_RELEASE_REASON = ("Stay Release Reason", "", False, False)
    RELIGION = ("Religion", "Mostly missing. over 97% missing values", False, True)
    GENDER = ("Gender", "", False, False)
    MARITAL_STATUS = ("Marital Status", "", False, False)
    BIRTH_DATE = ("Birth Date", "", True, False)
    BIRTH_YEAR = ("Birth Year", "", False, False)
    ETHNICITY = ("Ethnicity", "Hispanic or not hispanic", False, False)
    ENTRY_STATUS = ("Entry Status", "Needs to be normalized, but probably usable", False, False)
    FELON = ("Felon", "", False, False)
    BOND_POSTED_DATE = ("Bond Posted Date", "mostly missing, 92%", False, True)
    BOND_POSTED_AMOUNT = ("Bond Posted Amount", "mostly missing, 92%", False, True)
    CASE_STATUS = ("Case Status", "", False, False)
    CASE_CATEGORY = ("Case Category", "", False, False)
    FINAL_ORDER_YES_NO = ("Final Order Yes No", "", False, False)
    FINAL_ORDER_DATE = ("Final Order Date", "", False, False)
    CASE_THREAT_LEVEL = ("Case Threat Level", "1-aggravated felon, 2-3 or more convicted felon crimes, 3-fewer than 3, at least 1 convicted felon crime", False, False)
    BOOK_IN_CRIMINALITY = ("Book In Criminality", "", False, False)
    FINAL_CHARGE = ("Final Charge", "", False, False)
    DEPARTED_DATE = ("Departed Date", "", False, False)
    DEPARTURE_COUNTRY = ("Departure Country", "", False, False)
    INITIAL_BOND_SET_AMOUNT = ("Initial Bond Set Amount", "", False, False)
    CITIZENSHIP_COUNTRY = ("Citizenship Country", "", False, False)
    FINAL_PROGRAM = ("Final Program", "", False, False)
    MOST_SERIOUS_CONVICTION_MSC_CHARGE_CODE = ("Most Serious Conviction (MSC) Charge Code", "redundant", False, True)
    MSC_CHARGE = ("MSC Charge", "", False, False)
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
