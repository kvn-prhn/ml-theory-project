import pandas as pd
import numpy as np
import pathlib
import re
from datetime import datetime
from arrests_columns import ArrestsColumns

def missing_percent_print(d, col_name):
    print(f"{col_name}, {(d[col_name].isnull().sum() / len(d)).item() * 100:.4}% missing values")

# repeat the same country string replacements

def update_country_strings(df, col_name):
    df[col_name] = df[col_name].replace('PALESTINE BORN BEFORE 1948', 'PALESTINE')
    df[col_name] = df[col_name].replace('Palestine', 'PALESTINE')
    
    # Soveirgn states and territories
    df[col_name] = df[col_name].replace('CHINA, PEOPLES REPUBLIC OF', 'CHINA')
    df[col_name] = df[col_name].replace('HONG KONG', 'CHINA')
    df[col_name] = df[col_name].replace('MACAU', 'CHINA')
    df[col_name] = df[col_name].replace('BRITISH VIRGIN ISLANDS', 'UNITED KINGDOM')
    df[col_name] = df[col_name].replace('BERMUDA', 'UNITED KINGDOM')
    df[col_name] = df[col_name].replace('NETHERLANDS ANTILLES', 'NETHERLANDS')
    df[col_name] = df[col_name].replace('SAINT MARTIN(FRENCH)', 'FRANCE')
    df[col_name] = df[col_name].replace('FRENCH POLYNESIA', 'FRANCE')
    df[col_name] = df[col_name].replace('GUADELOUPE', 'FRANCE')
    df[col_name] = df[col_name].replace('SAINT BARTHELEMY', 'FRANCE')
    df[col_name] = df[col_name].replace('NEW CALEDONIA', 'FRANCE')
    df[col_name] = df[col_name].replace('REUNION', 'FRANCE')
    df[col_name] = df[col_name].replace('FRENCH GUIANA', 'FRANCE')
    df[col_name] = df[col_name].replace('SINT MAARTEN(DUTCH)', 'NETHERLANDS')
    df[col_name] = df[col_name].replace('ARUBA', 'NETHERLANDS')
    df[col_name] = df[col_name].replace('SINT EUSTATIUS', 'NETHERLANDS')
    df[col_name] = df[col_name].replace('SABA', 'NETHERLANDS')
    df[col_name] = df[col_name].replace('BONAIRE', 'NETHERLANDS')
    df[col_name] = df[col_name].replace('CURACAO', 'NETHERLANDS')
    df[col_name] = df[col_name].replace('TURKS AND CAICOS ISLANDS', 'UNITED KINGDOM')
    df[col_name] = df[col_name].replace('CAYMAN ISLANDS', 'UNITED KINGDOM')
    df[col_name] = df[col_name].replace('MONTSERRAT', 'UNITED KINGDOM')
    df[col_name] = df[col_name].replace('ANGUILLA', 'UNITED KINGDOM')
    df[col_name] = df[col_name].replace('ST. HELENA', 'UNITED KINGDOM')
    df[col_name] = df[col_name].replace('CHRISTMAS ISLAND', 'AUSTRALIA')
    # note: "DEM REP OF CONGO" is a different country from "CONGO" which I assume is the republic of congo

def clean_arrests(d):
    use_cols = [v.value[0] for k, v in ArrestsColumns.__members__.items() if not v.value[2] and not v.value[3]]
    print(f'{use_cols=}')
    d = d[use_cols].copy()
    d.head()

    update_country_strings(d, ArrestsColumns.CITIZENSHIP_COUNTRY.column_name)

    missing_percent_print(d, ArrestsColumns.CITIZENSHIP_COUNTRY.column_name)

    missing_percent_print(d, ArrestsColumns.APPREHENSION_AOR.column_name)
    # sorted(list(d[~d[ArrestsColumns.APPREHENSION_AOR.column_name].isna()][ArrestsColumns.APPREHENSION_AOR.column_name].unique()))

    # this field includes U.S. territories, a state in mexico, and tags for arrests in "ARMED FORCES" areas outside the U.S.
    missing_percent_print(d, ArrestsColumns.APPREHENSION_STATE.column_name)
    # sorted(list(d[~d[ArrestsColumns.APPREHENSION_STATE.column_name].isna()][ArrestsColumns.APPREHENSION_STATE.column_name].unique()))

    missing_percent_print(d, ArrestsColumns.FINAL_PROGRAM.column_name)

    # under the same same program?
    d[ArrestsColumns.FINAL_PROGRAM.column_name] = d[ArrestsColumns.FINAL_PROGRAM.column_name].replace('287G Program', '287g Task Force')
    # https://www.ice.gov/identify-and-arrest/fugitive-operations
    # another name for the "Mobile criminal apprehension teams"?
    d[ArrestsColumns.FINAL_PROGRAM.column_name] = d[ArrestsColumns.FINAL_PROGRAM.column_name].replace('Mobile Criminal Alien Team', 'Fugitive Operations')
    # "Violent Criminal Alien Section (VCAS)" is under the "Criminal Alien program"
    d[ArrestsColumns.FINAL_PROGRAM.column_name] = d[ArrestsColumns.FINAL_PROGRAM.column_name].replace('Violent Criminal Alien Section', 'ERO Criminal Prosecutions')
    # https://portal.ice.gov/immigration-guide/atd

    d[ArrestsColumns.FINAL_PROGRAM.column_name].value_counts()

    missing_percent_print(d, ArrestsColumns.APPREHENSION_METHOD.column_name)

    # filter out "Criminal Alien Program" completely because it's too generic
    d = d[d[ArrestsColumns.APPREHENSION_METHOD.column_name] != 'Criminal Alien Program'].copy()
    # assume several categories are the same
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Transportation Check Bus', 'Traffic Check')
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Transportation Check Passenger Train', 'Traffic Check')
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Transportation Check Aircraft', 'Traffic Check')
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Presented During Inspection', 'Inspections')
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Crewman/Stowaway', 'Inspections')
    # put remaining tiny categories into 'Other efforts' category
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Boat Patrol', 'Other efforts')
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Patrol Interior', 'Other efforts')
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Other Task Force', 'Other efforts')
    d[ArrestsColumns.APPREHENSION_METHOD.column_name] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].replace('Other Agency (turned over to INS)', 'Other efforts')

    d[ArrestsColumns.APPREHENSION_METHOD.column_name].value_counts()

    d['Jail Apprehension'] = d[ArrestsColumns.APPREHENSION_METHOD.column_name].isin(['CAP Federal Incarceration', 'CAP Local Incarceration', 'CAP State Incarceration'])

    missing_percent_print(d, ArrestsColumns.APPREHENSION_CRIMINALITY.column_name)

    d[ArrestsColumns.APPREHENSION_CRIMINALITY.column_name].value_counts()

    missing_percent_print(d, ArrestsColumns.CASE_STATUS.column_name)

    # these have different codes but different meanings?
    # so it's probably find to combine them?
    d[ArrestsColumns.CASE_STATUS.column_name] = d[ArrestsColumns.CASE_STATUS.column_name].replace('Z-SAW - Permanent Residence Granted', 'L-Legalization - Permanent Residence Granted')

    d[ArrestsColumns.CASE_STATUS.column_name].value_counts()

    missing_percent_print(d, ArrestsColumns.CASE_CATEGORY.column_name)

    d[ArrestsColumns.CASE_CATEGORY.column_name].value_counts()

    # consistent date filtering
    d = d[d[ArrestsColumns.DEPARTED_DATE.column_name].isna() |
        ((pd.to_datetime('2023-9-1') <= d[ArrestsColumns.DEPARTED_DATE.column_name]) & 
        (d[ArrestsColumns.DEPARTED_DATE.column_name] <= pd.to_datetime('2025-7-31')))].copy()

    d[ArrestsColumns.DEPARTED_DATE.column_name].value_counts()

    # departure country/date == null means they haven't been deported yet
    d[ArrestsColumns.DEPARTED_DATE.column_name].isna().value_counts()

    missing_percent_print(d, ArrestsColumns.DEPARTURE_COUNTRY.column_name)
    update_country_strings(d, ArrestsColumns.DEPARTURE_COUNTRY.column_name)

    d[ArrestsColumns.DEPARTURE_COUNTRY.column_name].value_counts()

    # sorted(list(d[~d[ArrestsColumns.DEPARTURE_COUNTRY.column_name].isna()][ArrestsColumns.DEPARTURE_COUNTRY.column_name].unique()))

    missing_percent_print(d, ArrestsColumns.GENDER.column_name)

    missing_percent_print(d, ArrestsColumns.APPREHENSION_SITE_LANDMARK.column_name)

    # download states table if needed
    if not pathlib.Path('states.csv').exists():
        import requests
        with requests.get('https://raw.githubusercontent.com/jasonong/List-of-US-States/refs/heads/master/states.csv') as r:
            with open('states.csv', 'wb') as f:
                f.write(r.content)
    states_d = pd.read_csv('states.csv')
    states_d['State_Upper'] = states_d['State'].apply(lambda x: x.upper())

    apprsl_d = d[~d[ArrestsColumns.APPREHENSION_SITE_LANDMARK.column_name].isna()][[ArrestsColumns.APPREHENSION_SITE_LANDMARK.column_name]].drop_duplicates().copy()
    c = ArrestsColumns.APPREHENSION_SITE_LANDMARK.column_name
    apprsl_d['repl_val'] = apprsl_d[c].apply(lambda x: x.strip())
    # some strings end with full state name instead of abbreviation.
    # https://github.com/jasonong/List-of-US-States/blob/master/states.csv

    # if the string ends with a full state name, then repale it with the abbreviation
    def str_end_state_to_abbr(x):
        for i, r in states_d.iterrows():
            if x.endswith(f" {r['State_Upper']}"):
                # print(x)
                return x.replace(r['State_Upper'], r['Abbreviation'])
        return x

    apprsl_d['repl_val'] = apprsl_d['repl_val'].apply(str_end_state_to_abbr)

    apprsl_d['repl_val'] = apprsl_d['repl_val'].apply(lambda x: x.upper())
    apprsl_d['repl_val'] = apprsl_d['repl_val'].apply(lambda x: x[:-len(' STATE')] if x.endswith(' STATE') else x)
    # sometimes, the states at end of strings have a comma and sometimes they don't
    # assume if the string ends with an  upper case 2 letter string, then it's a state 
    # and we can add a comma to try normalizing it
    def add_comma_before_state_abbrev(x):
        m = re.search('[A-Z] ([A-Z][A-Z])$', x)
        if m:
            return f'{x[:-3]}, {m.groups(0)[0]}'
        return x

    # 'CAP-String', 'CAP String' => 'CAP - String'
    apprsl_d['repl_val'].apply(lambda x: x.replace('CAP-', 'CAP - ', count=1) if x.startswith('CAP-') else x)
    apprsl_d['repl_val'].apply(lambda x: x.replace('CAP ', 'CAP - ', count=1) if x.startswith('CAP ') else x)

    apprsl_d['repl_val'] = apprsl_d['repl_val'].apply(add_comma_before_state_abbrev)

    d = d.merge(apprsl_d, on = ArrestsColumns.APPREHENSION_SITE_LANDMARK.column_name, how = 'left')
    d[ArrestsColumns.APPREHENSION_SITE_LANDMARK.column_name] = d['repl_val']
    d = d.drop('repl_val', axis = 1).copy()

def combine_duplicate_ids(df):
    initial_rows = df.shape[0]
    arrest_counts = df['Unique Identifier'].value_counts()
    df['Num Arrests'] = df['Unique Identifier'].map(arrest_counts)
    df.sort_values('Apprehension Date', ascending=False, inplace=True)
    df.drop_duplicates(subset='Unique Identifier', keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    rows_removed = initial_rows - df.shape[0]
    print("Removed %d duplicate rows, keeping only most recent arrest per individual" % rows_removed)
    print("Dataframe now has %d rows" % df.shape[0])



