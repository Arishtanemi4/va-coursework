import __init__ as init
import pandas as pd
import numpy as np
from sklearn.linear_model import BayesianRidge
import warnings


def compute_proportions(df):
    normalization_map = init.normalization_map
    df_props = pd.DataFrame(index=df.index)

    df_props['area'] = df['area']
    df_props['district_code'] = df['district_code']
    df_props['year'] = df['year']

    for denominator, features in normalization_map.items():
        actual_denom = denominator
        if denominator not in df.columns:
            if denominator == 'all_categories_industry' and 'all_industries' in df.columns:
                actual_denom = 'all_industries'
            else:
                print(f"Warning: Missing denominator '{denominator}'. Skipping these features.")
                continue
        
        valid_features = [col for col in features if col in df.columns]
        if not valid_features:
            continue

        safe_denominator = df[actual_denom].replace(0, 1)  # safeguard
        
        for feature in valid_features:
            df_props[feature] = df[feature] / safe_denominator

    return df_props.fillna(0)


def main():
    print("Loading mapped 2011 and 2021 datasets for forecasting...")
    

    df_2011_mapped = pd.read_csv(f"{init.root_data_output_join_dir}2011_on_2021.csv")
    df_2011_mapped['year'] = 2011

    df_2021 = pd.read_csv(f"{init.root_data_output_join_dir}2021.csv")
    df_2021['year'] = 2021

    props_2011 = compute_proportions(df_2011_mapped)
    props_2021 = compute_proportions(df_2021)

    props_2011 = props_2011.sort_values('district_code').reset_index(drop=True)
    props_2021 = props_2021.sort_values('district_code').reset_index(drop=True)

    totals_to_exclude = ['white_total', 'asian_total', 'black_total', 'mixed_total', 'other_total']
    features_to_forecast = [col for col in props_2011.columns if col not in ['area', 'district_code', 'year'] + totals_to_exclude]

    print("Running Bayesian Ridge regressions to extrapolate 2031...")
    
    forecast_records = []

    X_train = np.array([[2011], [2021]])
    X_test = np.array([[2031]])

    for idx, row_2011 in props_2011.iterrows():
        district = row_2011['district_code']
        area = row_2011['area']
        
        # Locate the corresponding 2021 row
        row_2021 = props_2021[props_2021['district_code'] == district].iloc[0]
        
        record = {
            'area': area,
            'district_code': district,
            'year': 2031
        }
        
        for feature in features_to_forecast:
            y_train = np.array([row_2011[feature], row_2021[feature]])

            clf = BayesianRidge()
            clf.fit(X_train, y_train)
            
            y_pred, y_std = clf.predict(X_test, return_std=True)
            
            pred_clamped = np.clip(y_pred[0], 0, 1)
            
            record[feature + '_prop_forecast'] = pred_clamped
            record[feature + '_prop_std'] = y_std[0] 

        forecast_records.append(record)

    df_2031 = pd.DataFrame(forecast_records)
    
    out_2031 = f"{init.root_data_output_result_dir}2031_forecast.csv"
    df_2031.to_csv(out_2031, index=False)

    print(f"Success! Exported 2031 forecasts with Bayesian uncertainty margins to:\n{out_2031}")

if __name__ == "__main__":
    main()