from enum import Enum

class ArrestsColumns(Enum):
    APPREHENSION_DATE = ("Apprehension Date", "The date of arrest", False, False)
    APPREHENSION_STATE = ("Apprehension State", "State where arrest occurred", False, False)
    APPREHENSION_COUNTY = ("Apprehension County", "County where the arrest occurred", False, True)
    APPREHENSION_AOR = ("Apprehension AOR", "Area of Responsibility (ICE field office) which conducted the arrest", False, False)
    FINAL_PROGRAM = ("Final Program", "The program associated with the arrest (not necessarily performed by ICE), which might also be described as the category of arrest", False, False)
    FINAL_PROGRAM_GROUP = ("Final Program Group", "Single value column", False, True)
    APPREHENSION_METHOD = ("Apprehension Method", "This describes how the arrest took place, with the most important distinction being between arrests that take place in prisons and jails and arrests that take place elsewhere", False, False)
    APPREHENSION_CRIMINALITY = ("Apprehension Criminality", "Categorizes individuals by criminal history status—those with convictions, those with charges but no convictions, or immigration violators without criminal records", False, False)
    CASE_STATUS = ("Case Status", "Includes some information about case type and status, most likely as of the date that the data was extracted", False, False)
    CASE_CATEGORY = ("Case Category", "This field includes combined information on case type and status. See https://journals.sagepub.com/doi/epdf/10.1177/233150241500300402 pp. 335-36 for descriptions of the values", False, False)
    DEPARTED_DATE = ("Departed Date", "Date of actual departure or deportation from the United States", False, False)
    DEPARTURE_COUNTRY = ("Departure Country", "Country to which the individual was deported", False, False)
    FINAL_ORDER_YES_NO = ("Final Order Yes No", "YES/NO depending on whether final order date is defined", False, True)
    FINAL_ORDER_DATE = ("Final Order Date", "date of removal order or a non-appealed order", False, False)
    BIRTH_DATE = ("Birth Date", "", True, False)
    BIRTH_YEAR = ("Birth Year", "Birth year of the individual", False, False)
    CITIZENSHIP_COUNTRY = ("Citizenship Country", "Country of citizenship of noncitizen", False, False)
    GENDER = ("Gender", "ICE determination of gender of individual", False, False)
    APPREHENSION_SITE_LANDMARK = ("Apprehension Site Landmark", "Either an actual location or an ICE division associated with an arrest", False, False)
    ALIEN_FILE_NUMBER = ("Alien File Number", "Anonymized", True, False)
    EID_CASE_ID = ("EID Case ID", "Anonymized", True, False)
    EID_SUBJECT_ID = ("EID Subject ID", "Anonymized", True, False)
    UNIQUE_IDENTIFIER = ("Unique Identifier", "Anonymized unique individual identifier based on Alien Registration Number (A-number)", False, False)

    def __init__(self, column_name, description, redacted, bad_data):
        self.column_name = column_name
        # self.table = table
        self.description = description
        self.redacted = redacted
        self.bad_data = bad_data
        self.useable = not redacted and not bad_data
