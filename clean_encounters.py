"""
This is the script form of encounters_cleaning.ipynb. See that file for more
explanation and assumptions behind the cleaning
"""

import pandas as pd
import clean_utils

def cleanEventDate(df):
    print("="*40)
    print("Processing 'Event Date' column")
    event_dates = df['Event Date']
    print("before cleaning, %f%% missing values" % (100 * event_dates.isnull().sum() / df.shape[0]))
    valid_dates_mask = (pd.to_datetime('2023-9-1') <= event_dates) & (event_dates <= pd.to_datetime('2025-7-31'))
    print("marking %d invalid dates as null" % (df.shape[0] - valid_dates_mask.sum()))
    df.loc[~valid_dates_mask, 'Event Date'] = pd.NaT
    print("after cleaning, %f%% missing values" % (100 * event_dates.isnull().sum() / df.shape[0]))

def cleanResponsibleSite(df):
    print("="*40)
    print("Processing 'Responsible Site' column")
    responsible_site = df['Responsible Site']
    print("%s unique values before cleaning" % responsible_site.nunique())
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
    print("%s unique values after cleaning" % responsible_site.nunique())

def cleanLeadSource(df):
    print("="*40)
    print("dropping Lead Source column")
    df.drop(columns='Lead Source', axis=1, inplace=True)

def cleanFinalProgram(df):
    print("="*40)
    print("cleaning 'Final Program' column")
    final_program = df['Final Program']
    final_program.replace('287g Task Force', '287G Program', inplace=True)
    final_program.replace('Joint Criminal Alien Response Team', 'Mobile Criminal Alien Team', inplace=True)
    print("%d unique values after cleaning" % final_program.unique().size)

def cleanCitizenshipCountry(df):
    print("="*40)
    print("cleaning 'Citizenship Country' column")
    citizenship_country = df['Citizenship Country']
    clean_utils.clean_countries(citizenship_country)

def cleanEventLandmark(df):
    print("="*40)
    print("dropping 'Event Landmark' column")
    df.drop(columns='Event Landmark', axis=1, inplace=True)

def clean_encounters(df):
    print("="*40)
    print("Cleaning Encounters dataframe")
    cleanEventLandmark(df)
    cleanLeadSource(df)
    cleanEventDate(df)
    cleanFinalProgram(df)
    cleanCitizenshipCountry(df)
    cleanResponsibleSite(df)
