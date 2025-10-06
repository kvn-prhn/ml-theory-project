import pandas as pd

# arrests = pd.read_excel('./ice-data/ARRESTS 2025-ICLI-00019_2024-ICFO-39357_ERO Admin Arrests_LESA-STU_FINAL Redacted_raw.xlsx')
# detainers = pd.read_excel('./ice-data/DETAINERS 2025-ICLI-00019_2024-ICFO-39357_ERO Detainers_LESA-STU_FINAL Redacted_raw.xlsx')
# detentions = pd.read_excel('./ice-data/DETENTIONS 2025-ICLI-00019_2024-ICFO-39357_ICE Detentions_LESA-STU_FINAL Redacted_raw.xlsx', skiprows=6)
# encounters = pd.read_excel('./ice-data/ENCOUNTERS 2025-ICLI-00019_2024-ICFO-39357_ERO Encounters_LESA-STU_FINAL Redacted_raw.xlsx', skiprows=6)
removals = pd.read_excel('./ice-data/REMOVALS 2025-ICLI-00019_2024-ICFO-39357_ICE Removals_LESA-STU_FINAL Redacted_raw.xlsx', skiprows=6)

def print_summary_statistics(df):
    print(50 * "-")
    total_cells = df.shape[0] * df.shape[1]
    total_missing = df.isnull().sum().sum()
    percent_missing = (total_missing / total_cells) * 100
    print(f"Total missing data: {percent_missing:.2f}%")

    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

    print ("Column Name, Unique Values, % Missing")
    for column in df.columns:
        missing_count = df[column].isnull().sum()
        missing_percentage = (missing_count / len(df)) * 100
        unique_count = df[column].nunique(dropna=True)
        print(f"{column}: {unique_count}, {missing_percentage:.2f}%")


print_summary_statistics(removals)