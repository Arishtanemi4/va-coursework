import os
import re
import sys
import pandas as pd

import __init__ as init


# clean the dfs fetched from national statistics site
def clean_census_data(df_path: str, sheet_name: str):
    """
        Path to input dataframe  and sheet name. must be excel.
    """
    df = pd.read_excel(df_path, sheet_name=sheet_name)

    # columsn names are at 7th or 8th row first make it then remove it as first row but instead of harcoding we look for the most comman pattern found "local"
    header_mask = df.iloc[:, 0].astype(str).str.lower().str.startswith('local')

    if header_mask.any():
        header_idx = header_mask.idxmax()
        df = df.iloc[header_idx:]
    else:
        print(f"'local' not found in column 0 Falling back to row 7.")
        df = df.iloc[7:]


    df.columns = df.iloc[0]
    df = df.reset_index(drop=True)
    df = df[1:]

    df.columns = df.columns.str.lower()  # lowering col names (personal preferrence)
    # regex to clean col names
    df.columns = (df.columns.str.replace(r'[ /]', '_', regex=True).str.replace(r'[:()\-]', '', regex=True))
    df = df.rename(columns={df.columns[1]:"mnemonics"})
    df = df.rename(columns={df.columns[0]:"area"})

    # Remove the las disclaimer and nan row
    first_nan_idx = df[df['area'].isna()].index[0]
    df = df.loc[:first_nan_idx - 1]

    # Extract filename from the poath and rename
    filename = re.search(r'([^/\\]+)\.[^.]+$', df_path).group(1)
    clean_name = re.sub(r'raw_', '', filename)
    clean_name = str.lower(clean_name)

    os.makedirs(init.root_data_clean_dir, exist_ok=True)

    print(f"Saving {init.root_data_clean_dir}{clean_name}.csv")
    df.to_csv(f"{init.root_data_clean_dir}{clean_name}.csv", index=False)


# Join the clean dfs into one single df
def data_joins(df1_path, df2_path, *extra_paths):
    """
    Reads CSVs from paths and joins them on 'area' and 'mnemonics'.
    """
    join_keys = ['area', 'mnemonics']

    # Load and merge the first two required files
    df1 = pd.read_csv(df1_path)
    df2 = pd.read_csv(df2_path)
    combined_df = pd.merge(df1, df2, on=join_keys, how='outer')
    
    # Loop through any additional paths provided
    for path in extra_paths:
        next_df = pd.read_csv(path)
        combined_df = pd.merge(combined_df, next_df, on=join_keys, how='outer')
        
    return combined_df



def district_management():
    df_2011 = pd.read_csv(f"{init.root_data_clean_joins_dir}2011.csv")
    # df_2021 = pd.read_csv(f"{init.root_data_clean_joins_dir}2021.csv")
    
    df_map = pd.read_csv(f"{init.root_data_clean_joins_dir}LAD_Mapping_2011_to_2021.csv")

    df_2011_mapped = pd.merge(df_2011, df_map, left_on='mnemonics', right_on='LAD2011', how='left')
    df_2011_mapped['mnemonics'] = df_2011_mapped['LAD2021'].fillna(df_2011_mapped['mnemonics'])
    df_2011_mapped['area'] = df_2011_mapped['LAD2021NM'].fillna(df_2011_mapped['area'])
    df_2011_mapped = df_2011_mapped.drop(columns=['LAD2011NM', 'LAD2011', 'LAD2021NM', 'LAD2021'])
    df_2011_agg = df_2011_mapped.groupby(['area', 'mnemonics']).sum(numeric_only=True).reset_index()

    df_2011_agg.to_csv(f"{init.root_data_clean_joins_dir}2011_cleaned.csv", index=False)

    print("2011 dataset cleaned and saved!")



def column_consolidation(df_path, column_mapping):
    df = pd.read_csv(df_path)
    df = df.rename(columns=column_mapping)
    df = df.rename(columns=init.tableau_snake_case_names)

    if 'white_roma' in df.columns:
        df['white_other'] = df['white_other'] + df['white_roma']
        df.drop(columns=['white_roma'], inplace=True)
    
    df.to_csv(df_path, index=False)



def main():

    root_dir = init.root_dir
    root_data_dir = init.root_data_dir
    root_data_clean_dir = init.root_data_clean_dir
    root_data_clean_joins_dir = init.root_data_clean_joins_dir
    
    print(root_dir)
    print(root_data_dir)
    print(root_data_clean_dir)
    print(root_data_clean_joins_dir)

    # Clean 2011 Census data (Read from raw directory)
    clean_census_data(df_path=f"{root_data_dir}ethnic_group_raw_2011_ks201ew.xlsx", sheet_name="Total")
    clean_census_data(df_path=f"{root_data_dir}occupation_raw_2011_ks608ew_ks610ew.xlsx", sheet_name="Total; All persons")
    clean_census_data(df_path=f"{root_data_dir}health_raw_2011_qs302ew.xlsx", sheet_name="Total")
    clean_census_data(df_path=f"{root_data_dir}indusrty_raw_2011_ks605ew_ks607ew.xlsx", sheet_name="Data")

    # Clean 2021 census data 
    clean_census_data(df_path=f"{root_data_dir}ethnic_group_raw_2021_ts021.xlsx", sheet_name="Data")
    clean_census_data(df_path=f"{root_data_dir}occupation_raw_2021_ts063.xlsx", sheet_name="Data")
    clean_census_data(df_path=f"{root_data_dir}health_raw_2021_ts037.xlsx", sheet_name="Data")
    clean_census_data(df_path=f"{root_data_dir}industry_raw_2021_ts060.xlsx", sheet_name="Data")

    # joining 2011 data
    df_2011 = data_joins(
        f"{root_data_clean_dir}ethnic_group_2011_ks201ew.csv",
        f"{root_data_clean_dir}occupation_2011_ks608ew_ks610ew.csv",
        f"{root_data_clean_dir}health_2011_qs302ew.csv",
        f"{root_data_clean_dir}indusrty_2011_ks605ew_ks607ew.csv"
        )

    print("2011 Datasets joined")
    
    # joining 2021 data
    df_2021 = data_joins(
        f"{root_data_clean_dir}ethnic_group_2021_ts021.csv",
        f"{root_data_clean_dir}occupation_2021_ts063.csv",
        f"{root_data_clean_dir}health_2021_ts037.csv",
        f"{root_data_clean_dir}industry_2021_ts060.csv"
    )

    print("2021 Datasets joined")

    os.makedirs(root_data_clean_joins_dir, exist_ok=True)

    df_2011.to_csv(f"{root_data_clean_joins_dir}2011.csv", index=False)
    df_2021.to_csv(f"{root_data_clean_joins_dir}2021.csv", index=False)

    print("Datasets saved!")

    district_management()

    print("District merged.")

    column_consolidation(f"{root_data_clean_joins_dir}2011_cleaned.csv", init.census_ethnicity_mapping_2011)
    column_consolidation(f"{root_data_clean_joins_dir}2021.csv", init.census_ethnicity_mapping_2021)

    print("Columns consolidated.")

if __name__ == "__main__":
    main()