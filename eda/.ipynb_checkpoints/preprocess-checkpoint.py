import os
import re
import pandas as pd


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

    os.makedirs("../data/clean", exist_ok=True)
    
    print(f"Saving ../data/clean/{clean_name}.csv")
    df.to_csv(f"../data/clean/{clean_name}.csv", index=False)


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
        # Read the file first, then merge it
        next_df = pd.read_csv(path)
        combined_df = pd.merge(combined_df, next_df, on=join_keys, how='outer')
        
    return combined_df


def main():
    # Clean 2011 Census data
    clean_census_data(df_path="../data/economic_activity_raw_2011_ks601ew_ks603ew.xlsx", sheet_name="All persons")
    clean_census_data(df_path="../data/ethnic_group_raw_2011_ks201ew.xlsx", sheet_name="Total")
    clean_census_data(df_path="../data/occupation_raw_ks608ew_ks610ew.xlsx", sheet_name="Total; All persons")
    clean_census_data(df_path="../data/health_raw_2011_qs302ew.xlsx", sheet_name="Total")
    clean_census_data(df_path="../data/indusrty_raw_2011_ks605ew_ks607ew.xlsx", sheet_name="Data")

    # Clean 2021 census data
    clean_census_data(df_path="../data/econimic_activity_raw_2021_ts066.xlsx", sheet_name="Data")
    clean_census_data(df_path="../data/ethnic_group_raw_2021_ts021.xlsx", sheet_name="Data")
    clean_census_data(df_path="../data/occupation_raw_2021_ts063.xlsx", sheet_name="Data")
    clean_census_data(df_path="../data/health_raw_2021_ts037.xlsx", sheet_name="Data")
    clean_census_data(df_path="../data/industry_raw_2021_ts060.xlsx", sheet_name="Data")

    # joining 2011 data
    df_2011 = data_joins("../data/clean/ethnic_group_2011_ks201ew.csv", "../data/clean/occupation_ks608ew_ks610ew.csv", "../data/clean/health_2011_qs302ew.csv", "../data/clean/indusrty_2011_ks605ew_ks607ew.csv")

    print("2011 Datasets joined")
    
    # joining 2021 data
    df_2021 = data_joins("../data/clean/ethnic_group_2021_ts021.csv", "../data/clean/occupation_2021_ts063.csv", "../data/clean/health_2021_ts037.csv", "../data/clean/industry_2021_ts060.csv")

    print("2021 Datasets joined")

    os.makedirs("../data/clean/joins", exist_ok=True)

    df_2011.to_csv("../data/clean/joins/2011.csv", index=False)
    df_2021.to_csv("../data/clean/joins/2021.csv", index=False)

    print("Datasets saved!")


if __name__ == "__main__":
    main()