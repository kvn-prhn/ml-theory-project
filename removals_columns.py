from tables import Tables
from enum import Enum

class RemovalsColumns(Enum):
    """
    REMOVALS

    Records every deportation that ICE conducts, with a row for each individual
    deportation. An individual only has more than one row if that individual
    was deported more than once. Note that expulsions may occur directly at the
    border, by CBP, without involving ICE.
    """
    DEPARTED_DATE = ("Departed Date", Tables.REMOVALS, "Date of actual departure or deportation from the United States", False, False, False)
    PORT_OF_DEPARTURE = ("Port of Departure", Tables.REMOVALS, "Final place person left from", False, False, False)
    DEPARTURE_COUNTRY = ("Departure Country", Tables.REMOVALS, "Country to which the individual was deported", False, False, False)
    DOCKET_AOR = ("Docket AOR", Tables.REMOVALS, "Area of Responsibility (ICE field office). Our best guess is that this indicates the arresting field office rather than the field office covering the port of departure", False, False, False)
    APPREHENSION_STATE = ("Apprehension State", Tables.REMOVALS, "State of arrest", False, False, False)
    APPREHENSION_COUNTY = ("Apprehension County", Tables.REMOVALS, "County of arrest", False, False, False)
    CASE_STATUS = ("Case Status", Tables.REMOVALS, "Includes some information about case type and status, most likely as of the date that the data was extracted", False, False, False)
    GENDER = ("Gender", Tables.REMOVALS, "ICE determination of gender of individual", False, False, False)
    BIRTH_COUNTRY = ("Birth Country", Tables.REMOVALS, "Country of birth of noncitizen", False, False, False)
    CITIZENSHIP_COUNTRY = ("Citizenship Country", Tables.REMOVALS, "Country of citizenship of noncitizen", False, False, False)
    BIRTH_DATE = ("Birth Date", Tables.REMOVALS, "", True, False, False)
    BIRTH_YEAR = ("Birth Year", Tables.REMOVALS, "Birth year", False, False, False)
    ENTRY_DATE = ("Entry Date", Tables.REMOVALS, "Date of most recent entry into the United States", False, False, False)
    ENTRY_STATUS = ("Entry Status", Tables.REMOVALS, "We are unsure how this field is used", False, False, False)
    MSC_NCIC_CHARGE = ("MSC NCIC Charge", Tables.REMOVALS, "Standardized crime descriptions, likely drawn from the National Crime Information Center", False, False, False)
    MSC_NCIC_CHARGE_CODE = ("MSC NCIC Charge Code", Tables.REMOVALS, "", True, False, False)
    MSC_CHARGE_DATE = ("MSC Charge Date", Tables.REMOVALS, "Date of the charge for the conviction", False, False, False)
    MSC_CRIMINAL_CHARGE_STATUS = ("MSC Criminal Charge Status", Tables.REMOVALS, "Status near always marked as 'Convicted,' otherwise 'Pending'", False, False, False)
    MSC_CRIMINAL_CHARGE_STATUS_CODE = ("MSC Criminal Charge Status Code", Tables.REMOVALS, "", True, False, False)
    MSC_CONVICTION_DATE = ("MSC Conviction Date", Tables.REMOVALS, "Date of Most Serious Criminal Conviction", False, False, False)
    CASE_THREAT_LEVEL = ("Case Threat Level", Tables.REMOVALS, "Removal case threat level based on conviction; corresponds to ICE threat categorization levels", False, False, False)
    CASE_CRIMINALITY = ("Case Criminality", Tables.REMOVALS, "Whether individual has criminal conviction, pending charge, or no charges", False, False, False)
    FELON = ("Felon", Tables.REMOVALS, "A flag indicating that ICE believes a person has an aggravated felony conviction", False, False, False)
    PROCESSING_DISPOSITION = ("Processing Disposition", Tables.REMOVALS, "We are unsure how to understand the values in this field", False, False, False)
    CASE_CATEGORY = ("Case Category", Tables.REMOVALS, "Combined information on case type and status", False, False, False)
    FINAL_PROGRAM = ("Final Program", Tables.REMOVALS, "Program associated with the arrest, such as criminal alien program or 287(g)", False, False, False)
    FINAL_PROGRAM_CODE = ("Final Program Code", Tables.REMOVALS, "", True, False, False)
    CASE_CATEGORY_TIME_OF_ARREST = ("Case Category Time of Arrest", Tables.REMOVALS, "", True, False, False)
    LATEST_ARREST_PROGRAM_CURRENT = ("Latest Arrest Program Current", Tables.REMOVALS, "Program associated with the arrest", False, False, False)
    LATEST_ARREST_PROGRAM_CURRENT_CODE = ("Latest Arrest Program Current Code", Tables.REMOVALS, "", True, False, False)
    LATEST_PERSON_APPREHENSION_DATE = ("Latest Person Apprehension Date", Tables.REMOVALS, "Date of most recent arrest", False, False, False)
    FINAL_ORDER_YES_NO = ("Final Order Yes No", Tables.REMOVALS, "Indicates whether individual has a final order of removal", False, False, False)
    FINAL_ORDER_DATE = ("Final Order Date", Tables.REMOVALS, "Date of final order of removal; either affirmed on appeal or uncontested", False, False, False)
    FINAL_CHARGE_CODE = ("Final Charge Code", Tables.REMOVALS, "", True, False, False)
    FINAL_CHARGE_SECTION_CODE = ("Final Charge Section Code", Tables.REMOVALS, "", True, False, False)
    PRIOR_DEPORT_YES_NO = ("Prior Deport Yes No", Tables.REMOVALS, "Indicator for whether individual was previously removed", False, False, False)
    LATEST_PERSON_DEPARTED_DATE = ("Latest Person Departed Date", Tables.REMOVALS, "", False, False, False)
    ALIEN_FILE_NUMBER = ("Alien File Number", Tables.REMOVALS, "", True, False, False)
    EID_CASE_ID = ("EID Case ID", Tables.REMOVALS, "", True, False, False)
    EID_SUBJECT_ID = ("EID Subject ID", Tables.REMOVALS, "", True, False, False)
    UNIQUE_IDENTIFIER = ("Unique Identifier", Tables.REMOVALS, "Anonymized unique individual identifier based on Alien Registration Number", False, False, False)

    # Derived columns
    CONVICTED = ("Convicted", Tables.REMOVALS, "boolean derived from MSC Criminal Charge Status - True if status is CONVICTED, False otherwise", False, False, True)
    MALE = ("Male", Tables.REMOVALS, "true if male, false if female", False, False, True)
    IS_FELON = ("Is Felon", Tables.REMOVALS, "true if felon, false otherwise", False, False, True)

    def __init__(self, column_name, table, description, redacted, bad_data, derived):
        self.column_name = column_name
        self.table = table
        self.description = description
        self.redacted = redacted
        self.bad_data = bad_data
        self.derived = derived
        self.useable = not redacted and not bad_data
