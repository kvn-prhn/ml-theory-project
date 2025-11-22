"""
This is the script form of encounters_cleaning.ipynb. See that file for more
explanation and assumptions behind the cleaning
"""

import pandas as pd
from utils import log
import clean_utils

START_DATE = pd.to_datetime('2023-09-01 00:00:00')

def cleanEventDate(df):
    log("="*40)
    log("Processing 'Event Date' column")
    event_dates = df['Event Date']
    rows_before = df.shape[0]
    valid_dates_mask = (pd.to_datetime('2023-9-1') <= event_dates) & (event_dates <= pd.to_datetime('2025-7-31'))
    invalid_count = (df.shape[0] - valid_dates_mask.sum())
    log("dropping %d rows with invalid dates" % invalid_count)
    df.drop(df[~valid_dates_mask].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    rows_after = df.shape[0]
    log("Rows before drop: %d" % rows_before)
    log("Rows after drop: %d" % rows_after)

def cleanResponsibleSite(df):
    log("="*40)
    log("Processing 'Responsible Site' column")
    responsible_site = df['Responsible Site']
    log("%s unique values before cleaning" % responsible_site.nunique())
    responsible_site.replace('SACRAMENTO, CA, SUB-OFFICE', 'ERO - Sacramento, CA Sub Office', inplace=True)
    responsible_site.replace('SAN BERNADINO, CA, SUB-OFFICE', 'ERO - San Bernardino, CA Sub Office', inplace=True)
    responsible_site.replace('SANTA ANA, CA, SUB-OFFICE', 'ERO - Santa Ana, CA Sub-Office', inplace=True)
    responsible_site.replace('ST. LOUIS, MO, SUB-OFFICE', 'ERO - St. Louis, MO Sub-Office', inplace=True)
    responsible_site.replace('SAVANNAH, GA, SUB-OFFICE', 'ERO - Savannah, GA Sub-Office', inplace=True)
    responsible_site.replace('LOUISVILLE, KY, SUB-OFFICE', 'ERO - Louisville, KY Sub-Office', inplace=True)
    responsible_site.replace('MILWAUKEE, WI, SUB-OFFICE', 'ERO - Milwaukee, WI Sub-Office', inplace=True)
    responsible_site.replace('FRESNO, CA, SUB-OFFICE', 'ERO - Fresno, CA Sub Office', inplace=True)
    responsible_site.replace('YAKIMA, WA, SUB-OFFICE', 'ERO - Yakima, WA Sub-Office', inplace=True)
    responsible_site.replace('GRAND JUNCTION, CO, SUB-OFFICE', 'ERO - Grand Junction, CO Sub-Office', inplace=True)
    responsible_site.replace('WICHITA, KS, SUB-OFFICE', 'ERO - Wichita, KS Sub-Office', inplace=True)
    responsible_site.replace('MEDFORD, OR, SUB-OFFICE', 'ERO - Medford, OR Sub Office', inplace=True)
    responsible_site.replace('BAKERSFIELD CA IHP', 'ERO - Bakersfield, CA IHP Sub Office', inplace=True)
    responsible_site.replace('RALEIGH/DURHAM, NC, SUB-OFFICE', 'ERO - Raleigh/Durham, NC Sub-Office', inplace=True)
    log("%s unique values after cleaning" % responsible_site.nunique())

def cleanLeadSource(df):
    log("="*40)
    log("dropping Lead Source column")
    df.drop(columns='Lead Source', axis=1, inplace=True)

def clean_lead_event_type(df):
    log("="*40)
    log("dropping 'Lead Event Type' column")
    df.drop(columns='Lead Event Type', axis=1, inplace=True)

def cleanFinalProgram(df):
    log("="*40)
    log("cleaning 'Final Program' column")
    final_program = df['Final Program']
    final_program.replace('287g Task Force', '287G Program', inplace=True)
    final_program.replace('Joint Criminal Alien Response Team', 'Mobile Criminal Alien Team', inplace=True)
    log("%d unique values after cleaning" % final_program.unique().size)

def cleanCitizenshipCountry(df):
    log("="*40)
    log("cleaning 'Citizenship Country' column")
    citizenship_country = df['Citizenship Country']
    clean_utils.clean_countries(citizenship_country)

def cleanEventLandmark(df):
    log("="*40)
    log("dropping 'Event Landmark' column")
    df.drop(columns='Event Landmark', axis=1, inplace=True)

def clean_responsible_site(df):
    log("="*40)
    log("dropping 'Responsible Site' column. According to the cookbook: \n'We believe that this typically indicates the docket control office, \nwhich is a sub-office within an area of responsibility; we do not know \nmore details. Some discussion of docket control offices is available \nhere: https://www.ice.gov/doclib/foia/dro_policy_memos/09684drofieldpolicymanual.pdf.'.\n A lot of this information seems to be contained in the 'Responsible AOR' column")
    df.drop(columns='Responsible Site', axis=1, inplace=True)

def clean_processing_disposition(df):
    log("="*40)
    log("dropping 'Processing Disposition' column. According to the \ncookbook, 'We are unsure how to understand the values in this field, \nespecially in relation to case category.'")
    df.drop(columns='Processing Disposition', axis=1, inplace=True)

def create_deported_column(df):
    log("Creating 'Deported' column")
    df['Deported'] = df['Departed Date'].notna()

def clean_birth_year(df):
    log("="*40)
    log("Converting 'Birth Year' column to integer type")
    df['Birth Year'] = df['Birth Year'].astype('Int16')

def clean_responsible_aor(df):
    log("="*40)
    log("Cleaning 'Responsible AOR' column")
    rows_before = df.shape[0]
    df.dropna(subset=['Responsible AOR'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    rows_after = df.shape[0]
    log("Rows before drop: %d" % rows_before)
    log("Rows after drop: %d" % rows_after)
    log("Dropped %d rows with missing 'Responsible AOR'" % (rows_before - rows_after))

def create_days_after_start(df):
    log("="*40)
    log("Creating 'Days After Start' column")
    df['Days After Start'] = (df['Event Date'] - START_DATE).dt.days.astype('int32')

def clean_gender(df):
    log("="*40)
    log("Cleaning 'Gender' Column")
    rows_before = df.shape[0]
    df.drop(df[df['Gender'] == 'Unknown'].index, inplace=True)
    df.reset_index(drop=True, inplace=True)
    rows_after = df.shape[0]
    rows_removed = rows_before - rows_after
    log("Rows before drop: %d" % rows_before)
    log("Rows after drop: %d" % rows_after)
    log("Removed %d rows with 'Unknown' gender" % rows_removed)

def create_event_month(df):
    log("="*40)
    log("Creating 'Event Month' column")
    df['Event Month'] = pd.Categorical(df['Event Date'].dt.month_name(), categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

def clean_encounters(df):
    log("="*40)
    log("Cleaning Encounters dataframe")
    cleanEventLandmark(df)
    cleanLeadSource(df)
    cleanEventDate(df)
    cleanFinalProgram(df)
    cleanCitizenshipCountry(df)
    cleanResponsibleSite(df)
    create_deported_column(df)
    clean_birth_year(df)
    clean_responsible_aor(df)
    clean_lead_event_type(df)
    create_days_after_start(df)
    clean_processing_disposition(df)
    clean_responsible_site(df)
    clean_gender(df)
    create_event_month(df)

def combine_duplicate_ids(df):
    initial_rows = df.shape[0]
    arrest_counts = df['Unique Identifier'].value_counts()
    df['Num Encounters'] = df['Unique Identifier'].map(arrest_counts)
    df.sort_values('Event Date', ascending=False, inplace=True)
    df.drop_duplicates(subset='Unique Identifier', keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    rows_removed = initial_rows - df.shape[0]
    log("Removed %d duplicate rows, keeping only most recent encounter per individual" % rows_removed)
    log("Dataframe now has %d rows" % df.shape[0])
