import pandas as pd
import numpy as np
import pathlib
import re
from datetime import datetime
from detentions_columns import DetentionsColumns

def clean_detentions(d):
    use_cols = [v.value[0] for k, v in DetentionsColumns.__members__.items() if not v.value[2] and not v.value[3]]
    print(f'{use_cols=}')
    d = d[use_cols].copy()
    d.head()

    def missing_percent_print(d, col_name):
        print(f"{col_name}, {(d[col_name].isnull().sum() / len(d)).item() * 100:.4}% missing values")

    missing_percent_print(d, DetentionsColumns.STAY_BOOK_IN_DATE_TIME.column_name)

    # dates filtering
    print(f'before detentions date filtering: {d.shape=}')
    d = d[d[DetentionsColumns.STAY_BOOK_IN_DATE_TIME.column_name].isna() |
        ((pd.to_datetime('2023-9-1') <= d[DetentionsColumns.STAY_BOOK_IN_DATE_TIME.column_name]) & 
        (d[DetentionsColumns.STAY_BOOK_IN_DATE_TIME.column_name] <= pd.to_datetime('2025-7-31')))].copy()
    d = d[d[DetentionsColumns.BOOK_IN_DATE_TIME.column_name].isna() |
        ((pd.to_datetime('2023-9-1') <= d[DetentionsColumns.BOOK_IN_DATE_TIME.column_name]) & 
        (d[DetentionsColumns.BOOK_IN_DATE_TIME.column_name] <= pd.to_datetime('2025-7-31')))].copy()
    d = d[d[DetentionsColumns.STAY_BOOK_OUT_DATE_TIME.column_name].isna() |
        ((pd.to_datetime('2023-9-1') <= d[DetentionsColumns.STAY_BOOK_OUT_DATE_TIME.column_name]) & 
        (d[DetentionsColumns.STAY_BOOK_OUT_DATE_TIME.column_name] <= pd.to_datetime('2025-7-31')))].copy()
    d = d[d[DetentionsColumns.STAY_BOOK_OUT_DATE.column_name].isna() |
        ((pd.to_datetime('2023-9-1') <= d[DetentionsColumns.STAY_BOOK_OUT_DATE.column_name]) & 
        (d[DetentionsColumns.STAY_BOOK_OUT_DATE.column_name] <= pd.to_datetime('2025-7-31')))].copy()
    print(f'after detentions date filtering: {d.shape=}')

    missing_percent_print(d, DetentionsColumns.DETENTION_FACILITY_CODE.column_name)

    # d[DetentionsColumns.DETENTION_FACILITY_CODE.column_name].value_counts()

    missing_percent_print(d, DetentionsColumns.DETENTION_RELEASE_REASON.column_name)

    def release_reason_replace(d, c):
        # c = DetentionsColumns.DETENTION_RELEASE_REASON.column_name
        # group similar categories back to other categories if its obvious
        d[c] = d[c].replace('Paroled - Fear Found', 'Paroled')
        d[c] = d[c].replace('Paroled - Public Benefit', 'Paroled')
        d[c] = d[c].replace('Paroled - Humanitarian', 'Paroled')
        d[c] = d[c].replace('Voluntary Return', 'Voluntary departure')
        d[c] = d[c].replace('Voluntary Return', 'Voluntary departure')
        # https://immigrationlawneworleans.com/immigration-law/order-of-supervision-osup-what-you-need-to-know/
        d[c] = d[c].replace('Order of supervision', 'Order of Supervision')
        d[c] = d[c].replace('Order of Supervision - Humanitarian', 'Order of Supervision')
        d[c] = d[c].replace('Order of Supervision - Re-Release', 'Order of Supervision')
        d[c] = d[c].replace('Order of Supervision - No SLRRFF', 'Order of Supervision')
        d[c] = d[c].replace('Order of recognizance', 'Order of Recognizance')
        d[c] = d[c].replace('Order of Recognizance - Humanitarian', 'Order of Recognizance')
        d[c] = d[c].replace('ORR - Office of Refugee Resettlement', 'Office of Refugee Resettlement')
        d[c] = d[c].replace('ORR-Runaway', 'Office of Refugee Resettlement')

    release_reason_replace(d, DetentionsColumns.DETENTION_RELEASE_REASON.column_name)

    d[DetentionsColumns.DETENTION_RELEASE_REASON.column_name].value_counts()

    missing_percent_print(d, DetentionsColumns.STAY_RELEASE_REASON.column_name)

    release_reason_replace(d, DetentionsColumns.STAY_RELEASE_REASON.column_name)

    d[DetentionsColumns.STAY_RELEASE_REASON.column_name].value_counts()

    # missing_percent_print(d, DetentionsColumns.RELIGION.column_name)

    missing_percent_print(d, DetentionsColumns.MARITAL_STATUS.column_name)

    # impute missing values with 'Unknown'
    d[DetentionsColumns.MARITAL_STATUS.column_name] = d[DetentionsColumns.MARITAL_STATUS.column_name].apply(lambda x: 'Unknown' if type(x) != str else x)

    # assume 'separated' and 'divorced' are different?
    d[DetentionsColumns.MARITAL_STATUS.column_name].value_counts()

    missing_percent_print(d, DetentionsColumns.ETHNICITY.column_name)

    d[DetentionsColumns.ETHNICITY.column_name].value_counts()

    d[DetentionsColumns.ETHNICITY.column_name] = d[DetentionsColumns.ETHNICITY.column_name].apply(lambda x: 'Unknown' if type(x) != str else x)

    d[DetentionsColumns.ETHNICITY.column_name].value_counts()

    missing_percent_print(d, DetentionsColumns.ENTRY_STATUS.column_name)

    c = DetentionsColumns.ENTRY_STATUS.column_name
    d[c] = d[c].replace('Crew - Absconder', 'Crew')
    d[c] = d[c].replace('Crew - Deserter', 'Crew')
    d[c] = d[c].replace('Crew - In transit to conveyance', 'Crew')
    d[c] = d[c].replace('Crew - Working', 'Crew')

    d[c] = d[c].replace('False Claim with Altered Document', 'False Claim')
    d[c] = d[c].replace('False Claim with Counterfeit Document', 'False Claim')
    d[c] = d[c].replace('False Claim with Valid Document', 'False Claim')
    d[c] = d[c].replace('ORAL FALSE CLAIMS TO OTHER THAN U.S. CITZ-', 'False Claim')
    d[c] = d[c].replace('Oral False Claim to U.S. Citizenship', 'False Claim')
    d[c] = d[c].replace('Fraud-Other Than False Claim to USC', 'False Claim')

    d[c] = d[c].replace('United States Citizen-False Claim', 'US Citizen')

    d[c] = d[c].replace('Parolee - CH - Advanced Humanitarian', 'Parolee')
    d[c] = d[c].replace('Parolee - DA - Advanced Parole', 'Parolee')
    d[c] = d[c].replace('Parolee - DT - Port of Entry Parole', 'Parolee')
    d[c] = d[c].replace('Parolee - OP - Overseas Parole', 'Parolee')
    d[c] = d[c].replace('Parolee - Parole as Asylee/Refugee', 'Parolee')
    d[c] = d[c].replace('Parolee- CC - Cuban Adjustment Act', 'Parolee')
    d[c] = d[c].replace('Significant Public Benefit Parole', 'Parolee')

    # https://www.aila.org/library/dhs-and-dos-suspend-transit-without-visa-twov-and-
    # TWOV - transit without visa (program ended in 2003? maybe outdated terminology?)
    d[c] = d[c].replace('TWOV', 'No Documents')

    d[c] = d[c].replace('Other Applicant for Admission', 'Other')
    d[c] = d[c].replace('Other Non-Immigrant Classification', 'Other')

    d[c] = d[c].replace('Refugee - Initial', 'Refugee')

    d[c] = d[c].replace('Temporary Resident', 'Temporary')
    d[c] = d[c].replace('Temporary Work Agriculture', 'Temporary')
    d[c] = d[c].replace('Temporary Worker Other', 'Temporary')

    d[c] = d[c].replace('Present Without Admission', 'PWA Other')

    d[c] = d[c].replace('Lawful Permanent Resident - Seeking admission (OALICE)', 'Legal Permanent Resident')

    # sorted(list(d[DetentionsColumns.ENTRY_STATUS.column_name].value_counts().index))

    d[DetentionsColumns.ENTRY_STATUS.column_name].value_counts()

    # missing_percent_print(d, DetentionsColumns.BOND_POSTED_DATE.column_name)

    # missing_percent_print(d, DetentionsColumns.BOND_POSTED_AMOUNT.column_name)

    missing_percent_print(d, DetentionsColumns.CASE_STATUS.column_name)

    d[DetentionsColumns.CASE_STATUS.column_name].value_counts()

    d[DetentionsColumns.CASE_CATEGORY.column_name].value_counts()

    missing_percent_print(d, DetentionsColumns.CASE_THREAT_LEVEL.column_name)

    d[DetentionsColumns.CASE_THREAT_LEVEL.column_name].value_counts()

    missing_percent_print(d, DetentionsColumns.BOOK_IN_CRIMINALITY.column_name)

    d[DetentionsColumns.BOOK_IN_CRIMINALITY.column_name].value_counts()

    missing_percent_print(d, DetentionsColumns.FINAL_CHARGE.column_name)

    c = DetentionsColumns.FINAL_CHARGE.column_name
    d[c] = d[c].apply(lambda x: x.replace('** ', '') if type(x) == str else x)
    d[c] = d[c].apply(lambda x: x.upper() if type(x) == str else x)

    d[c] = d[c].replace('CONVICTION OF ONE CRIME INVOLVING MORAL TURPITUDE', 'CONVICTION OF CRIME INVOLVING MORAL TURPITUDE')
    d[c] = d[c].replace('CONVICTION OF TWO CRIMES INVOLVING MORAL TURPITUDE', 'CONVICTION OF CRIME INVOLVING MORAL TURPITUDE')
    d[c] = d[c].replace('CONVICTION OR COMMISSION OF A CRIME INVOLVING MORAL TURPITUDE', 'CONVICTION OF CRIME INVOLVING MORAL TURPITUDE')
    d[c] = d[c].replace('MORAL TURPITUDE-1 CONVICTION', 'CONVICTION OF CRIME INVOLVING MORAL TURPITUDE')

    d[c] = d[c].replace('FALSE CLAIM OF UNITED STATES CITIZENSHIP', 'FALSE CLAIM TO U.S. CITIZENSHIP')
    d[c] = d[c].replace('TRAFFICKER IN CONTROLLED SUBSTANCE', 'CONTROLLED SUBSTANCE TRAFFICKERS')
    d[c] = d[c].replace('IMMIGRANT WITHOUT AN IMMIGRANT VISA', 'IMMIGRANT WITHOUT VISA')
    d[c] = d[c].replace('DRUG ABUSER OR ADDICT', 'DRUG CONVICTION')
    d[c] = d[c].replace('NARCOTICS', 'DRUG CONVICTION')
    d[c] = d[c].replace('CONVICTION -- VIOLATION OF NARCOTIC DRUG LAW OR REGULATION', 'DRUG CONVICTION')

    d[c] = d[c].replace('ENTERED WITHOUT INSPECTION', 'ENTRY WITHOUT INSPECTION')
    d[c] = d[c].replace('EWI', 'ENTRY WITHOUT INSPECTION')

    d[c] = d[c].replace('SECURITY AND RELATED GROUNDS:  TERRORIST ACTIVITY', 'TERRORISM RELATED')
    d[c] = d[c].replace('ENGAGED IN TERRORIST ACTIVITY', 'TERRORISM RELATED')
    d[c] = d[c].replace('POLITICAL ENDORSER OF TERRORIST ORGANIZATION', 'TERRORISM RELATED')
    d[c] = d[c].replace('LIKELY TO ENGAGE IN TERRORIST ACTIVITY', 'TERRORISM RELATED')   # ?????

    d[c] = d[c].replace('SECURITY AND RELATED GROUNDS:  ESPIONAGE AND SABOTAGE', 'SECURITY AND RELATED GROUNDS')
    d[c] = d[c].replace('UNLAWFUL ACTIVITY (SECURITY & RELATED GROUNDS)', 'SECURITY AND RELATED GROUNDS')
    d[c] = d[c].replace('SECURITY AND RELATED GROUNDS:  ENDANGERING PUBLIC SAFETY OR NATIONAL SECURITY', 'SECURITY AND RELATED GROUNDS')

    d[c] = d[c].replace('NONIMMIGRANT OVERSTAY: CREWMEMBER', 'NONIMMIGRANT OVERSTAY')
    d[c] = d[c].replace('NONIMMIGRANT -- REMAINED LONGER', 'NONIMMIGRANT OVERSTAY')
    d[c] = d[c].replace('NONIMMIGRANT STUDENT OUT OF STATUS: FAILURE TO ATTEND', 'NONIMMIGRANT STUDENT OUT OF STATUS')
    d[c] = d[c].replace('NONIMMIGRANT STUDENT OUT OF STATUS:  FAILURE TO CARRY FULL COURSE OF STUDY', 'NONIMMIGRANT STUDENT OUT OF STATUS')
    d[c] = d[c].replace('NONIMMIGRANT STATUS VIOLATORS: FAILED TO MAINTAIN THE NONIMMIGRANT STATUS IN WHICH THE ALIEN WAS ADMITTED', 'NONIMMIGRANT STATUS VIOLATORS')
    d[c] = d[c].replace('NONIMMIGRANT FAILURE TO MAINTAIN STATUS AFTER STATUS CHANGED', 'NONIMMIGRANT STATUS VIOLATORS')
    d[c] = d[c].replace('NONIMMIGRANT OUT OF STATUS: MEXICAN BORDER CROSSER', 'NONIMMIGRANT STATUS VIOLATORS')
    d[c] = d[c].replace('FAILURE TO MAINTAIN STATUS:  CRIME OF VIOLENCE UNDER 8 C.F.R. 214.1(G)', 'NONIMMIGRANT STATUS VIOLATORS')
    d[c] = d[c].replace('VIOLATION OF NONIMMIGRANT STATUS - FAILURE TO COMPLY WITH SPECIAL REGISTRATION REQUIREMENTS (NSEERS)', 'NONIMMIGRANT STATUS VIOLATORS')
    d[c] = d[c].replace('FAIL TO MAINTAIN NONIMM STATUS', 'NONIMMIGRANT STATUS VIOLATORS')
    d[c] = d[c].replace('NON-IMMIGRANT STATUS VIOLATOR', 'NONIMMIGRANT STATUS VIOLATORS')

    d[c] = d[c].replace('ALIEN PRESENT WITHOUT ADMISSION OR PAROLE - (PWAS)', 'ALIEN PRESENT WITHOUT ADMISSION OR PAROLE')
    d[c] = d[c].replace('ALIEN PRESENT IN THE UNITED STATES WHO WAS NOT ADMITTED OR PAROLED OR ARRIVING IN THE UNITED STATES AT A TIME OR PLACE NOT DESIGNATED BY THE AG - (212)(A)(6)(A)', 'ALIEN PRESENT WITHOUT ADMISSION OR PAROLE')

    d[c] = d[c].replace('FRAUD AND MISUSE OF VISAS, PERMITS AND OTHER DOCUMENTS:  CONVICTED UNDER 18 USC 1546', 'FRAUD OR WILLFUL MISREPRESENTATION')
    d[c] = d[c].replace('ALIEN PRESENT IN THE UNITED STATES WHO WAS NOT ADMITTED OR PAROLED OR ARRIVING IN THE UNITED STATES AT A TIME OR PLACE NOT DESIGNATED BY THE AG - (212)(A)(6)(A)', 'ALIEN PRESENT WITHOUT ADMISSION OR PAROLE')

    d[DetentionsColumns.FINAL_CHARGE.column_name].value_counts()

    [x for x in d[DetentionsColumns.FINAL_CHARGE.column_name].unique() if type(x) == str and 'STATUS' in x]

    missing_percent_print(d, DetentionsColumns.FINAL_PROGRAM.column_name)

    c = DetentionsColumns.FINAL_PROGRAM.column_name
    d[c] = d[c].replace('Inspections - Land', 'Inspections')
    d[c] = d[c].replace('Inspections - Air', 'Inspections')
    d[c] = d[c].replace('Inspections - Sea', 'Inspections')

    d[c] = d[c].replace('287G Program', '287g Task Force')

    d[c] = d[c].replace('Mobile Criminal Alien Team', 'Fugitive Operations')
    d[c] = d[c].replace('Violent Criminal Alien Section', 'ERO Criminal Prosecutions')

    d[DetentionsColumns.FINAL_PROGRAM.column_name].value_counts()

    missing_percent_print(d, DetentionsColumns.MSC_CHARGE.column_name)

    d[DetentionsColumns.MSC_CHARGE.column_name].value_counts()

    # most of these values appear clean/normalized, but we could enrich the data with a "MSC" category
    # that is more general than the specific MSCs

    d['Stay Book In Month'] = pd.Categorical(d[DetentionsColumns.STAY_BOOK_IN_DATE_TIME.column_name].dt.month_name(), categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)


def combine_duplicate_ids(df):
    initial_rows = df.shape[0]
    arrest_counts = df['Unique Identifier'].value_counts()
    df['Num Detentions'] = df['Unique Identifier'].map(arrest_counts)
    df.sort_values('Stay Book In Date Time', ascending=False, inplace=True)
    df.drop_duplicates(subset='Unique Identifier', keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    rows_removed = initial_rows - df.shape[0]
    print("Removed %d duplicate rows, keeping only most recent detention per individual" % rows_removed)
    print("Dataframe now has %d rows" % df.shape[0])
