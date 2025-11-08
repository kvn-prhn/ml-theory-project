import pandas as pd
import clean_utils

def clean_departed_date(df):
    """
    no-op: all dates within 2023-09-01 and 2025-07-28, and already datetime type
    """
    # departed_date = df['Departed Date']
    # clean_utils.summarize_ordinal_column(departed_date)
    # print(departed_date.min())
    # print(departed_date.max())

def clean_port_of_departure(df):
    """
    0.7% missing values, but "UNKNOWN, POE" category
    no-op: all values look good
    """
    port_of_departure = df['Port of Departure']
    # clean_utils.summarize_column(port_of_departure)
    # print(port_of_departure.value_counts())
    # print("%f%% missing values" % (100 * (port_of_departure == 'UNKNOWN, POE').sum() / df.shape[0]))

def clean_departure_country(df):
    departure_country = df['Departure Country']
    clean_utils.clean_countries(departure_country)

def clean_docket_aor(df):
    """
    no-op: no missing values, no repeated columns
    """
    # docket_aor = df['Docket AOR']
    # clean_utils.summarize_column(docket_aor)
    # print(docket_aor.value_counts())

def clean_apprehension_state(df):
    """
    83% missing values. Won't be useful. Use aor instead.
    """
    # apprehension_state = df['Apprehension State']
    # clean_utils.summarize_categorical_column(apprehension_state)
    df.drop(columns='Apprehension State', axis=1, inplace=True)
    print("dropped 'Apprehension State, %s columns remaining" % df.shape[1])

def clean_apprehension_county(df):
    """
    ~100% missing values, dropping
    """
    # apprehension_county = df['Apprehension County']
    # clean_utils.summarize_categorical_column(apprehension_county)
    df.drop(columns='Apprehension County', axis=1, inplace=True)
    print("dropped 'Apprehension County, %s columns remaining" % df.shape[1])

def clean_case_status(df):
    """
    no-op. no missing data or repeat categories
    """
    # case_status = df['Case Status']
    # clean_utils.summarize_categorical_column(case_status)

def clean_gender(df):
    """
    drop 130 missing values
    """
    gender = df['Gender']
    # clean_utils.summarize_categorical_column(gender)
    unknown_rows = (gender == "Unknown")
    print("dropping %d rows where gender is 'Unknown'" % unknown_rows.sum())
    df.drop(df[unknown_rows].index, inplace=True)
    print("dataframe now has %d rows" % df.shape[0])
    df['Male'] = gender == 'Male'
    print("Created 'Male' column with %d male values" % df['Male'].sum())
    df.drop(columns='Gender', axis=1, inplace=True)
    print("Dropped 'Gender' column, %d columns remain" % df.shape[1])

def clean_birth_country(df):
    birth_country = df['Birth Country']
    clean_utils.clean_countries(birth_country)

def clean_citizenship_country(df):
    citizenship_country = df['Citizenship Country']
    clean_utils.clean_countries(citizenship_country)

def clean_birth_year(df):
    birth_year = df['Birth Year']
    # clean_utils.summarize_ordinal_column(birth_year)
    print("dropping %d rows with missing birth year" % birth_year.isnull().sum())
    df.dropna(subset=['Birth Year'], inplace=True)
    print("dataframe now has %d rows" % df.shape[0])
    df['Birth Year'] = df['Birth Year'].astype('int16')

def clean_entry_date(df):
    entry_date = df['Entry Date']
    # clean_utils.summarize_ordinal_column(entry_date)
    entry_year = entry_date.dt.year
    birth_year = df['Birth Year']
    invalid_rows = entry_year < birth_year
    print("dropping %d rows where entry date is before birth year" % invalid_rows.sum())
    df.drop(df[invalid_rows].index, inplace=True)
    print("dataframe now has %d rows" % df.shape[0])

def clean_entry_status(df):
    """
    The cookbook says they "don't know how this is used". There are some
    interesting fields like "student" and "visitor" but they have <100 entries
    dropping.
    """
    # entry_status = df['Entry Status']
    # clean_utils.summarize_categorical_column(entry_status)
    df.drop(columns='Entry Status', axis=1, inplace=True)
    print("dropped 'Entry Status' column %d columns remain" % df.shape[1])

def clean_msc_ncic_charge(df):
    """
    70% missing, but presumably, if its missing they is no criminal charge
    """
    # msc_ncic_charge = df['MSC NCIC Charge']
    # clean_utils.summarize_categorical_column(msc_ncic_charge)

def clean_msc_charge_date(df):
    """
    also missing 70%, but assuming that is the same as msc ncic charge
    dates look reasonable. already datetime type
    """
    # msc_charge_date = df['MSC Charge Date']
    # clean_utils.summarize_ordinal_column(msc_charge_date)

def clean_msc_criminal_charge_status(df):
    """
    only a single instance of "pending", drop it and replace with boolean
    'Convicted' column
    """
    msc_criminal_charge_status = df['MSC Criminal Charge Status']
    # clean_utils.summarize_categorical_column(msc_criminal_charge_status)
    df['Convicted'] = msc_criminal_charge_status == 'CONVICTED'
    print("Created 'Convicted' column with %d True values" % df['Convicted'].sum())
    df.drop(columns='MSC Criminal Charge Status', axis=1, inplace=True)
    print("Dropped 'MSC Criminal Charge Status' column, %d columns remain" % df.shape[1])

def clean_msc_conviction_date(df):
    """
    missing 70% values, but i thin that just means no criminal conviction
    """
    # msc_conviction_date = df['MSC Conviction Date']
    # clean_utils.summarize_ordinal_column(msc_conviction_date)

def clean_case_threat_level(df):
    """
    same 70% missing as other case stuff
    """
    # case_threat_level = df['Case Threat Level']
    # clean_utils.summarize_categorical_column(case_threat_level)

def clean_case_criminality(df):
    """
    no-op. not sure how this is related to my new 'Convicted' column ... 
    """
    # case_criminality = df['Case Criminality']
    # clean_utils.summarize_categorical_column(case_criminality)

def clean_felon(df):
    felon = df['Felon']
    # clean_utils.summarize_categorical_column(felon)
    df['Is Felon'] = (felon == 'Other') | (felon == 'Drugs') | (felon == 'Both (drug and other agg felon convictions)')
    print("Created 'Is Felon' column with %d true values" % df['Is Felon'].sum())
    df.drop(columns='Felon', axis=1, inplace=True)
    print("Dropped 'Felon' column, %d columns remain" % df.shape[1])

def clean_processing_disposition(df):
    """
    there is a long tail of random things, we may want to combine some of them into a larger "other" group
    not sure we will use this field though ... the cookbook doesn't know how to interpret it.
    """
    # processing_disposition = df['Processing Disposition']
    # clean_utils.summarize_categorical_column(processing_disposition)
    # print("dropping %d rows with missing processing disposition" % processing_disposition.isnull().sum())
    # df.dropna(subset=['Processing Disposition'], inplace=True)
    # print("dataframe now has %d rows" % df.shape[0])
    df.drop(columns='Processing Disposition', axis=1, inplace=True)
    print("Dropped 'Processing Disposition' column, %d columns remain" % df.shape[1])

def clean_case_category(df):
    """
    no-op: looks good
    """
    # case_category = df['Case Category']
    # clean_utils.summarize_categorical_column(case_category)

def clean_final_program(df):
    """
    no-op, looks good
    """
    # final_program = df['Final Program']
    # clean_utils.summarize_categorical_column(final_program)

def clean_latest_arrest_program_current(df):
    """
    many missing values, cookbook says to use final program instead
    """
    # latest_arrest_program_current = df['Latest Arrest Program Current']
    # clean_utils.summarize_categorical_column(latest_arrest_program_current)
    df.drop(columns='Latest Arrest Program Current', axis=1, inplace=True)
    print("Dropped 'Latest Arrest Program Current' column, %d columns remain" % df.shape[1])

def clean_latest_person_apprehension_date(df):
    # latest_person_apprehension_date = df['Latest Person Apprehension Date']
    # clean_utils.summarize_ordinal_column(latest_person_apprehension_date)
    df.dropna(subset=['Latest Person Apprehension Date'], inplace=True)
    print("dropped rows with null values for 'Latest Person Apprehension Date' dataframe now has %d rows" % df.shape[0])

def clean_final_order_yes_no(df):
    """
    noop: looks good
    """
    # final_order_yes_no = df['Final Order Yes No']
    # clean_utils.summarize_categorical_column(final_order_yes_no)

def clean_final_order_date(df):
    final_order_date = df['Final Order Date']
    # clean_utils.summarize_ordinal_column(final_order_date)
    order_year = final_order_date.dt.year
    birth_year = df['Birth Year']
    invalid_rows = order_year < birth_year
    print("dropping %d rows where order date is before birth" % invalid_rows.sum())
    df.drop(df[invalid_rows].index, inplace=True)
    print("dataframe now has %d rows" % df.shape[0])

def clean_prior_deport_yes_no(df):
    """
    no-op: looks good
    """
    # prior_deport_yes_no = df['Prior Deport Yes No']
    # clean_utils.summarize_categorical_column(prior_deport_yes_no)

def clean_latest_person_departed_date(df):
    """
    no-op: looks good
    """
    # latest_person_departed_date = df['Latest Person Departed Date']
    # clean_utils.summarize_ordinal_column(latest_person_departed_date)

def combine_duplicate_ids(df):
    """
    Keep only the latest entry for each unique identifier. If an individual
    appears multiple times, it means they were deported multiple times, so
    keep only their most recent deportation. Add a column tracking the number
    of removals for each individual.
    """
    initial_rows = df.shape[0]
    unique_identifier = df['Unique Identifier']
    duplicates = unique_identifier.duplicated(keep='first').sum()
    print("Found %d rows with duplicate unique identifiers" % duplicates)

    # Count the number of removals for each unique identifier
    removal_counts = unique_identifier.value_counts()
    df['Num Removals'] = df['Unique Identifier'].map(removal_counts)
    print("Created 'Num Removals' column with %d total removals tracked" % df['Num Removals'].sum())

    # Sort by Departed Date in descending order (most recent first)
    # Then drop duplicates, keeping the first (most recent) occurrence
    df.sort_values('Departed Date', ascending=False, inplace=True)
    df.drop_duplicates(subset='Unique Identifier', keep='first', inplace=True)
    df.reset_index(drop=True, inplace=True)

    rows_removed = initial_rows - df.shape[0]
    print("Removed %d duplicate rows, keeping only most recent deportation per individual" % rows_removed)
    print("Dataframe now has %d rows" % df.shape[0])

def clean_removals(df):
    print("Initial dataframe shape: %d rows, %d columns" % (df.shape[0], df.shape[1]))
    clean_departed_date(df)
    clean_port_of_departure(df)
    clean_departure_country(df)
    clean_docket_aor(df)
    clean_apprehension_state(df)
    clean_apprehension_county(df)
    clean_case_status(df)
    clean_gender(df)
    clean_birth_country(df)
    clean_citizenship_country(df)
    clean_birth_year(df)
    clean_entry_date(df)
    clean_entry_status(df)
    clean_msc_ncic_charge(df)
    clean_msc_charge_date(df)
    clean_msc_criminal_charge_status(df)
    clean_msc_conviction_date(df)
    clean_case_threat_level(df)
    clean_case_criminality(df)
    clean_felon(df)
    clean_processing_disposition(df)
    clean_case_category(df)
    clean_final_program(df)
    clean_latest_arrest_program_current(df)
    clean_latest_person_apprehension_date(df)
    clean_final_order_yes_no(df)
    clean_final_order_date(df)
    clean_prior_deport_yes_no(df)
    clean_latest_person_departed_date(df)

    print("Final dataframe shape: %d rows, %d columns" % (df.shape[0], df.shape[1]))
