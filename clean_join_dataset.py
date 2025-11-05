# take all of the dataset cleaning work from other notebooks to one large clean, reduced dataset
import pandas as pd
import pathlib
import numpy as np
import pathlib
import re
import os
from datetime import datetime

from detentions_columns import DetentionsColumns
from arrests_columns import ArrestsColumns


input_dir = pathlib.Path('proc_data')
assert input_dir.exists()

output_dir = pathlib.Path('clean_data')
if not output_dir.exists():
    output_dir.mkdir()


print(f'{output_dir=}')

### Common Functions ###
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
    return df


def update_apprehension_landmark(df, c):
    # download states table if needed
    # https://github.com/jasonong/List-of-US-States/blob/master/states.csv
    if not pathlib.Path('states.csv').exists():
        import requests
        with requests.get('https://raw.githubusercontent.com/jasonong/List-of-US-States/refs/heads/master/states.csv') as r:
            with open('states.csv', 'wb') as f:
                f.write(r.content)
    states_d = pd.read_csv('states.csv')
    states_d['State_Upper'] = states_d['State'].apply(lambda x: x.upper())

    apprsl_d = df[~df[c].isna()][[c]].drop_duplicates().copy()
    apprsl_d['repl_val'] = apprsl_d[c].apply(lambda x: x.strip())
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
    result = df.copy()
    result = result.merge(apprsl_d, on = c, how = 'left')
    result[c] = result['repl_val']
    result = result.drop('repl_val', axis = 1).copy()
    return result


# TODO msc charge clean

def update_case_status(d, c):
    result = d.copy()
    result[c].map({'ACTIVE':"Pending", '8-Excluded/Removed - Inadmissibility':"Deported",
           '6-Deported/Removed - Deportability':"Deported",
           '3-Voluntary Departure Confirmed':"Deported", '9-VR Witnessed':"Pending",
           'E-Charging Document Canceled by ICE':"Remained", 'A-Proceedings Terminated':'Remained',
           'B-Relief Granted':"Remained", '0-Withdrawal Permitted - I-275 Issued':"Deported",
           '7-Died':"Other", 'L-Legalization - Permanent Residence Granted':"Remained",
           '5-Title 50 Expulsion':"Deported", 'Z-SAW - Permanent Residence Granted':'Remained'})
    return result

def update_criminality(d, c):
    result = d.copy()
    result[c].map({'1 Convicted Criminal':"Criminal", '2 Pending Criminal Charges':"Pending Criminal", '3 Other Immigration Violator':"Other"})
    return result

def update_msc_charge(d, c):
    result = d.copy()
    MSC_CATEGORY_PATTERNS = {
    	'HOMICIDE': r'\bHOMICIDE|MANSLAUGHTER\b',
    	'SEX_OFFENSE': r'\bRAPE|SEX(?!\s*OFFENDER\s*REG)|SODOMY|LEWD|LASCIVIOUS|MOLEST|INDECENT|PROSTITUTION|COMMERCIAL SEX|PORN|OBSCENE|EXHIBITION|FONDLING\b',
    	'ASSAULT': r'\bASSAULT|BATTERY\b',
    	'ROBBERY': r'\bROBBERY|CARJACK\b',
    	'BURGLARY': r'\bBURGLARY\b',
    	'THEFT_FRAUD': r'\bLARCENY|THEFT|SHOPLIFT|STOLEN PROPERTY|EMBEZZLE|FRAUD|FORGERY|COUNTERFEIT|IDENTITY THEFT|RICO\b',
    	'DRUG_POSSESSION': r'\b(NARCOTIC|COCAINE|HEROIN|MARIJUANA|DRUG|OPIUM|AMPHETAMINE|HALLUCINOGEN).*(POSSESSION)\b',
    	'DRUG_TRAFFICK': r'\bSELL|SMUGGL|MANUFACTUR|DISTRIBUTION|TRAFFICK\b',
    	'WEAPONS': r'\bWEAPON|FIRING WEAPON|EXPLOSIVE|AMMUNITION\b',
    	'IMMIGRATION': r'\bIMMIGRATION|ILLEGAL\s*RE?-?ENTRY|ILLEGAL ENTRY|SMUGGLING ALIENS\b',
    	'PUBLIC_ORDER': r'\bDISORDERLY|TRESPASS|PUBLIC PEACE|OBSTRUCT|CONTEMPT|VIOLATION OF A COURT ORDER|PAROLE|PROBATION|ESCAPE|FAILURE TO APPEAR|RIOT\b',
    	'TRAFFIC': r'\bDUI|DRIVING UNDER INFLUENCE|HIT AND RUN|TRAFFIC OFFENSE\b',
    	'KIDNAPPING': r'\bKIDNAP|ABDUCT\b',
    	'ARSON': r'\bARSON|INCENDIARY DEVICE\b',
    	'TERRORISM': r'\bTERRORISM|SABOTAGE|ESPIONAGE|TREASON\b',
    	'ENVIRONMENT': r'\bCONSERVATION|ENVIRONMENT|FISH\b'
    }
    MSC_VIOLENT = {'HOMICIDE','SEX_OFFENSE','ASSAULT','ROBBERY','KIDNAPPING','WEAPONS'}
     
    def _u(x):
    	if pd.isna(x):
    		return None
    	s = str(x).strip().upper()
    	s = re.sub(r'\s+', ' ', s)
    	return s or None
    
    def _categorize_msc(text):
    	t = _u(text)
    	if t is None:
    		return None
    	for cat, pat in MSC_CATEGORY_PATTERNS.items():
    		if re.search(pat, t):
    			sub = 'TRAFFICK' if (cat in {'DRUG_TRAFFICK'} or (cat == 'DRUG_POSSESSION' and re.search(r'\bSELL|SMUGGL|MANUFACTUR|DISTRIBUTION|TRAFFICK\b', t))) else None
    			violent = 1 if cat in MSC_VIOLENT else 0
    			if cat == 'DRUG_POSSESSION':
    				cat_out = 'DRUG_POSSESSION'
    			elif cat == 'DRUG_TRAFFICK':
    				cat_out = 'DRUG_TRAFFICK'
    			else:
    				cat_out = cat
    			return cat_out
    	return 'OTHER'
    
    result[c].map(_categorize_msc)
    return result


### Cleaning Functions ###
def encounters_clean(output_file):
    if output_file.exists():
        print(output_file, 'already exists')
        return
    print('encounters_clean()')
    
    # encounters_df = pd.read_parquet('ice_data/proc_data/encounters.parquet')
    encounters_df = pd.read_parquet(input_dir / 'encounters.parquet')
    include_cols = []
    NUM_ROWS = encounters_df.shape[0]
    NUM_COLS = encounters_df.shape[1]
    
    print("num rows: %d" % NUM_ROWS)
    print("num cols: %d" % NUM_COLS)
    print("Column headers: %s" % encounters_df.columns)
    
    event_dates = encounters_df['Event Date']
    valid_dates_mask = (pd.to_datetime('2023-9-1') <= event_dates) & (event_dates <= pd.to_datetime('2025-7-31'))
    encounters_df.loc[~valid_dates_mask, 'Event Date'] = pd.NaT
    include_cols.append('Event Date')
    
    include_cols.append('Responsible AOR')
    
    responsible_site = encounters_df['Responsible Site']
    
    # Assuming "... SUB-OFFICE" and "ERO - ... Sub Office" are the same
    responsible_site.replace('SACRAMENTO, CA, SUB-OFFICE', 'ERO - Sacramento, CA Sub Office', inplace=True)
    responsible_site.replace('SAN BERNADINO, CA, SUB-OFFICE', 'ERO - San Bernardino, CA Sub Office', inplace=True)  # Also fixes spelling
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
    include_cols.append('Responsible Site')
    
    include_cols.append('Event Type')
    
    final_program = encounters_df['Final Program']
    final_program.replace('287g Task Force', '287G Program', inplace=True)
    final_program.replace('Joint Criminal Alien Response Team', 'Mobile Criminal Alien Team', inplace=True)
    include_cols.append('Final Program')
    
    include_cols.append('Encounter Criminality')
    include_cols.append('Processing Disposition')
    include_cols.append('Departed Date')
    include_cols.append('Departure Country')
    include_cols.append('Final Order Yes No')
    include_cols.append('Final Order Date')
    include_cols.append('Birth Year')
    
    encounters_df = update_country_strings(encounters_df, 'Citizenship Country')
    
    include_cols.append('Gender')
    # include_cols.append('Event Landmark')
    include_cols.append('Unique Identifier')
    
    encounters_df[include_cols].to_parquet(output_file)
    print(output_file)


def arrests_clean(output_file):
    if output_file.exists():
        print(output_file, 'already exists')
        return
    print('arrests_clean()')
    
    # encounters_df = pd.read_parquet('ice_data/proc_data/encounters.parquet')
    d = pd.read_parquet(input_dir / 'arrests.parquet')
    use_cols = [v.value[0] for k, v in ArrestsColumns.__members__.items() if not v.value[2] and not v.value[3]]
    d = d[use_cols].copy()
    include_cols = []

    d = update_country_strings(d, ArrestsColumns.CITIZENSHIP_COUNTRY.column_name)
    include_cols.append(ArrestsColumns.CITIZENSHIP_COUNTRY.column_name)

    include_cols.append(ArrestsColumns.APPREHENSION_AOR.column_name)
    include_cols.append(ArrestsColumns.APPREHENSION_STATE.column_name)

    d[ArrestsColumns.FINAL_PROGRAM.column_name] = d[ArrestsColumns.FINAL_PROGRAM.column_name].replace('287G Program', '287g Task Force')
    # https://www.ice.gov/identify-and-arrest/fugitive-operations
    # another name for the "Mobile criminal apprehension teams"?
    d[ArrestsColumns.FINAL_PROGRAM.column_name] = d[ArrestsColumns.FINAL_PROGRAM.column_name].replace('Mobile Criminal Alien Team', 'Fugitive Operations')
    # "Violent Criminal Alien Section (VCAS)" is under the "Criminal Alien program"
    d[ArrestsColumns.FINAL_PROGRAM.column_name] = d[ArrestsColumns.FINAL_PROGRAM.column_name].replace('Violent Criminal Alien Section', 'ERO Criminal Prosecutions')
    # https://portal.ice.gov/immigration-guide/atd
    include_cols.append(ArrestsColumns.FINAL_PROGRAM.column_name)

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
    include_cols.append(ArrestsColumns.APPREHENSION_METHOD.column_name)

    d = update_criminality(d, ArrestsColumns.APPREHENSION_CRIMINALITY.column_name)
    include_cols.append(ArrestsColumns.APPREHENSION_CRIMINALITY.column_name)
    
    d[ArrestsColumns.CASE_STATUS.column_name] = d[ArrestsColumns.CASE_STATUS.column_name].replace('Z-SAW - Permanent Residence Granted', 'L-Legalization - Permanent Residence Granted')
    include_cols.append(ArrestsColumns.CASE_STATUS.column_name)

    # consistent date filtering
    d = d[d[ArrestsColumns.DEPARTED_DATE.column_name].isna() |
          ((pd.to_datetime('2023-9-1') <= d[ArrestsColumns.DEPARTED_DATE.column_name]) & 
          (d[ArrestsColumns.DEPARTED_DATE.column_name] <= pd.to_datetime('2025-7-31')))].copy()
    include_cols.append(ArrestsColumns.DEPARTED_DATE.column_name)

    d = update_country_strings(d, ArrestsColumns.DEPARTURE_COUNTRY.column_name)
    include_cols.append(ArrestsColumns.DEPARTURE_COUNTRY.column_name)

    # TODO apprehension site function here
    d = update_apprehension_landmark(d, ArrestsColumns.APPREHENSION_SITE_LANDMARK.column_name)
    include_cols.append(ArrestsColumns.APPREHENSION_SITE_LANDMARK.column_name)

    include_cols.append('Unique Identifier')
    
    d[include_cols].to_parquet(output_file)
    print(output_file)


def detentions_clean(output_file):
    if output_file.exists():
        print(output_file, 'already exists')
        return
    print('detentions_clean()')

    d = pd.read_parquet(input_dir / 'detentions.parquet')
    use_cols = [v.value[0] for k, v in DetentionsColumns.__members__.items() if not v.value[2] and not v.value[3]]
    d = d[use_cols].copy()
    include_cols = []
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
    include_cols.append(DetentionsColumns.STAY_BOOK_IN_DATE_TIME.column_name)
    include_cols.append(DetentionsColumns.BOOK_IN_DATE_TIME.column_name)
    include_cols.append(DetentionsColumns.STAY_BOOK_OUT_DATE_TIME.column_name)
    include_cols.append(DetentionsColumns.STAY_BOOK_OUT_DATE.column_name)
    
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
        return d
    
    d = release_reason_replace(d, DetentionsColumns.DETENTION_RELEASE_REASON.column_name)
    include_cols.append(DetentionsColumns.STAY_RELEASE_REASON.column_name)
    include_cols.append(DetentionsColumns.MARITAL_STATUS.column_name)
    
    d[DetentionsColumns.ETHNICITY.column_name] = d[DetentionsColumns.ETHNICITY.column_name].apply(lambda x: 'Unknown' if type(x) != str else x)
    include_cols.append(DetentionsColumns.ETHNICITY.column_name)
    
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
    include_cols.append(DetentionsColumns.ENTRY_STATUS.column_name)

    d = update_case_status(d, DetentionsColumns.CASE_STATUS.column_name)
    
    include_cols.append(DetentionsColumns.CASE_STATUS.column_name)
    include_cols.append(DetentionsColumns.CASE_CATEGORY.column_name)
    include_cols.append(DetentionsColumns.CASE_THREAT_LEVEL.column_name)
    include_cols.append(DetentionsColumns.BOOK_IN_CRIMINALITY.column_name)

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
    include_cols.append(DetentionsColumns.FINAL_CHARGE.column_name)

    c = DetentionsColumns.FINAL_PROGRAM.column_name
    d[c] = d[c].replace('Inspections - Land', 'Inspections')
    d[c] = d[c].replace('Inspections - Air', 'Inspections')
    d[c] = d[c].replace('Inspections - Sea', 'Inspections')
    
    d[c] = d[c].replace('287G Program', '287g Task Force')
    
    d[c] = d[c].replace('Mobile Criminal Alien Team', 'Fugitive Operations')
    d[c] = d[c].replace('Violent Criminal Alien Section', 'ERO Criminal Prosecutions')
    include_cols.append(DetentionsColumns.FINAL_PROGRAM.column_name)

    d = update_msc_charge(d, DetentionsColumns.MSC_CHARGE.column_name)
    include_cols.append(DetentionsColumns.MSC_CHARGE.column_name)
    
    include_cols.append('Unique Identifier')
    d[include_cols].to_parquet(output_file)
    print(output_file)


def detainers_clean(output_file):
    if output_file.exists():
        print(output_file, 'already exists')
        return
    print('detainers_clean()')
    
    detainers_df = pd.read_parquet(input_dir / 'detainers.parquet')
    
    _US_STATE_ABBR = {
        'ALABAMA':'AL','ALASKA':'AK','ARIZONA':'AZ','ARKANSAS':'AR','CALIFORNIA':'CA','COLORADO':'CO',
        'CONNECTICUT':'CT','DELAWARE':'DE','FLORIDA':'FL','GEORGIA':'GA','HAWAII':'HI','IDAHO':'ID',
        'ILLINOIS':'IL','INDIANA':'IN','IOWA':'IA','KANSAS':'KS','KENTUCKY':'KY','LOUISIANA':'LA',
        'MAINE':'ME','MARYLAND':'MD','MASSACHUSETTS':'MA','MICHIGAN':'MI','MINNESOTA':'MN','MISSISSIPPI':'MS',
        'MISSOURI':'MO','MONTANA':'MT','NEBRASKA':'NE','NEVADA':'NV','NEW HAMPSHIRE':'NH','NEW JERSEY':'NJ',
        'NEW MEXICO':'NM','NEW YORK':'NY','NORTH CAROLINA':'NC','NORTH DAKOTA':'ND','OHIO':'OH','OKLAHOMA':'OK',
        'OREGON':'OR','PENNSYLVANIA':'PA','RHODE ISLAND':'RI','SOUTH CAROLINA':'SC','SOUTH DAKOTA':'SD',
        'TENNESSEE':'TN','TEXAS':'TX','UTAH':'UT','VERMONT':'VT','VIRGINIA':'VA','WASHINGTON':'WA',
        'WEST VIRGINIA':'WV','WISCONSIN':'WI','WYOMING':'WY','DISTRICT OF COLUMBIA':'DC'
    }
    _US_TERRITORY_ABBR = {
        'PUERTO RICO':'PR','GUAM':'GU','VIRGIN ISLANDS':'VI','NORTHERN MARIANA ISLANDS':'MP','AMERICAN SAMOA':'AS'
    }
    _US_ALL_ABBR = {**_US_STATE_ABBR, **_US_TERRITORY_ABBR}
    
    _STATE_TO_CENSUS_REGION = {
        'CT':'Northeast','ME':'Northeast','MA':'Northeast','NH':'Northeast','RI':'Northeast','VT':'Northeast',
        'NJ':'Northeast','NY':'Northeast','PA':'Northeast',
        'IL':'Midwest','IN':'Midwest','MI':'Midwest','OH':'Midwest','WI':'Midwest',
        'IA':'Midwest','KS':'Midwest','MN':'Midwest','MO':'Midwest','NE':'Midwest','ND':'Midwest','SD':'Midwest',
        'DE':'South','FL':'South','GA':'South','MD':'South','NC':'South','SC':'South','VA':'South','DC':'South',
        'WV':'South','AL':'South','KY':'South','MS':'South','TN':'South','AR':'South','LA':'South','OK':'South','TX':'South',
        'AZ':'West','CO':'West','ID':'West','MT':'West','NV':'West','NM':'West','UT':'West','WY':'West',
        'AK':'West','CA':'West','HI':'West','OR':'West','WA':'West',
        'PR':'Territory','GU':'Territory','VI':'Territory','MP':'Territory','AS':'Territory'
    }
    
    status_map = {
        "Detainer": "Detained",
        "Prosecutorial Discretion": "Detained", 
        "Bag and Baggage": "Detained", 
        "TURNED OVER TO": "Detained", 
        "HSI Criminal Arrest": "Detained",
        "Warrant of Arrest/Notice to Appear": "Pending",
        "Notice to Appear Released (I-862)": "Pending",
        "Notice to Appear Detained (I-862)": "Pending",
        "Notice to Appear (I-862)": "Pending",
        "I-210": "Pending", 
        "Expedited Removal (I-860)": "Pending",
        "Expedited Removal (I-860) - Full Scope": "Pending",
        "Expedited Removal with Credible Fear": "Pending",
        "Expedited Removal with Credible Fear - Full Scope": "Pending",
        "Expedited Removal - Per 212(F)": "Pending",
        "REINSTATEMENT OF DEPORT ORDER I-871": "Deported",
        "Reinstatement of Deportation Reasonable Fear": "Deported",
        "Voluntary Return": "Deported",
        "Voluntary Departure": "Deported",
        "Withdrawal (I-275)": "Deported",
        "Withdrawal in Lieu of NTA": "Deported",
        "Withdrawal in Lieu of ER": "Deported",
        "VWP Removal": "Deported",  
        "Crew Member (I-99) Removal": "Deported", 
        "Paroled": "Deported",
        "Not Amenable to Removal": "Deported",  
        "Not in Custody": "Released",
        "Foreign Born USC": "Released",  
        "Deported": "Deported",
        "ADMINISTRATIVE DEPORTATION I-851/I-851A": "Deported",
        "Other": "Unknown",
        None: "Unknown",
        "Admitted": "Unknown",
    }
    drop_cols = ['Felon', 'Case Category','Time of Apprehension Current Program', 'Detainer Type']
    
    detainers_df_clean = detainers_df.copy(deep  = True)
    detainers_df_clean.drop(columns=drop_cols, inplace=True)
    detainers_df_clean.drop_duplicates(inplace=True)
    date_cols = [col for col in detainers_df.columns if 'date' in col.lower()]
    year_cols = ['MSC Sentence Days', 'MSC Sentence Months', 'MSC Sentence Years', 'Birth Year']
    yes_no_cols = [col for col in detainers_df.columns if 'yes' in col.lower()]
    
    for col in date_cols:
        detainers_df_clean[col] = pd.to_datetime(detainers_df_clean[col], errors='coerce')
    for col in year_cols:
        detainers_df_clean[col] = pd.to_numeric(detainers_df_clean[col], errors='coerce')
        
    max_date = pd.Timestamp('2025-07-31')
    for col in date_cols:
        detainers_df_clean.loc[detainers_df_clean[col] > max_date, col] = pd.NaT
    
    detainers_df_clean['Age'] = 2025 - detainers_df_clean['Birth Year']
    
    for col in yes_no_cols:
        detainers_df_clean[col] = detainers_df_clean[col].map({"YES":1,"NO":0})
    
    # detainers_df_clean['Case Status'].map({'ACTIVE':"Pending", '8-Excluded/Removed - Inadmissibility':"Deported",
    #        '6-Deported/Removed - Deportability':"Deported",
    #        '3-Voluntary Departure Confirmed':"Deported", '9-VR Witnessed':"Pending",
    #        'E-Charging Document Canceled by ICE':"Remained", 'A-Proceedings Terminated':'Remained',
    #        'B-Relief Granted':"Remained", '0-Withdrawal Permitted - I-275 Issued':"Deported",
    #        '7-Died':"Other", 'L-Legalization - Permanent Residence Granted':"Remained",
    #        '5-Title 50 Expulsion':"Deported", 'Z-SAW - Permanent Residence Granted':'Remained'})
    detainers_df_clean = update_case_status(detainers_df_clean, 'Case Status')

    # detainers_df_clean['Detainer Prepared Criminality'].map({'1 Convicted Criminal':"Criminal", '2 Pending Criminal Charges':"Pending Criminal",
    #        '3 Other Immigration Violator':"Other"})
    detainers_df_clean = update_criminality(detainers_df_clean, 'Detainer Prepared Criminality')

    # detainers_df_clean['Most Serious Conviction (MSC) Charge'] = detainers_df_clean['Most Serious Conviction (MSC) Charge'].map(_categorize_msc)
    detainers_df_clean = update_msc_charge(detainers_df_clean, 'Most Serious Conviction (MSC) Charge')
    
    detainers_df_clean['Facility State'] = detainers_df_clean['Facility State'].map(_US_ALL_ABBR)
    
    detainers_df_clean['Census Region'] = detainers_df_clean['Facility State'].map(_STATE_TO_CENSUS_REGION)
    
    detainers_df_clean['Detainer Prepared Criminality'] = detainers_df_clean['Detainer Prepared Criminality'].map({'1 Convicted Criminal':"Criminal", '2 Pending Criminal Charges':'Pending Criminal',
           '3 Other Immigration Violator':"Non-Criminal"})
    
    detainers_df_clean['Case Status'] = detainers_df_clean['Case Status'].map({'ACTIVE':"Pending", '8-Excluded/Removed - Inadmissibility':"Deported",
           '6-Deported/Removed - Deportability': "Deported",
           '3-Voluntary Departure Confirmed':"Deported", '9-VR Witnessed':"Pending",
           'E-Charging Document Canceled by ICE':"Remained", 'A-Proceedings Terminated':"Remained",
           'B-Relief Granted':"Remained", '0-Withdrawal Permitted - I-275 Issued':"Pending",
           '7-Died':"Other", 'L-Legalization - Permanent Residence Granted':"Remained",
           '5-Title 50 Expulsion':"Deported", 'Z-SAW - Permanent Residence Granted':"Remained", None: "Unknown"})
    
    detainers_df_clean['Detainer Prep Threat Level'] = detainers_df_clean['Detainer Prep Threat Level'].map({None: 0, 1.0: 1, 2.0:2, 3.0:3})
    
    detainers_df_clean['Processing Disposition'] = detainers_df_clean['Processing Disposition'].map(status_map)
    
    detainers_df_clean['Total Sentence Days'] = detainers_df_clean['MSC Sentence Years'] * 365 + detainers_df_clean['MSC Sentence Months'] * 30 + detainers_df_clean['MSC Sentence Days']
    
    #Remove columns with more than 75% missing
    missing_fraction = detainers_df_clean.isnull().mean()
    cols_to_drop = missing_fraction[missing_fraction > 0.75].index
    detainers_df_clean.drop(columns=cols_to_drop, inplace=True)
    
    critical_field = ['Unique Identifier']
    detainers_df_clean.dropna(subset=critical_field, inplace=True)
    detainers_df_clean.drop_duplicates(inplace=True)
    # output_parquet = 'detainers_cleaned.parquet'
    detainers_df_clean.to_parquet(output_file, index=False)
    print(output_file)


if __name__ == '__main__':
    encounters_clean(output_dir / 'encounters.parquet')
    arrests_clean(output_dir / 'arrests.parquet')
    detentions_clean(output_dir / 'detentions.parquet')
    detainers_clean(output_dir / 'detainers.parquet')
    print('Done')
