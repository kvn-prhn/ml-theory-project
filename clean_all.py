import pandas as pd
import clean_encounters
import clean_removals
import clean_detainers
import clean_arrests
import clean_detentions
import os
import sys
from tables import Tables

INPUT_DIR = 'ice_data/proc_data/'
OUTPUT_DIR = 'ice_data/clean_data/'

clean_func_map = {
    'arrests': clean_arrests.clean_arrests,
    'detainers': clean_detainers.clean_detainers,
    'detentions': clean_detentions.clean_detentions,
    'encounters': clean_encounters.clean_encounters,
    'removals': clean_removals.clean_removals,
}

if __name__ == "__main__":
    assert len(sys.argv) <= 2, "too many arguments"
    tables_to_clean = clean_func_map.keys() if len(sys.argv) == 1 else [sys.argv[1]]

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for table_name in tables_to_clean:
        print(f"Cleaning %s table" % table_name)
        df = pd.read_parquet(INPUT_DIR + table_name + '.parquet')
        clean_func_map[table_name](df)
        df.to_parquet(OUTPUT_DIR + table_name + '.parquet', index=False)