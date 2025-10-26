from tables import Tables
from enum import Enum, auto

class DetainersColumns(Enum):
    DETAINER_PREPARE_DATE = (
        "Detainer Prepare Date", Tables.DETAINERS,
        "Date on which detainer was issued/sent to the receiving jail/prison. Very low mislabeled data.",
        False, True
    )
    FACILITY_STATE = (
        "Facility State", Tables.DETAINERS,
        "State of the jail/prison receiving the detainer request.",
        False, False
    )
    FACILITY_AOR = (
        "Facility AOR", Tables.DETAINERS,
        "ICE field office responsible for the facility's area. See https://www.ice.gov/contact/field-offices.",
        False, False
    )
    PORT_OF_DEPARTURE = (
        "Port of Departure", Tables.DETAINERS,
        "Final place the person departed from.",
        False, False
    )
    DEPARTURE_COUNTRY = (
        "Departure Country", Tables.DETAINERS,
        "Country to which the individual was deported.",
        False, False
    )
    DEPARTED_DATE = (
        "Departed Date", Tables.DETAINERS,
        "Date of actual departure/removal from the United States.",
        False, False
    )
    CASE_STATUS = (
        "Case Status", Tables.DETAINERS,
        "Combined info on case type and status (likely as of extraction date).",
        False, False
    )
    DETAINER_PREPARED_CRIMINALITY = (
        "Detainer Prepared Criminality", Tables.DETAINERS,
        "Three values: conviction; charge-only; or no charges/convictions (other immigration violator).",
        False, False
    )
    DETENTION_FACILITY = (
        "Detention Facility", Tables.DETAINERS,
        "Name of jail/prison that received the detainer request (criminal custody, not immigration detention).",
        False, False
    )
    DETENTION_FACILITY_CODE = (
        "Detention Facility Code", Tables.DETAINERS,
        "Short alphabetic code (DETLOC). Semantics differ across tables; here = criminal-custody facility code.",
        False, False
    )
    FACILITY_CITY = (
        "Facility City", Tables.DETAINERS,
        "City where the jail/prison receiving the detainer request is located.",
        False, False
    )
    DETAINER_PREP_THREAT_LEVEL = (
        "Detainer Prep Threat Level", Tables.DETAINERS,
        "Conviction-based threat-like levels but appears to rely on predicted outcomes from pending charges; missingness can be meaningful.",
        False, False
    )
    GENDER = (
        "Gender", Tables.DETAINERS,
        "ICE determination of gender.",
        False, False
    )
    CITIZENSHIP_COUNTRY = (
        "Citizenship Country", Tables.DETAINERS,
        "Country of citizenship of the noncitizen.",
        False, False
    )
    BIRTH_COUNTRY = (
        "Birth Country", Tables.DETAINERS,
        "Country of birth of the noncitizen.",
        False, False
    )
    BIRTH_YEAR = (
        "Birth Year", Tables.DETAINERS,
        "Birth year.",
        False, False
    )
    ENTRY_STATUS = (
        "Entry Status", Tables.DETAINERS,
        "Usage unclear in documentation.",
        False, True
    )
    MOST_SERIOUS_CONVICTION_CHARGE = (
        "Most Serious Conviction (MSC) Charge", Tables.DETAINERS,
        "Most serious criminal conviction recorded (standardized, likely NCIC-derived).",
        False, False
    )
    MSC_SENTENCE_DAYS = (
        "MSC Sentence Days", Tables.DETAINERS,
        "Days portion of sentence for the MSC; many convictions lack any sentence fields (use caution).",
        False, False
    )
    MSC_SENTENCE_MONTHS = (
        "MSC Sentence Months", Tables.DETAINERS,
        "Months portion of sentence for the MSC; many convictions lack any sentence fields (use caution).",
        False, False
    )
    MSC_SENTENCE_YEARS = (
        "MSC Sentence Years", Tables.DETAINERS,
        "Years portion of sentence for the MSC; many convictions lack any sentence fields (use caution).",
        False, False
    )
    MSC_CHARGE_DATE = (
        "MSC Charge Date", Tables.DETAINERS,
        "Date of charge for the MSC.",
        False, False
    )
    MSC_CONVICTION_DATE = (
        "MSC Conviction Date", Tables.DETAINERS,
        "Date of conviction for the MSC.",
        False, False
    )
    FELON = (
        "Felon", Tables.DETAINERS,
        "Flag indicating aggravated felony conviction status; documentation unsure whether used.",
        False, True
    )
    PROCESSING_DISPOSITION = (
        "Processing Disposition", Tables.DETAINERS,
        "Disposition codes are hard to interpret and may not align cleanly with Case Category.",
        False, True
    )
    CASE_CATEGORY = (
        "Case Category", Tables.DETAINERS,
        "Combined information on case type and status (see referenced memo pp. 335-36).",
        False, False
    )
    FINAL_PROGRAM = (
        "Final Program", Tables.DETAINERS,
        "Program/category associated with the arrest (e.g., CAP, 287(g), Border Patrol).",
        False, False
    )
    TIME_OF_APPREHENSION_CASE_CATEGORY = (
        "Time of Apprehension Case Category", Tables.DETAINERS,
        "Case type/status recorded at the time of apprehension.",
        False, False
    )
    TIME_OF_APPREHENSION_CURRENT_PROGRAM = (
        "Time of Apprehension Current Program", Tables.DETAINERS,
        "Program/category associated with the arrest at time of apprehension.",
        False, False
    )
    APPREHENSION_METHOD = (
        "Apprehension Method", Tables.DETAINERS,
        "How the arrest took place (notably, in prisons/jails vs elsewhere).",
        False, False
    )
    CASE_FINAL_ORDER_YES_NO = (
        "Case Final Order Yes No", Tables.DETAINERS,
        "Whether a final order of removal exists for the case (see also Final Order Date).",
        False, False
    )
    FINAL_ORDER_DATE = (
        "Final Order Date", Tables.DETAINERS,
        "Date the final order of removal was issued/affirmed or became final.",
        False, False
    )
    APPREHENSION_DATE = (
        "Apprehension Date", Tables.DETAINERS,
        "Date of arrest.",
        False, False
    )
    ENTRY_DATE = (
        "Entry Date", Tables.DETAINERS,
        "Date of most recent entry into the United States.",
        False, False
    )
    PRIOR_FELONY_YES_NO = (
        "Prior Felony Yes No", Tables.DETAINERS,
        "Indicator for prior felony; semantics uncertain.",
        False, True
    )
    MULTIPLE_PRIOR_MISD_YES_NO = (
        "Multiple Prior MISD Yes No", Tables.DETAINERS,
        "Indicator for multiple prior misdemeanors; semantics uncertain.",
        False, True
    )
    VIOLENT_MISDEMEANOR_YES_NO = (
        "Violent Misdemeanor Yes No", Tables.DETAINERS,
        "Indicator for violent misdemeanor; semantics uncertain.",
        False, True
    )
    ILLEGAL_ENTRY_YES_NO = (
        "Illegal Entry Yes No", Tables.DETAINERS,
        "Indicator for illegal entry; documentation states unknown.",
        False, True
    )
    ILLEGAL_REENTRY_YES_NO = (
        "Illegal Reentry Yes No", Tables.DETAINERS,
        "Indicator for illegal reentry; documentation states unknown.",
        False, True
    )
    IMMIGRATION_FRAUD_YES_NO = (
        "Immigration Fraud Yes No", Tables.DETAINERS,
        "Indicator for immigration fraud; documentation states unknown.",
        False, True
    )
    SIGNIFICANT_RISK_YES_NO = (
        "Significant Risk Yes No", Tables.DETAINERS,
        "Risk flag; documentation states unknown.",
        False, True
    )
    OTHER_REMOVAL_REASON_YES_NO = (
        "Other Removal Reason Yes No", Tables.DETAINERS,
        "Whether another removal reason applies; documentation states unknown.",
        False, True
    )
    OTHER_REMOVAL_REASON = (
        "Other Removal Reason", Tables.DETAINERS,
        "Text field describing other removal reason (if any).",
        False, False
    )
    CRIMINAL_STREET_GANG_YES_NO = (
        "Criminal Street Gang Yes No", Tables.DETAINERS,
        "Indicator for gang affiliation; documentation states unknown.",
        False, True
    )
    AGGRAVATED_FELONY_YES_NO = (
        "Aggravated Felony Yes No", Tables.DETAINERS,
        "Flag indicating aggravated felony conviction; documentation unsure whether used.",
        False, True
    )
    DEPORTATION_ORDERED_YES_NO = (
        "Deportation Ordered Yes No", Tables.DETAINERS,
        "Whether the person was ordered removed; final order date is generally more reliable.",
        False, False
    )
    ORDER_TO_SHOW_CAUSE_SERVED_YES_NO = (
        "Order to Show Cause Served Yes No", Tables.DETAINERS,
        "Whether a Notice to Appear (formerly Order to Show Cause) was issued.",
        False, False
    )
    ORDER_TO_SHOW_CAUSE_SERVED_DATE = (
        "Order to Show Cause Served Date", Tables.DETAINERS,
        "Date the Notice to Appear (formerly Order to Show Cause) was issued.",
        False, False
    )
    BIOMETRIC_MATCH_YES_NO = (
        "Biometric Match Yes No", Tables.DETAINERS,
        "Meaning unclear in documentation.",
        False, True
    )
    STATEMENTS_MADE_YES_NO = (
        "Statements Made Yes No", Tables.DETAINERS,
        "Whether statements were made; roughly a quarter of entries missing—use caution.",
        False, True
    )
    UNLAWFUL_ATTEMPT_YES_NO = (
        "Unlawful Attempt Yes No", Tables.DETAINERS,
        "Indicator for unlawful attempt; documentation states unknown.",
        False, True
    )
    UNLAWFUL_ENTRY_YES_NO = (
        "Unlawful Entry Yes No", Tables.DETAINERS,
        "Indicator for unlawful entry; documentation states unknown.",
        False, True
    )
    VISA_YES_NO = (
        "Visa Yes No", Tables.DETAINERS,
        "Indicator for visa; documentation states unknown.",
        False, True
    )
    FINAL_ORDER_YES_NO = (
        "Final Order Yes No", Tables.DETAINERS,
        "Whether an individual has a final order of removal (affirmed or unappealed, or issued without IJ).",
        False, False
    )
    FEDERAL_INTEREST_YES_NO = (
        "Federal Interest Yes No", Tables.DETAINERS,
        "Indicator for federal interest; documentation states unknown.",
        False, True
    )
    RESUME_CUSTODY_YES_NO = (
        "Resume Custody Yes No", Tables.DETAINERS,
        "Indicator for resuming custody; documentation states unknown.",
        False, True
    )
    DETAINER_LIFT_REASON = (
        "Detainer Lift Reason", Tables.DETAINERS,
        "Reason detainer was lifted (e.g., booked into immigration detention vs declined).",
        False, False
    )
    DETAINER_TYPE = (
        "Detainer Type", Tables.DETAINERS,
        "Whether ICE requested continued detention vs notification of release; reliability uncertain.",
        False, True
    )
    UNIQUE_IDENTIFIER = (
        "Unique Identifier", Tables.DETAINERS,
        "Anonymized unique individual identifier (A-number-based).",
        False, False
    )

    def __init__(self, column_name, table, description, redacted, bad_data):
        self.column_name = column_name
        self.table = table
        self.description = description
        self.redacted = redacted
        self.bad_data = bad_data
        self.useable = not redacted and not bad_data