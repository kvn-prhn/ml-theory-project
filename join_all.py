"""
Takes the output of clean_all.py, merges duplicate unique ids and merges all
datasets on unique id.
"""

import pandas as pd
import clean_encounters
import clean_removals
import clean_detainers
import clean_arrests
import clean_detentions
import os

ARRESTS_FILENAME = 'arrests.parquet'
DETAINERS_FILENAME = 'detainers.parquet'
DETENTIONS_FILENAME = 'detentions.parquet'
ENCOUNTERS_FILENAME = 'encounters.parquet'
REMOVALS_FILENAME = 'removals.parquet'

INPUT_DIR = 'ice_data/clean_data/'
OUTPUT_DIR = 'ice_data/joined_data/'

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    arrests_df = pd.read_parquet(INPUT_DIR + ARRESTS_FILENAME)
    detainers_df = pd.read_parquet(INPUT_DIR + DETAINERS_FILENAME)
    detentions_df = pd.read_parquet(INPUT_DIR + DETENTIONS_FILENAME)
    encounters_df = pd.read_parquet(INPUT_DIR + ENCOUNTERS_FILENAME)
    removals_df = pd.read_parquet(INPUT_DIR + REMOVALS_FILENAME)

    clean_removals.combine_duplicate_ids(removals_df)
    clean_arrests.combine_duplicate_ids(arrests_df)
    clean_detainers.combine_duplicate_ids(detainers_df)
    clean_detentions.combine_duplicate_ids(detentions_df)
    clean_encounters.combine_duplicate_ids(encounters_df)
