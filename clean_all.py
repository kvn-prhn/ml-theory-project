import pandas as pd
import clean_encounters
import clean_removals

"""
TODO
- remove duplicates in encounters, detentions, detainers, administrative arrests
"""

if __name__ == "__main__":
    encounters_df = pd.read_parquet('ice_data/proc_data/encounters.parquet')
    clean_encounters.clean_encounters(encounters_df)

    print("Loading removals data...")
    removals_df = pd.read_parquet('ice_data/proc_data/removals.parquet')
    clean_removals.clean_removals(removals_df)