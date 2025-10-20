# pip install pandas 
import pathlib
import pandas as pd

from arrests_columns import ArrestsColumns
from detainers_columns import DetainersColumns
from detentions_columns import DetentionsColumns
from encounters_columns import EncountersColumns
from removals_columns import RemovalsColumns

# UPDATE THIS PATH TO WHERE THE ICE EXCEL FILES ARE
data_dir = pathlib.Path('..\\..\\..\\Datasets\\ice_release_11aug2025')
assert data_dir.exists()


arrests_file = next(data_dir.glob('*Arrests*.xlsx'))
detainers_file = next(data_dir.glob('*Detainers*.xlsx'))
encounters_file = next(data_dir.glob('*Encounters*.xlsx'))
detentions_file = next(data_dir.glob('*Detentions*.xlsx'))
removals_file = next(data_dir.glob('*Removals*.xlsx'))
print(f'{arrests_file=}\n{detainers_file=}\n{encounters_file=}\n{detentions_file=}\n{removals_file=}')

my_temp_dir = pathlib.Path('proc_data')
if not my_temp_dir.exists():
    my_temp_dir.mkdir()


def load_arrests_data():
    temp1 = my_temp_dir / 'arrests.parquet'
    if temp1.exists():
        return temp1
        
    arrests_cols = [v.value for k, v in ArrestsColumns.__members__.items()]
    arrests_d = pd.read_excel(arrests_file, sheet_name='Arrests', skiprows=6, usecols = arrests_cols,  # nrows=10, 
                              engine='openpyxl', engine_kwargs={'read_only': True}) 

    arrests_d2 = arrests_d[~arrests_d[ArrestsColumns.UNIQUE_IDENTIFIER].isna()]
    arrests_d2.drop_duplicates().reset_index(drop=True).to_parquet(temp1)

    return temp1


def load_detainers_data():
    temp2 = my_temp_dir / 'detainers.parquet'
    if temp2.exists():
        return temp2

    detainers_cols = [v.value for k, v in DetainersColumns.__members__.items()]
    # print(detainers_cols)
    detainers_d = pd.read_excel(detainers_file, sheet_name='Detainers', skiprows=6, usecols = detainers_cols,
                                engine='openpyxl', engine_kwargs={'read_only': True}) 
    
    detainers_d2 = detainers_d[~detainers_d[DetainersColumns.UNIQUE_IDENTIFIER].isna()].copy()
    detainers_d2[DetainersColumns.MSC_CHARGE_DATE] = pd.to_datetime(detainers_d2[DetainersColumns.MSC_CHARGE_DATE])
    detainers_d2[DetainersColumns.MSC_CONVICTION_DATE] = pd.to_datetime(detainers_d2[DetainersColumns.MSC_CONVICTION_DATE])
    detainers_d2.drop_duplicates().reset_index(drop=True).to_parquet(temp2)
    
    return temp2


def load_detentions_data():
    temp3 = my_temp_dir / 'detentions.parquet'
    if temp3.exists():
        return temp3
        
    detention_cols = [v.value for k, v in DetentionsColumns.__members__.items()]
    detentions_d = pd.concat([pd.read_excel(detentions_file, sheet_name='Stays <10012024', skiprows=6, usecols = detention_cols,
                                            engine='openpyxl', engine_kwargs={'read_only': True}),
                              pd.read_excel(detentions_file, sheet_name='Stays >=10012024', skiprows=6, usecols = detention_cols,
                                            engine='openpyxl', engine_kwargs={'read_only': True})],
                             ignore_index=True)

    detentions_d2 = detentions_d[~detentions_d[DetentionsColumns.UNIQUE_IDENTIFIER].isna()]
    detentions_d2.drop_duplicates().reset_index(drop=True).to_parquet(temp3)

    return temp3


def load_encounters_data():
    temp4 = my_temp_dir / 'encounters.parquet'
    if temp4.exists():
        return temp4
        
    encounters_cols = [v.value for k, v in EncountersColumns.__members__.items()]
    encounters_d = pd.concat([pd.read_excel(encounters_file, sheet_name='Encounters <10012024', skiprows=6, usecols = encounters_cols,
                                            engine='openpyxl', engine_kwargs={'read_only': True}),
                              pd.read_excel(encounters_file, sheet_name='Encounters >=10012024', skiprows=6, usecols = encounters_cols,
                                            engine='openpyxl', engine_kwargs={'read_only': True})],
                             ignore_index=True)
    
    encounters_d2 = encounters_d[~encounters_d[EncountersColumns.UNIQUE_IDENTIFIER].isna()]
    encounters_d2.drop_duplicates().reset_index(drop=True).to_parquet(temp4)

    return temp4


def load_removals_data():
    temp5 = my_temp_dir / 'removals.parquet'
    if temp5.exists():
        return temp5

    removals_cols = [v.value for k, v in RemovalsColumns.__members__.items()]
    removals_d = pd.read_excel(removals_file, sheet_name='Removals', skiprows=6, usecols = removals_cols,
                               engine='openpyxl', engine_kwargs={'read_only': True})
    
    removals_d2 = removals_d[~removals_d[RemovalsColumns.UNIQUE_IDENTIFIER].isna()].copy()
    removals_d2[RemovalsColumns.ENTRY_DATE] = pd.to_datetime(removals_d2[RemovalsColumns.ENTRY_DATE], errors='coerce')
    removals_d2[RemovalsColumns.MSC_CHARGE_DATE] = pd.to_datetime(removals_d2[RemovalsColumns.MSC_CHARGE_DATE], errors='coerce')
    removals_d2[RemovalsColumns.MSC_CONVICTION_DATE] = pd.to_datetime(removals_d2[RemovalsColumns.MSC_CONVICTION_DATE], errors='coerce')
    
    removals_d2.drop_duplicates().reset_index(drop=True).to_parquet(temp5)

    return temp5


arrests_rfile = load_arrests_data()
print(arrests_rfile)
detainers_rfile = load_detainers_data()
print(detainers_rfile)
detentions_rfile = load_detentions_data()
print(detentions_rfile)
encounters_rfile = load_encounters_data()
print(encounters_rfile)
removals_rfile = load_removals_data()
print(removals_rfile)

    