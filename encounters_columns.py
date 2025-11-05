from tables import Tables
from enum import Enum, auto

class EncountersColumns(Enum):
    """
    ENCOUNTERS

    Records every time ICE Enforcement and Removal Operations encounters a
    person, i.e. considers whether to take enforcement action against a person.
    This need not mean a physical encounter. Most notably, every time ICE
    processes a match between FBI book-in information (i.e. to a jail or prison)
    and ICE database information, that match is logged as an ICE encounter.
    Generally, if an individual appears in the detainers or arrests table, that
    individual should appear in this table. An individual might appear in the
    removals or detentions tables without appearing in the encounters data if
    Customs and Border Protection initially encounters the person. This is both
    the largest and the sparsest of the tables, and in many cases, encounters
    lack a unique ID because the individual lacked an A number (A numbers are
    generally only given to people with immigrant visas or when they are
    processed for deportation proceedings).

    Note: the redacted columns were already removed by Kevin in the parquet file
    so I've commented them out here.

    Notes: 
    - 1.2 million rows
    - ~18% of rows are deported. Non-null values for 'Departed Date' indicates this
    - 'Departed Date' and 'Departure Country' are non-null together
    - 'Case Status' and 'Case Category' are non-null together
    - 'Final Order Date' is a "subset" of 'Final Order Yes No'
    - 'Departed Date' is a subset of 'Final Order Date' (maybe not tbd)

    * by "subset" I mean if the other columns value is non-null this one is too
    """
    EVENT_DATE = ("Event Date", Tables.ENCOUNTERS, "Date of encounter", False, False)
    RESPONSIBLE_AOR = ("Responsible AOR", Tables.ENCOUNTERS, "Area of Responsibility (ICE field office). See https://www.ice.gov/contact/field-offices for details on areas of responsibility.", False, False)
    RESPONSIBLE_SITE = ("Responsible Site", Tables.ENCOUNTERS, "We believe that this typically indicates the docket control office, which is a sub-office within an area of responsibility; we do not know more details. Some discussion of docket control offices is available here: https://www.ice.gov/doclib/foia/dro_policy_memos/09684drofieldpolicymanual.pdf.", False, False)
    LEAD_EVENT_TYPE = ("Lead Event Type", Tables.ENCOUNTERS, "Unknown category meaning, vast majority 'Not applicable'", False, True)
    LEAD_SOURCE = ("Lead Source", Tables.ENCOUNTERS, "Unknown", False, False)
    EVENT_TYPE = ("Event Type", Tables.ENCOUNTERS, "The event type roughly tracks the 'Apprehension method' field in the arrests data, though many encounters do not result in arrests.", False, False)
    FINAL_PROGRAM = ("Final Program", Tables.ENCOUNTERS, "The program associated with the arrest (not necessarily performed by ICE), which might also be described as the category of arrest. The values show the range of these categories, but key examples are the criminal alien program, which involves arrests in prisons and jails, the 287(g) program, which involves collaboration with a local agency, and border patrol.", False, False)
    # FINAL_PROGRAM_GROUP = ("Final Program Group", Tables.ENCOUNTERS, "Always ICE in encounters and arrests; in removals and detentions we would expect it often to be CBP.", True, False)
    ENCOUNTER_CRIMINALITY = ("Encounter Criminality", Tables.ENCOUNTERS, "This takes three values, corresponding to whether an individual has at least one criminal conviction, no criminal convictions but at least one criminal charge, or no charges or convictions ('other immigration violator')", False, False)
    PROCESSING_DISPOSITION = ("Processing Disposition", Tables.ENCOUNTERS, "We are unsure how to understand the values in this field, especially in relation to case category.", False, False)
    CASE_STATUS = ("Case Status", Tables.ENCOUNTERS, "Includes some information about case type and status, most likely as of the date that the data was extracted.", False, False)
    CASE_CATEGORY = ("Case Category", Tables.ENCOUNTERS, "This field includes combined information on case type and status. See https://journals.sagepub.com/doi/epdf/10.1177/233150241500300402 pp. 335-36 for descriptions of the values. Recorded at time of arrest.", False, False)
    DEPARTED_DATE = ("Departed Date", Tables.ENCOUNTERS, "Date of actual departure or deportation from the United States.", False, False)
    DEPARTURE_COUNTRY = ("Departure Country", Tables.ENCOUNTERS, "Country to which the individual was deported.", False, False)
    FINAL_ORDER_YES_NO = ("Final Order Yes No", Tables.ENCOUNTERS, "This indicates whether an individual has a final order of removal, which means an order of removal that was either affirmed on appeal or not appealed, or that was issued without the involvement of an immigration judge (for example, in expedited removal). See also the final order date field.", False, False)
    FINAL_ORDER_DATE = ("Final Order Date", Tables.ENCOUNTERS, "Date of the final order of removal, which means an order of removal that was either affirmed on appeal or not appealed, or that was issued without the involvement of an immigration judge (for example, in expedited removal).", False, False)
    # BIRTH_DATE = ("Birth Date", Tables.ENCOUNTERS, "", True, False)
    BIRTH_YEAR = ("Birth Year", Tables.ENCOUNTERS, "", False, False)
    CITIZENSHIP_COUNTRY = ("Citizenship Country", Tables.ENCOUNTERS, "", False, False)
    GENDER = ("Gender", Tables.ENCOUNTERS, "", False, False)
    EVENT_LANDMARK = ("Event Landmark", Tables.ENCOUNTERS, "Either an actual location or an ICE division associated with an arrest. See https://uwchr.github.io/ice-enforce/landmarks.html for details.", False, False)
    # ALIEN_FILE_NUMBER = ("Alien File Number", Tables.ENCOUNTERS, "", True, False)
    # EID_CASE_ID = ("EID Case ID", Tables.ENCOUNTERS, "", True, False)
    # EID_SUBJECT_ID = ("EID Subject ID", Tables.ENCOUNTERS, "", True, False)
    UNIQUE_IDENTIFIER = ("Unique Identifier", Tables.ENCOUNTERS, "Anonymized unique individual identifier based on Alien Registration Number (A-number). A-numbers are assigned to noncitizens by ICE or USCIS; undocumented noncitizens who have not interacted with the U.S. government, as well as people on nonimmigrant visas (i.e. people who do not intend to remain in the United States) typically do not have A-numbers.", False, False)

    # I (laird) use bad_data to signal a column we won't get any value out of. I should have used a more specific name
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