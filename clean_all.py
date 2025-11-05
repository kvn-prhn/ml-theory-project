import pandas as pd
import clean_encounters

if __name__ == "__main__":
    encounters_df = pd.read_parquet('ice_data/proc_data/encounters.parquet')
    clean_encounters.cleanEncounters(encounters_df)