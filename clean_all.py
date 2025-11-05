import pandas as pd
import clean_encounters
import clean_removals
import clean_detainers
import os

"""
TODO
- remove duplicates in encounters, detentions, detainers, administrative arrests
"""

ARRESTS_FILENAME = 'arrests.parquet'
DETAINERS_FILENAME = 'detainers.parquet'
DETENTIONS_FILENAME = 'detentions.parquet'
ENCOUNTERS_FILENAME = 'encounters.parquet'
REMOVALS_FILENAME = 'removals.parquet'

INPUT_DIR = 'ice_data/proc_data/'
OUTPUT_DIR = 'ice_data/clean_data/'

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Cleaning Arrests data")

    print("Cleaning Detainers Data")
    detainers_df = pd.read_parquet(INPUT_DIR + DETAINERS_FILENAME)
    clean_detainers.clean_detainers(detainers_df)
    detainers_df.to_parquet(OUTPUT_DIR + DETAINERS_FILENAME, index=False)

    print("Cleaning Detentions Data")
    
    print("Cleaning Encounters Data")
    #encounters_df = pd.read_parquet(INPUT_DIR + ENCOUNTERS_FILENAME)
    #clean_encounters.clean_encounters(encounters_df)
    #encounters_df.to_parquet(OUTPUT_DIR + ENCOUNTERS_FILENAME, index=False)

    print("Cleaning Removals Data")
    #removals_df = pd.read_parquet(INPUT_DIR + REMOVALS_FILENAME)
    #clean_removals.clean_removals(removals_df)
    #removals_df.to_parquet(OUTPUT_DIR + REMOVALS_FILENAME, index=False)