import pandas as pd
import numpy as np
import os
# os.chdir("/home/wes/projects/ml_proj_new/ml-theory-project/")
import re

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

def clean_detainers(detainers_df_clean):
    # laird: making this happen in place so it is faster and to match pattern of other cleaning scrips.
    # detainers_df_clean = detainers_df.copy(deep  = True)
    detainers_df_clean.drop(columns=drop_cols, inplace=True)
    detainers_df_clean.drop_duplicates(inplace=True)
    date_cols = [col for col in detainers_df_clean.columns if 'date' in col.lower()]
    year_cols = ['MSC Sentence Days', 'MSC Sentence Months', 'MSC Sentence Years', 'Birth Year']
    yes_no_cols = [col for col in detainers_df_clean.columns if 'yes' in col.lower()]

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
        
    detainers_df_clean['Case Status'].map({'ACTIVE':"Pending", '8-Excluded/Removed - Inadmissibility':"Deported",
        '6-Deported/Removed - Deportability':"Deported",
        '3-Voluntary Departure Confirmed':"Deported", '9-VR Witnessed':"Pending",
        'E-Charging Document Canceled by ICE':"Remained", 'A-Proceedings Terminated':'Remained',
        'B-Relief Granted':"Remained", '0-Withdrawal Permitted - I-275 Issued':"Deported",
        '7-Died':"Other", 'L-Legalization - Permanent Residence Granted':"Remained",
        '5-Title 50 Expulsion':"Deported", 'Z-SAW - Permanent Residence Granted':'Remained'})

    detainers_df_clean['Detainer Prepared Criminality'].map({'1 Convicted Criminal':"Criminal", '2 Pending Criminal Charges':"Pending Criminal",
        '3 Other Immigration Violator':"Other"})

    detainers_df_clean['Most Serious Conviction (MSC) Charge'] = detainers_df_clean['Most Serious Conviction (MSC) Charge'].map(_categorize_msc)

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

    # laird: changed this to not remove a few columns, namely entry date
    # I've just copied all the rows with >75% missing data here
    detainers_df_clean.drop('Federal Interest Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Visa Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Unlawful Entry Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Unlawful Attempt Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Order to Show Cause Served Date', axis=1, inplace=True)
    detainers_df_clean.drop('Other Removal Reason', axis=1, inplace=True)
    detainers_df_clean.drop('Immigration Fraud Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Other Removal Reason Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Illegal Entry Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Illegal Reentry Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Significant Risk Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Criminal Street Gang Yes No', axis=1, inplace=True)
    # detainers_df_clean.drop('Entry Date', axis=1, inplace=True)
    detainers_df_clean.drop('Multiple Prior MISD Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Time of Apprehension Case Category', axis=1, inplace=True)
    detainers_df_clean.drop('Aggravated Felony Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Prior Felony Yes No', axis=1, inplace=True)
    detainers_df_clean.drop('Violent Misdemeanor Yes No', axis=1, inplace=True)

    detainers_df_clean['Apprehension Month'] = pd.Categorical(detainers_df_clean['Apprehension Date'].dt.month_name(), categories=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'], ordered=True)

    # critical_field = ['Unique Identifier']
    # detainers_df_clean.dropna(subset=critical_field, inplace=True)
    # detainers_df_clean.drop_duplicates(inplace=True)

    # it = iter(detainers_df_clean.columns)
    # col = next(it)
    # print(col)
    # print()
    # print(detainers_df_clean[col].unique())
    # print()
    # print(detainers_df_clean[col].value_counts())


def combine_duplicate_ids(df):
    initial_rows = df.shape[0]
    arrest_counts = df['Unique Identifier'].value_counts()
    df['Num Detainers'] = df['Unique Identifier'].map(arrest_counts)
    df.sort_values('Detainer Prepare Date', ascending=False, inplace=True)
    df.drop_duplicates(subset='Unique Identifier', keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)
    rows_removed = initial_rows - df.shape[0]
    print("Removed %d duplicate rows, keeping only most recent detainer per individual" % rows_removed)
    print("Dataframe now has %d rows" % df.shape[0])
